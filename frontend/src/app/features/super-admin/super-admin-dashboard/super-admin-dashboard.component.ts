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

  // Mock data for RAG status and organization performance
  ragStatus = {
    green: 12,
    amber: 5,
    red: 2
  };

  orgPerformanceData = [
    { org_name: 'Acme Corp', completion_rate: 92, sites: 8, rag_status: 'green' },
    { org_name: 'TechStart Inc', completion_rate: 88, sites: 5, rag_status: 'green' },
    { org_name: 'BuildRight Ltd', completion_rate: 75, sites: 12, rag_status: 'amber' },
    { org_name: 'SafeConstruct', completion_rate: 68, sites: 6, rag_status: 'amber' },
    { org_name: 'MegaBuild Co', completion_rate: 85, sites: 15, rag_status: 'green' }
  ];

  recentActivity = [
    { type: 'organization', action: 'New organization created', details: 'VIG001 - Vanguard Sites', timestamp: '2 minutes ago', icon: 'building' },
    { type: 'site', action: 'Site added', details: 'Vanguard HQ added to VIG001', timestamp: '15 minutes ago', icon: 'map-pin' },
    { type: 'user', action: 'User registered', details: 'john@vanguard.com joined', timestamp: '1 hour ago', icon: 'user' },
    { type: 'defect', action: 'Defect reported', details: 'Critical defect at Site A', timestamp: '2 hours ago', icon: 'alert' },
    { type: 'task', action: 'Task completed', details: 'Safety checklist completed', timestamp: '3 hours ago', icon: 'check' }
  ];

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

    // Mock data for platform growth over last 6 months
    const months = ['Month 1', 'Month 2', 'Month 3', 'Month 4', 'Month 5', 'Month 6'];
    const organizations = [12, 15, 18, 20, 22, 25];
    const sites = [45, 58, 72, 88, 105, 128];
    const users = [150, 195, 248, 310, 385, 472];

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

    // Mock data for subscription tiers
    const config: ChartConfiguration = {
      type: 'pie',
      data: {
        labels: ['Enterprise', 'Professional', 'Standard', 'Basic'],
        datasets: [{
          data: [8, 10, 15, 12],
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
