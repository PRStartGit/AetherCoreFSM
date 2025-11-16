import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SiteService } from '../../../core/services/site.service';
import { Site } from '../../../core/models';

@Component({
  selector: 'app-sites-list',
  templateUrl: './sites-list.component.html',
  styleUrls: ['./sites-list.component.scss']
})
export class SitesListComponent implements OnInit {
  sites: Site[] = [];
  loading = true;
  error: string | null = null;
  searchTerm = '';

  constructor(
    private siteService: SiteService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadSites();
  }

  loadSites(): void {
    this.loading = true;
    this.error = null;

    this.siteService.getAll().subscribe({
      next: (sites) => {
        this.sites = sites;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load sites';
        this.loading = false;
        console.error('Error loading sites:', err);
      }
    });
  }

  get filteredSites(): Site[] {
    if (!this.searchTerm) {
      return this.sites;
    }
    const term = this.searchTerm.toLowerCase();
    return this.sites.filter(site =>
      site.name.toLowerCase().includes(term) ||
      site.site_code.toLowerCase().includes(term) ||
      site.city?.toLowerCase().includes(term)
    );
  }

  createSite(): void {
    this.router.navigate(['/org-admin/sites/new']);
  }

  editSite(siteId: number): void {
    this.router.navigate(['/org-admin/sites/edit', siteId]);
  }

  deleteSite(site: Site): void {
    if (!confirm(`Are you sure you want to delete "${site.name}"?`)) {
      return;
    }

    this.siteService.delete(site.id).subscribe({
      next: () => {
        this.loadSites();
      },
      error: (err) => {
        this.error = 'Failed to delete site';
        console.error('Error deleting site:', err);
      }
    });
  }

  getStatusBadgeClass(isActive: boolean): string {
    return isActive ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800';
  }
}
