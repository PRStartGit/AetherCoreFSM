import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../../core/auth/auth.service';
import { UserService } from '../../../../core/services/user.service';
import { User, UserRole } from '../../../../core/models';

@Component({
  selector: 'app-recipes-landing',
  templateUrl: './recipes-landing.component.html',
  styleUrls: ['./recipes-landing.component.css']
})
export class RecipesLandingComponent implements OnInit {
  currentUser: User | null = null;
  hasRecipeAccess = false;
  loading = true;
  orgAdmins: User[] = [];
  private apiUrl = '/api/v1';

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private http: HttpClient,
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

    // Super admins always have access
    if (this.currentUser.role === UserRole.SUPER_ADMIN) {
      this.hasRecipeAccess = true;
      this.loading = false;
      return;
    }

    // Org admins have automatic access if their organization has the recipes module enabled
    if (this.currentUser.role === UserRole.ORG_ADMIN) {
      // Check if organization has recipes module enabled
      this.checkOrgModuleEnabled('recipes').subscribe({
        next: (enabled) => {
          this.hasRecipeAccess = enabled;
          if (!this.hasRecipeAccess) {
            this.loadOrgAdmins();
          }
          this.loading = false;
        },
        error: () => {
          this.hasRecipeAccess = false;
          this.loading = false;
        }
      });
      return;
    }

    // Check module access for regular users
    this.getUserModuleAccess(this.currentUser.id).subscribe({
      next: (modules) => {
        this.hasRecipeAccess = modules.includes('Zynthio Recipes');

        if (!this.hasRecipeAccess) {
          // Load org admins to display contact information
          this.loadOrgAdmins();
        }

        this.loading = false;
      },
      error: () => {
        this.hasRecipeAccess = false;
        this.loadOrgAdmins();
        this.loading = false;
      }
    });
  }

  getUserModuleAccess(userId: number) {
    return this.http.get<string[]>(`${this.apiUrl}/users/${userId}/module-access`);
  }

  checkOrgModuleEnabled(moduleName: string) {
    return this.http.get<boolean>(`${this.apiUrl}/organizations/modules/${moduleName}/enabled`);
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

  isSuperAdmin(): boolean {
    return this.currentUser?.role === UserRole.SUPER_ADMIN;
  }

  hasCrudAccess(): boolean {
    if (!this.currentUser) return false;

    // Super admins and org admins always have CRUD
    if (this.currentUser.role === UserRole.SUPER_ADMIN || this.currentUser.role === UserRole.ORG_ADMIN) {
      return true;
    }

    // Check job role for CRUD access
    const crudRoles = ['Head Chef', 'Sous Chef', 'General Manager', 'Assistant Manager'];
    if (this.currentUser.job_role && this.currentUser.job_role.name) {
      return crudRoles.includes(this.currentUser.job_role.name);
    }

    return false;
  }
}
