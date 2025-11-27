import { Component, OnInit, AfterViewInit, ViewChild, ElementRef, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { DashboardService } from '../../../core/services/dashboard.service';
import { SuperAdminMetrics, Alert, SiteRanking, ModuleAdoption, DefectTrend } from '../../../core/models';
import { Chart, ChartConfiguration, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-super-admin-dashboard',
  templateUrl: './super-admin-dashboard.component.html',
  styleUrls: ['./super-admin-dashboard.component.css']
})
export class SuperAdminDashboardComponent implements OnInit, AfterViewInit, OnDestroy {
  metrics: SuperAdminMetrics | null = null;
  loading = true;
  error: string | null = null;

  @ViewChild('platformGrowthChart') platformGrowthCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('subscriptionTierChart') subscriptionTierCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('orgPerformanceChart') orgPerformanceCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('defectTrendsChart') defectTrendsCanvas!: ElementRef<HTMLCanvasElement>;

  private platformGrowthChart?: Chart;
  private subscriptionTierChart?: Chart;
  private orgPerformanceChart?: Chart;
  private defectTrendsChart?: Chart;

  ragStatus = {
    green: 0,
    amber: 0,
    red: 0
  };

  orgPerformanceData: any[] = [];
  recentActivity: any[] = [];

  // Pagination for recent activity
  activityPage = 1;
  activityPageSize = 5;
  activityTotal = 0;
  activityTotalPages = 1;
  activityLoading = false;

  // New enhanced data
  alerts: Alert[] = [];
  topSites: SiteRanking[] = [];
  bottomSites: SiteRanking[] = [];
  moduleAdoption: ModuleAdoption[] = [];
  defectTrends: DefectTrend[] = [];

  constructor(
    private dashboardService: DashboardService,
    private router: Router
  ) {}

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

        // Populate RAG status from API
        if (data.rag_summary) {
          this.ragStatus = {
            green: data.rag_summary.green || 0,
            amber: data.rag_summary.amber || 0,
            red: data.rag_summary.red || 0
          };
        }

        // Populate organization performance from API
        if (data.org_performance && data.org_performance.length > 0) {
          this.orgPerformanceData = data.org_performance;
        }

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

        // Populate new enhanced data
        this.alerts = data.alerts || [];
        this.topSites = data.top_sites || [];
        this.bottomSites = data.bottom_sites || [];
        this.moduleAdoption = data.module_adoption || [];
        this.defectTrends = data.defect_trends || [];

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

  loadRecentActivity(page: number = 1): void {
    this.activityLoading = true;
    this.activityPage = page;

    this.dashboardService.getRecentActivity(page, this.activityPageSize).subscribe({
      next: (response) => {
        this.recentActivity = response.items.map((activity: any) => ({
          type: activity.type || 'general',
          action: activity.description || 'Activity',
          details: activity.description || '',
          timestamp: this.formatTimestamp(activity.timestamp),
          icon: this.getIconForType(activity.type),
          organization: activity.organization,
          site: activity.site
        }));
        this.activityTotal = response.total;
        this.activityTotalPages = response.total_pages;
        this.activityLoading = false;
      },
      error: (err) => {
        console.error('Error loading recent activity:', err);
        this.activityLoading = false;
      }
    });
  }

  nextActivityPage(): void {
    if (this.activityPage < this.activityTotalPages) {
      this.loadRecentActivity(this.activityPage + 1);
    }
  }

  prevActivityPage(): void {
    if (this.activityPage > 1) {
      this.loadRecentActivity(this.activityPage - 1);
    }
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

    if (this.defectTrendsCanvas) {
      this.createDefectTrendsChart();
    }
  }

  private createPlatformGrowthChart(): void {
    if (this.platformGrowthChart) {
      this.platformGrowthChart.destroy();
    }

    // Use real growth data from API
    const months: string[] = this.metrics?.growth_data?.map((d: any) => d.month) || [];
    const organizations: number[] = this.metrics?.growth_data?.map((d: any) => d.organizations) || [];
    const sites: number[] = this.metrics?.growth_data?.map((d: any) => d.sites) || [];
    const users: number[] = this.metrics?.growth_data?.map((d: any) => d.users) || [];

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

    // Use real subscription data from API
    const subscription = this.metrics?.subscription_summary || {};
    const labels: string[] = [];
    const data: number[] = [];
    const colors: string[] = [];

    if (subscription['platform_admin'] > 0) {
      labels.push('Platform Admin');
      data.push(subscription['platform_admin']);
      colors.push('#6366f1');
    }
    if (subscription['enterprise'] > 0) {
      labels.push('Enterprise');
      data.push(subscription['enterprise']);
      colors.push('#8b5cf6');
    }
    if (subscription['professional'] > 0) {
      labels.push('Professional');
      data.push(subscription['professional']);
      colors.push('#3b82f6');
    }
    if (subscription['basic'] > 0) {
      labels.push('Basic');
      data.push(subscription['basic']);
      colors.push('#10b981');
    }
    if (subscription['free'] > 0) {
      labels.push('Free');
      data.push(subscription['free']);
      colors.push('#06b6d4');
    }
    if (subscription['trial'] > 0) {
      labels.push('Trial');
      data.push(subscription['trial']);
      colors.push('#f59e0b');
    }

    const config: ChartConfiguration = {
      type: 'pie',
      data: {
        labels: labels,
        datasets: [{
          data: data,
          backgroundColor: colors,
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

    // Use real organization performance data from API
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

  private createDefectTrendsChart(): void {
    if (this.defectTrendsChart) {
      this.defectTrendsChart.destroy();
    }

    if (!this.defectTrends || this.defectTrends.length === 0) return;

    const labels = this.defectTrends.map(d => d.date);
    const created = this.defectTrends.map(d => d.created);
    const resolved = this.defectTrends.map(d => d.resolved);

    const config: ChartConfiguration = {
      type: 'bar',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Created',
            data: created,
            backgroundColor: '#ef4444',
            borderColor: '#dc2626',
            borderWidth: 1
          },
          {
            label: 'Resolved',
            data: resolved,
            backgroundColor: '#22c55e',
            borderColor: '#16a34a',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: 'top'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      }
    };

    this.defectTrendsChart = new Chart(this.defectTrendsCanvas.nativeElement, config);
  }

  // Quick action navigation methods
  navigateToOrganizations(): void {
    this.router.navigate(['/super-admin/organizations']);
  }

  navigateToSites(): void {
    this.router.navigate(['/org-admin/sites']);
  }

  navigateToUsers(): void {
    this.router.navigate(['/org-admin/users']);
  }

  navigateToDefects(): void {
    this.router.navigate(['/defects']);
  }

  navigateToReports(): void {
    this.router.navigate(['/super-admin/reports']);
  }

  // Alert helper methods
  getAlertIcon(type: string): string {
    switch (type) {
      case 'error': return 'error';
      case 'warning': return 'warning';
      default: return 'info';
    }
  }

  getAlertColor(type: string): string {
    switch (type) {
      case 'error': return 'bg-red-100 text-red-800 border-red-200';
      case 'warning': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-blue-100 text-blue-800 border-blue-200';
    }
  }

  // Format currency
  formatCurrency(value: number): string {
    return '£' + value.toLocaleString('en-GB', { minimumFractionDigits: 0, maximumFractionDigits: 0 });
  }

  getAverageCompletionRate(): number {
    if (!this.orgPerformanceData || this.orgPerformanceData.length === 0) return 0;
    const sum = this.orgPerformanceData.reduce((acc, org) => acc + (org.completion_rate || 0), 0);
    return Math.round(sum / this.orgPerformanceData.length);
  }

  getPlatformHealthScore(): number {
    // Calculate platform health based on RAG status distribution
    // Green orgs contribute 100%, Amber 50%, Red 0%
    const total = this.ragStatus.green + this.ragStatus.amber + this.ragStatus.red;
    if (total === 0) return 100;
    return Math.round((this.ragStatus.green * 100 + this.ragStatus.amber * 50) / total);
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
    if (this.defectTrendsChart) {
      this.defectTrendsChart.destroy();
    }
  }
}
