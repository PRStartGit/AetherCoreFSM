import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { OrganizationService } from '../../../../core/services/organization.service';
import { Organization } from '../../../../core/models';

@Component({
  selector: 'app-organization-list',
  templateUrl: './organization-list.component.html',
  styleUrls: ['./organization-list.component.scss']
})
export class OrganizationListComponent implements OnInit {
  organizations: Organization[] = [];
  loading = true;
  error: string | null = null;

  constructor(
    private organizationService: OrganizationService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadOrganizations();
  }

  loadOrganizations(): void {
    this.loading = true;
    this.error = null;

    this.organizationService.getAll().subscribe({
      next: (orgs) => {
        this.organizations = orgs;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load organizations';
        this.loading = false;
        console.error('Error loading organizations:', err);
      }
    });
  }

  navigateToCreate(): void {
    this.router.navigate(['/super-admin/organizations/new']);
  }

  navigateToEdit(org: Organization): void {
    this.router.navigate(['/super-admin/organizations', org.id]);
  }

  deleteOrganization(org: Organization): void {
    if (confirm(`Are you sure you want to delete "${org.name}"? This action cannot be undone.`)) {
      this.organizationService.delete(org.id).subscribe({
        next: () => {
          this.loadOrganizations();
        },
        error: (err) => {
          alert('Failed to delete organization');
          console.error('Error deleting organization:', err);
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
}
