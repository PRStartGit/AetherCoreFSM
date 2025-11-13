import { Component, OnInit } from '@angular/core';
import { DashboardService } from '../../../core/services/dashboard.service';
import { OrgAdminMetrics, RAGStatus } from '../../../core/models';

@Component({
  selector: 'app-org-admin-dashboard',
  templateUrl: './org-admin-dashboard.component.html',
  styleUrls: ['./org-admin-dashboard.component.css']
})
export class OrgAdminDashboardComponent implements OnInit {
  metrics: OrgAdminMetrics | null = null;
  loading = true;
  error: string | null = null;
  displayedColumns: string[] = ['site_name', 'rag_status', 'completion_rate', 'open_defects'];

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadMetrics();
  }

  loadMetrics(): void {
    this.loading = true;
    this.error = null;

    this.dashboardService.getOrgAdminMetrics().subscribe({
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

  getRAGColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'green':
        return '#43e97b';
      case 'amber':
        return '#fa709a';
      case 'red':
        return '#ff6b6b';
      default:
        return '#ccc';
    }
  }
}
