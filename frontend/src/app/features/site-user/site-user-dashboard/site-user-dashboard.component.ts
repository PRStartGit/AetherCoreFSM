import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../../../core/services/dashboard.service';
import { SiteUserMetrics, ChecklistStatus } from '../../../core/models';

@Component({
  selector: 'app-site-user-dashboard',
  templateUrl: './site-user-dashboard.component.html',
  styleUrls: ['./site-user-dashboard.component.css']
})
export class SiteUserDashboardComponent implements OnInit {
  metrics: SiteUserMetrics | null = null;
  loading = true;
  error: string | null = null;

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadMetrics();
  }

  loadMetrics(): void {
    this.loading = true;
    this.error = null;

    this.dashboardService.getSiteUserMetrics().subscribe({
      next: (data) => {
        this.metrics = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load dashboard metrics';
        this.loading = false;
        console.error('Error loading metrics:', err);
      }
    });
  }

  refresh(): void {
    this.loadMetrics();
  }

  getStatusColor(status: string): string {
    switch (status) {
      case ChecklistStatus.COMPLETED:
        return '#43e97b';
      case ChecklistStatus.IN_PROGRESS:
        return '#4facfe';
      case ChecklistStatus.PENDING:
        return '#fa709a';
      case ChecklistStatus.OVERDUE:
        return '#ff6b6b';
      default:
        return '#ccc';
    }
  }

  getProgressPercentage(checklist: any): number {
    if (checklist.total_tasks === 0) return 0;
    return Math.round((checklist.completed_tasks / checklist.total_tasks) * 100);
  }
}
