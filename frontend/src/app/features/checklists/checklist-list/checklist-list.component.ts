import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ChecklistService } from '../../../core/services/checklist.service';
import { SiteService } from '../../../core/services/site.service';
import { AuthService } from '../../../core/auth/auth.service';
import { Checklist, ChecklistStatus } from '../../../core/models/monitoring.model';
import { Site, UserRole } from '../../../core/models';
import { ChecklistFormComponent } from '../checklist-form/checklist-form.component';

@Component({
  selector: 'app-checklist-list',
  templateUrl: './checklist-list.component.html',
  styleUrls: ['./checklist-list.component.scss']
})
export class ChecklistListComponent implements OnInit {
  checklists: Checklist[] = [];
  sites: Site[] = [];
  loading = false;
  displayedColumns: string[] = ['site', 'category', 'status', 'due_date', 'progress', 'actions'];

  // Filter options
  selectedStatus: string = 'all';
  selectedSite: string = 'all';
  selectedDate: string = '';
  statuses = Object.values(ChecklistStatus);

  // Storage key for filter persistence
  private readonly FILTER_STORAGE_KEY = 'checklist_filters';

  constructor(
    private checklistService: ChecklistService,
    private siteService: SiteService,
    private authService: AuthService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Restore filters from session storage
    this.restoreFilters();

    this.loadSites();
    this.loadChecklists();
  }

  private restoreFilters(): void {
    const savedFilters = sessionStorage.getItem(this.FILTER_STORAGE_KEY);
    if (savedFilters) {
      try {
        const filters = JSON.parse(savedFilters);
        this.selectedStatus = filters.status || 'all';
        this.selectedSite = filters.site || 'all';
        this.selectedDate = filters.date || new Date().toISOString().split('T')[0];
      } catch {
        // If parsing fails, use defaults
        this.selectedDate = new Date().toISOString().split('T')[0];
      }
    } else {
      // Set default date to today if no saved filters
      this.selectedDate = new Date().toISOString().split('T')[0];
    }
  }

  private saveFilters(): void {
    const filters = {
      status: this.selectedStatus,
      site: this.selectedSite,
      date: this.selectedDate
    };
    sessionStorage.setItem(this.FILTER_STORAGE_KEY, JSON.stringify(filters));
  }

  clearFilters(): void {
    this.selectedStatus = 'all';
    this.selectedSite = 'all';
    this.selectedDate = new Date().toISOString().split('T')[0];
    sessionStorage.removeItem(this.FILTER_STORAGE_KEY);
    this.loadChecklists();
  }

  hasActiveFilters(): boolean {
    const today = new Date().toISOString().split('T')[0];
    return this.selectedStatus !== 'all' ||
           this.selectedSite !== 'all' ||
           this.selectedDate !== today;
  }

  loadSites(): void {
    this.siteService.getAll().subscribe({
      next: (sites: any[]) => {
        // Filter sites based on user access for site users
        const currentUser = this.authService.getUser();
        if (currentUser?.role === UserRole.SITE_USER && currentUser.site_ids?.length) {
          this.sites = sites.filter(site => currentUser.site_ids!.includes(site.id));
        } else {
          this.sites = sites;
        }
      },
      error: (error: any) => {
        console.error('Error loading sites:', error);
      }
    });
  }

  loadChecklists(): void {
    this.loading = true;
    const status = this.selectedStatus !== 'all' ? this.selectedStatus as ChecklistStatus : undefined;
    const siteId = this.selectedSite !== 'all' ? parseInt(this.selectedSite) : undefined;

    // Use the same date for both start and end to get checklists for a specific day
    const startDate = this.selectedDate || undefined;
    const endDate = this.selectedDate || undefined;

    this.checklistService.getAll(siteId, undefined, status, startDate, endDate).subscribe({
      next: (checklists: any[]) => {
        this.checklists = checklists;
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading checklists:', error);
        this.snackBar.open('Failed to load checklists', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(ChecklistFormComponent, {
      width: '700px',
      data: {
        checklist: null,
        sites: this.sites
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadChecklists();
      }
    });
  }

  openCompletionView(checklist: Checklist): void {
    this.router.navigate(['/checklists', checklist.id, 'complete']);
  }

  deleteChecklist(checklist: Checklist): void {
    if (confirm(`Are you sure you want to delete this checklist?`)) {
      this.checklistService.delete(checklist.id).subscribe({
        next: () => {
          this.snackBar.open('Checklist deleted successfully', 'Close', { duration: 3000 });
          this.loadChecklists();
        },
        error: (error: any) => {
          console.error('Error deleting checklist:', error);
          this.snackBar.open('Failed to delete checklist', 'Close', { duration: 3000 });
        }
      });
    }
  }

  getSiteName(siteId: number): string {
    const site = this.sites.find(s => s.id === siteId);
    return site?.name || 'Unknown';
  }

  getStatusClass(status: ChecklistStatus): string {
    return status.toLowerCase().replace('_', '-');
  }

  getProgressPercentage(checklist: Checklist): number {
    if (!checklist.total_items || checklist.total_items === 0 || !checklist.completed_items) {
      return 0;
    }
    return Math.round((checklist.completed_items / checklist.total_items) * 100);
  }

  isOverdue(checklist: Checklist): boolean {
    if (!checklist.checklist_date) {
      return false;
    }
    const dueDate = new Date(checklist.checklist_date);
    const now = new Date();
    return dueDate < now && checklist.status !== ChecklistStatus.COMPLETED;
  }

  onFilterChange(): void {
    this.saveFilters();
    this.loadChecklists();
  }

  canComplete(checklist: Checklist): boolean {
    return checklist.status === ChecklistStatus.PENDING || checklist.status === ChecklistStatus.IN_PROGRESS;
  }

  isPastDay(checklist: Checklist): boolean {
    if (!checklist.checklist_date) {
      return false;
    }
    const checklistDate = new Date(checklist.checklist_date);
    const today = new Date();
    // Set both to midnight for accurate day comparison
    checklistDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    return checklistDate < today;
  }

  getDisplayStatus(checklist: Checklist): string {
    // Show "Missed" for overdue checklists or past-day checklists that are still pending/in progress
    if (checklist.status === ChecklistStatus.OVERDUE ||
        (this.isPastDay(checklist) && (checklist.status === ChecklistStatus.PENDING || checklist.status === ChecklistStatus.IN_PROGRESS))) {
      return 'Missed';
    }
    return checklist.status.replace('_', ' ');
  }

  getStatusBadgeClass(checklist: Checklist): string {
    // Use red styling for missed/overdue checklists
    if (checklist.status === ChecklistStatus.OVERDUE ||
        (this.isPastDay(checklist) && (checklist.status === ChecklistStatus.PENDING || checklist.status === ChecklistStatus.IN_PROGRESS))) {
      return 'bg-red-100 text-red-800';
    }

    // Default styling based on status
    const statusMap: { [key: string]: string } = {
      'pending': 'bg-yellow-100 text-yellow-800',
      'in_progress': 'bg-blue-100 text-blue-800',
      'completed': 'bg-green-100 text-green-800',
      'overdue': 'bg-red-100 text-red-800'
    };
    return statusMap[checklist.status] || 'bg-gray-100 text-gray-800';
  }

  getStatusLabel(status: string): string {
    const labelMap: { [key: string]: string } = {
      'pending': 'Pending',
      'in_progress': 'In Progress',
      'completed': 'Completed',
      'overdue': 'Missed'
    };
    return labelMap[status] || status.replace('_', ' ');
  }

isSuperAdmin(): boolean {    return this.authService.isSuperAdmin();  }
  isSiteUser(): boolean {
    return this.authService.isSiteUser();
  }
}
