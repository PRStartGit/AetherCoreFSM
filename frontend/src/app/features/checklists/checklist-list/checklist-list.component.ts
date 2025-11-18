import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { ChecklistService } from '../../../core/services/checklist.service';
import { SiteService } from '../../../core/services/site.service';
import { AuthService } from '../../../core/auth/auth.service';
import { Checklist, ChecklistStatus } from '../../../core/models/monitoring.model';
import { Site } from '../../../core/models';
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
  startDate: string = '';
  endDate: string = '';
  statuses = Object.values(ChecklistStatus);

  constructor(
    private checklistService: ChecklistService,
    private siteService: SiteService,
    private authService: AuthService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadSites();
    this.loadChecklists();
  }

  loadSites(): void {
    this.siteService.getAll().subscribe({
      next: (sites: any[]) => {
        this.sites = sites;
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
    const startDate = this.startDate || undefined;
    const endDate = this.endDate || undefined;

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
    this.loadChecklists();
  }

  canComplete(checklist: Checklist): boolean {
    return checklist.status === ChecklistStatus.PENDING || checklist.status === ChecklistStatus.IN_PROGRESS;
  }

  isSiteUser(): boolean {
    return this.authService.isSiteUser();
  }
}
