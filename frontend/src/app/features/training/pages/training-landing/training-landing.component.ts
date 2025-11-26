import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../../core/auth/auth.service';
import { TrainingService } from '../../services/training.service';
import { UserService } from '../../../../core/services/user.service';
import { User, UserRole } from '../../../../core/models';

@Component({
  selector: 'app-training-landing',
  templateUrl: './training-landing.component.html',
  styleUrls: ['./training-landing.component.css']
})
export class TrainingLandingComponent implements OnInit {
  currentUser: User | null = null;
  hasTrainingAccess = false;
  loading = true;
  orgAdmins: User[] = [];

  constructor(
    private authService: AuthService,
    private trainingService: TrainingService,
    private userService: UserService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe({
      next: (user) => {
        this.currentUser = user;
        if (!user) {
          this.router.navigate(['/login']);
          return;
        }
        this.checkAccess();
      },
      error: () => {
        this.router.navigate(['/login']);
      }
    });
  }

  checkAccess(): void {
    if (!this.currentUser) return;

    // Super admins have automatic access
    if (this.currentUser.role === UserRole.SUPER_ADMIN) {
      this.hasTrainingAccess = true;
      this.loading = false;
      return;
    }

    // Check module access for other users
    this.trainingService.getUserModuleAccess(this.currentUser.id).subscribe({
      next: (modules) => {
        this.hasTrainingAccess = modules.includes('TRAINING');

        if (!this.hasTrainingAccess) {
          // Load org admins to display contact information
          this.loadOrgAdmins();
        }

        this.loading = false;
      },
      error: () => {
        this.hasTrainingAccess = false;
        this.loadOrgAdmins();
        this.loading = false;
      }
    });
  }

  loadOrgAdmins(): void {
    if (!this.currentUser || !this.currentUser.organization_id) return;

    // Get all users from the organization who are org admins
    this.userService.getAll(this.currentUser.organization_id).subscribe({
      next: (users: User[]) => {
        this.orgAdmins = users.filter(
          (u: User) => u.organization_id === this.currentUser!.organization_id &&
               u.role === UserRole.ORG_ADMIN
        );
      },
      error: (err: any) => {
        console.error('Failed to load org admins:', err);
      }
    });
  }
}
