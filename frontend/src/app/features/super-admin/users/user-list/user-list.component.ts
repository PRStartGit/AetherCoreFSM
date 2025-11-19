import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { UserService } from '../../../../core/services/user.service';
import { OrganizationService } from '../../../../core/services/organization.service';
import { AuthService } from '../../../../core/auth/auth.service';
import { User, Organization } from '../../../../core/models';

@Component({
  selector: 'app-user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements OnInit {
  users: User[] = [];
  organizations: Organization[] = [];
  loading = true;
  error: string | null = null;
  filterOrganizationId: number | null = null;

  constructor(
    private userService: UserService,
    private organizationService: OrganizationService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadOrganizations();
    this.loadUsers();
  }

  loadOrganizations(): void {
    this.organizationService.getAll().subscribe({
      next: (orgs) => {
        this.organizations = orgs;
      },
      error: (err) => {
        console.error('Error loading organizations:', err);
      }
    });
  }

  loadUsers(): void {
    this.loading = true;
    this.error = null;

    this.userService.getAll(this.filterOrganizationId || undefined).subscribe({
      next: (users) => {
        this.users = users;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load users';
        this.loading = false;
        console.error('Error loading users:', err);
      }
    });
  }

  onFilterChange(): void {
    this.loadUsers();
  }

  navigateToCreate(): void {
    this.router.navigate([this.getBaseRoute() + '/new']);
  }

  navigateToEdit(user: User): void {
    this.router.navigate([this.getBaseRoute(), user.id]);
  }

  deleteUser(user: User): void {
    if (confirm(`Are you sure you want to delete "${user.full_name}"? This action cannot be undone.`)) {
      this.userService.delete(user.id).subscribe({
        next: () => {
          this.loadUsers();
        },
        error: (err) => {
          alert('Failed to delete user');
          console.error('Error deleting user:', err);
        }
      });
    }
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  getRoleName(role: string): string {
    const roleMap: { [key: string]: string } = {
      'super_admin': 'Super Admin',
      'org_admin': 'Org Admin',
      'site_user': 'Site User'
    };
    return roleMap[role] || role;
  }

  getRoleColor(role: string): string {
    const colorMap: { [key: string]: string } = {
      'super_admin': 'bg-purple-100 text-purple-800',
      'org_admin': 'bg-blue-100 text-blue-800',
      'site_user': 'bg-green-100 text-green-800'
    };
    return colorMap[role] || 'bg-gray-100 text-gray-800';
  }

  getOrganizationName(orgId: number | null): string {
    if (!orgId) return 'N/A';
    const org = this.organizations.find(o => o.id === orgId);
    return org ? org.name : 'Unknown';
  }


  getBaseRoute(): string {
    const currentUser = this.authService.getUser();
    return currentUser?.role === 'super_admin' ? '/super-admin/users' : '/org-admin/users';
  }

  sendPasswordReset(user: User): void {
    if (confirm(`Send password reset email to "${user.full_name}" (${user.email})?`)) {
      // Find the organization org_id for this user
      const org = this.organizations.find(o => o.id === user.organization_id);
      const orgId = org ? org.org_id : 'zyn'; // Default to 'zyn' for super admins

      this.authService.requestPasswordReset({
        organization_id: orgId,
        email: user.email
      }).subscribe({
        next: () => {
          alert('Password reset email sent successfully!');
        },
        error: (err) => {
          alert('Failed to send password reset email');
          console.error('Error sending password reset:', err);
        }
      });
    }
  }
}
