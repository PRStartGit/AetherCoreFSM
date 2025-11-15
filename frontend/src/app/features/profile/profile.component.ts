import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { AuthService } from '../../core/auth/auth.service';
import { UserService } from '../../core/services/user.service';
import { OrganizationService } from '../../core/services/organization.service';
import { SiteService } from '../../core/services/site.service';
import { User } from '../../core/models/user.model';
import { Organization } from '../../core/models/organization.model';
import { Site } from '../../core/models';
import { ChangePasswordDialogComponent } from '../../shared/dialogs/change-password-dialog/change-password-dialog.component';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.scss']
})
export class ProfileComponent implements OnInit {
  user: User | null = null;
  organization: Organization | null = null;
  assignedSites: Site[] = [];
  loading = false;
  editMode = false;

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private organizationService: OrganizationService,
    private siteService: SiteService,
    private router: Router,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadUserProfile();
  }

  loadUserProfile(): void {
    this.loading = true;
    const currentUser = this.authService.getUser();

    if (!currentUser) {
      this.router.navigate(['/login']);
      return;
    }

    // Load full user details
    this.userService.getById(currentUser.id).subscribe({
      next: (user: User) => {
        this.user = user;
        this.loadOrganization();
        this.loadAssignedSites();
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading user profile:', error);
        this.snackBar.open('Failed to load profile', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  loadOrganization(): void {
    if (this.user?.organization_id) {
      this.organizationService.getById(this.user.organization_id).subscribe({
        next: (org: Organization) => {
          this.organization = org;
        },
        error: (error: any) => {
          console.error('Error loading organization:', error);
        }
      });
    }
  }

  loadAssignedSites(): void {
    if (this.user?.site_ids && this.user.site_ids.length > 0) {
      this.siteService.getAll().subscribe({
        next: (sites: Site[]) => {
          this.assignedSites = sites.filter(site =>
            this.user?.site_ids?.includes(site.id)
          );
        },
        error: (error: any) => {
          console.error('Error loading sites:', error);
        }
      });
    }
  }

  getRoleName(): string {
    if (!this.user) return '';

    switch (this.user.role) {
      case 'super_admin':
        return 'Super Admin';
      case 'org_admin':
        return 'Organization Admin';
      case 'site_user':
        return 'Site User';
      default:
        return this.user.role;
    }
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  }

  toggleEditMode(): void {
    this.editMode = !this.editMode;
  }

  onSaveProfile(): void {
    // TODO: Implement profile editing
    this.snackBar.open('Profile editing coming soon', 'Close', { duration: 3000 });
  }

  onChangePassword(): void {
    const dialogRef = this.dialog.open(ChangePasswordDialogComponent, {
      width: '500px',
      maxWidth: '95vw',
      disableClose: false,
      autoFocus: true
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        // result contains { old_password, new_password, confirm_password }
        const changeData = {
          old_password: result.old_password,
          new_password: result.new_password
        };

        this.authService.changePassword(changeData).subscribe({
          next: (response) => {
            this.snackBar.open('Password changed successfully!', 'Close', { duration: 5000 });
          },
          error: (error) => {
            const message = error.error?.detail || 'Failed to change password. Please try again.';
            this.snackBar.open(message, 'Close', { duration: 5000 });
          }
        });
      }
    });
  }
}
