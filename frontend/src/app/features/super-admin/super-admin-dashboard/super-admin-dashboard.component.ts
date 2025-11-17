import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { DashboardService } from '../../../core/services/dashboard.service';
import { SuperAdminMetrics } from '../../../core/models';
import { Chart, ChartConfiguration, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-super-admin-dashboard',
  templateUrl: './super-admin-dashboard.component.html',
  styleUrls: ['./super-admin-dashboard.component.css']
})
export class SuperAdminDashboardComponent implements OnInit, AfterViewInit {
  metrics: SuperAdminMetrics | null = null;
  loading = true;
  error: string | null = null;

  @ViewChild('platformGrowthChart') platformGrowthCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('subscriptionTierChart') subscriptionTierCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('orgPerformanceChart') orgPerformanceCanvas!: ElementRef<HTMLCanvasElement>;

  private platformGrowthChart?: Chart;
  private subscriptionTierChart?: Chart;
  private orgPerformanceChart?: Chart;

  // TODO: Replace with real RAG status data from API when available
  // Backend needs to provide organization-level RAG aggregation endpoint
  ragStatus = {
    green: 0,
    amber: 0,
    red: 0
  };

  // TODO: Replace with real organization performance data from API when available
  // Backend needs to provide top organizations by completion rate endpoint
  orgPerformanceData: any[] = [];

  // This will be populated from API metrics.recent_activity
  recentActivity: any[] = [];

  constructor(private dashboardService: DashboardService) {}

  ngOnInit(): void {
    this.loadMetrics();
  }

  ngAfterViewInit(): void {
    // Initialize charts after view is ready
    setTimeout(() => {
      this.initializeCharts();
    }, 100);
  }

  loadMetrics(): void {
    this.loading = true;
    this.error = null;

    this.dashboardService.getSuperAdminMetrics().subscribe({
      next: (data) => {
        this.metrics = data;

        // Populate recent activity from API data
        if (data.recent_activity && data.recent_activity.length > 0) {
          this.recentActivity = data.recent_activity.map((activity: any) => ({
            type: activity.type || 'general',
            action: activity.description || 'Activity',
            details: activity.description || '',
            timestamp: this.formatTimestamp(activity.timestamp),
            icon: this.getIconForType(activity.type)
          }));
        }

        this.loading = false;
        // Update charts with new data
        setTimeout(() => {
          this.initializeCharts();
        }, 100);
      },
      error: (err) => {
        this.error = 'Failed to load dashboard metrics';
        this.loading = false;
        console.error('Error loading metrics:', err);
      }
    });
  }

  private formatTimestamp(timestamp: string): string {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString();
  }

  private getIconForType(type: string): string {
    const iconMap: { [key: string]: string } = {
      'organization': 'building',
      'site': 'map-pin',
      'user': 'user',
      'defect': 'alert',
      'task': 'check',
      'checklist': 'check',
      'report': 'document'
    };
    return iconMap[type?.toLowerCase()] || 'info';
  }

  refresh(): void {
    this.loadMetrics();
  }

  getRAGColor(status: string): string {
    switch (status.toLowerCase()) {
      case 'green':
        return '#22c55e';
      case 'amber':
        return '#eab308';
      case 'red':
        return '#ef4444';
      default:
        return '#ccc';
    }
  }

  getActivityColor(type: string): string {
    switch (type) {
      case 'organization':
      case 'site':
        return 'text-blue-600 bg-blue-100';
      case 'user':
        return 'text-green-600 bg-green-100';
      case 'defect':
        return 'text-orange-600 bg-orange-100';
      case 'task':
        return 'text-purple-600 bg-purple-100';
      default:
        return 'text-gray-600 bg-gray-100';
    }
  }

  private initializeCharts(): void {
    if (!this.platformGrowthCanvas || !this.subscriptionTierCanvas || !this.orgPerformanceCanvas) {
      return;
    }

    this.createPlatformGrowthChart();
    this.createSubscriptionTierChart();
    this.createOrgPerformanceChart();
  }

  private createPlatformGrowthChart(): void {
    if (this.platformGrowthChart) {
      this.platformGrowthChart.destroy();
    }

    // TODO: Replace with real historical growth data from API
    // Backend needs to provide time-series data for organizations, sites, and users
    const months: string[] = [];
    const organizations: number[] = [];
    const sites: number[] = [];
    const users: number[] = [];

    const config: ChartConfiguration = {
      type: 'line',
      data: {
        labels: months,
        datasets: [
          {
            label: 'Organizations',
            data: organizations,
            borderColor: '#8b5cf6',
            backgroundColor: 'rgba(139, 92, 246, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 4,
            pointBackgroundColor: '#8b5cf6',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
          },
          {
            label: 'Sites',
            data: sites,
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 4,
            pointBackgroundColor: '#3b82f6',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
          },
          {
            label: 'Users',
            data: users,
            borderColor: '#10b981',
            backgroundColor: 'rgba(16, 185, 129, 0.1)',
            tension: 0.4,
            fill: false,
            pointRadius: 4,
            pointBackgroundColor: '#10b981',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top',
          },
          title: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    };

    this.platformGrowthChart = new Chart(this.platformGrowthCanvas.nativeElement, config);
  }

  private createSubscriptionTierChart(): void {
    if (this.subscriptionTierChart) {
      this.subscriptionTierChart.destroy();
    }

    // TODO: Replace with real subscription tier distribution from API
    // Backend needs to provide organization count grouped by subscription tier
    const config: ChartConfiguration = {
      type: 'pie',
      data: {
        labels: [],
        datasets: [{
          data: [],
          backgroundColor: [
            '#8b5cf6', // Purple for Enterprise
            '#3b82f6', // Blue for Professional
            '#06b6d4', // Cyan for Standard
            '#10b981'  // Green for Basic
          ],
          borderColor: '#fff',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'right',
          },
          title: {
            display: false
          }
        }
      }
    };

    this.subscriptionTierChart = new Chart(this.subscriptionTierCanvas.nativeElement, config);
  }

  private createOrgPerformanceChart(): void {
    if (this.orgPerformanceChart) {
      this.orgPerformanceChart.destroy();
    }

    // Use mock organization performance data
    const orgNames = this.orgPerformanceData.map(org => org.org_name);
    const completionRates = this.orgPerformanceData.map(org => org.completion_rate);

    const config: ChartConfiguration = {
      type: 'bar',
      data: {
        labels: orgNames,
        datasets: [{
          label: 'Completion Rate (%)',
          data: completionRates,
          backgroundColor: [
            '#8b5cf6',
            '#6366f1',
            '#3b82f6',
            '#06b6d4',
            '#10b981'
          ],
          borderColor: [
            '#7c3aed',
            '#4f46e5',
            '#2563eb',
            '#0891b2',
            '#059669'
          ],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: false
          }
        },
        scales: {
          x: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: (value) => value + '%'
            }
          }
        }
      }
    };

    this.orgPerformanceChart = new Chart(this.orgPerformanceCanvas.nativeElement, config);
  }

  ngOnDestroy(): void {
    // Clean up charts on component destruction
    if (this.platformGrowthChart) {
      this.platformGrowthChart.destroy();
    }
    if (this.subscriptionTierChart) {
      this.subscriptionTierChart.destroy();
    }
    if (this.orgPerformanceChart) {
      this.orgPerformanceChart.destroy();
    }
  }
}
