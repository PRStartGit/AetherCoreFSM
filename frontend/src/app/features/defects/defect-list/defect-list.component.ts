import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DefectService } from '../../../core/services/defect.service';
import { SiteService } from '../../../core/services/site.service';
import { Defect, DefectStatus, DefectSeverity, Site } from '../../../core/models';

@Component({
  selector: 'app-defect-list',
  templateUrl: './defect-list.component.html',
  styleUrls: ['./defect-list.component.scss']
})
export class DefectListComponent implements OnInit {
  defects: Defect[] = [];
  sites: Site[] = [];
  loading = false;
  error: string | null = null;

  // Filters
  selectedStatus: DefectStatus | '' = '';
  selectedSeverity: DefectSeverity | '' = '';
  selectedSiteId: number | null = null;

  DefectStatus = DefectStatus;
  DefectSeverity = DefectSeverity;

  constructor(
    private defectService: DefectService,
    private siteService: SiteService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadSites();
    this.loadDefects();
  }

  loadSites(): void {
    this.siteService.getAll().subscribe({
      next: (sites) => this.sites = sites,
      error: (err) => console.error('Error loading sites:', err)
    });
  }

  loadDefects(): void {
    this.loading = true;
    this.error = null;

    const status = this.selectedStatus || undefined;
    const severity = this.selectedSeverity || undefined;
    const siteId = this.selectedSiteId || undefined;

    this.defectService.getAll(siteId, status as DefectStatus, severity as DefectSeverity).subscribe({
      next: (defects) => {
        this.defects = defects;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load defects';
        this.loading = false;
        console.error('Error loading defects:', err);
      }
    });
  }

  applyFilters(): void {
    this.loadDefects();
  }

  clearFilters(): void {
    this.selectedStatus = '';
    this.selectedSeverity = '';
    this.selectedSiteId = null;
    this.loadDefects();
  }

  createDefect(): void {
    this.router.navigate(['/defects/new']);
  }

  editDefect(id: number): void {
    this.router.navigate(['/defects', id, 'edit']);
  }

  closeDefect(id: number): void {
    if (confirm('Are you sure you want to close this defect?')) {
      this.defectService.close(id).subscribe({
        next: () => this.loadDefects(),
        error: (err) => {
          alert('Failed to close defect');
          console.error('Error closing defect:', err);
        }
      });
    }
  }

  deleteDefect(id: number): void {
    if (confirm('Are you sure you want to delete this defect?')) {
      this.defectService.delete(id).subscribe({
        next: () => this.loadDefects(),
        error: (err) => {
          alert('Failed to delete defect');
          console.error('Error deleting defect:', err);
        }
      });
    }
  }

  getSeverityColor(severity: DefectSeverity): string {
    switch (severity) {
      case DefectSeverity.LOW: return 'bg-blue-100 text-blue-800';
      case DefectSeverity.MEDIUM: return 'bg-yellow-100 text-yellow-800';
      case DefectSeverity.HIGH: return 'bg-orange-100 text-orange-800';
      case DefectSeverity.CRITICAL: return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  getStatusColor(status: DefectStatus): string {
    switch (status) {
      case DefectStatus.OPEN: return 'bg-red-100 text-red-800';
      case DefectStatus.IN_PROGRESS: return 'bg-blue-100 text-blue-800';
      case DefectStatus.RESOLVED: return 'bg-green-100 text-green-800';
      case DefectStatus.CLOSED: return 'bg-gray-100 text-gray-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  }

  getSiteName(siteId: number): string {
    const site = this.sites.find(s => s.id === siteId);
    return site?.name || `Site #${siteId}`;
  }
}
