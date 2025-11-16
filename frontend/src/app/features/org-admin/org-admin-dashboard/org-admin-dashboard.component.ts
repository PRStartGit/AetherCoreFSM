import { Component, OnInit, AfterViewInit, ViewChild, ElementRef } from '@angular/core';
import { DashboardService } from '../../../core/services/dashboard.service';
import { OrgAdminMetrics, RAGStatus } from '../../../core/models';
import { Chart, ChartConfiguration, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-org-admin-dashboard',
  templateUrl: './org-admin-dashboard.component.html',
  styleUrls: ['./org-admin-dashboard.component.css']
})
export class OrgAdminDashboardComponent implements OnInit, AfterViewInit {
  metrics: OrgAdminMetrics | null = null;
  loading = true;
  error: string | null = null;
  displayedColumns: string[] = ['site_name', 'rag_status', 'completion_rate', 'open_defects'];

  @ViewChild('completionTrendChart') completionTrendCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('defectDistributionChart') defectDistributionCanvas!: ElementRef<HTMLCanvasElement>;
  @ViewChild('sitePerformanceChart') sitePerformanceCanvas!: ElementRef<HTMLCanvasElement>;

  private completionTrendChart?: Chart;
  private defectDistributionChart?: Chart;
  private sitePerformanceChart?: Chart;

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

    this.dashboardService.getOrgAdminMetrics().subscribe({
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
        return '#43e97b';
      case 'amber':
        return '#fa709a';
      case 'red':
        return '#ff6b6b';
      default:
        return '#ccc';
    }
  }

  private initializeCharts(): void {
    if (!this.completionTrendCanvas || !this.defectDistributionCanvas || !this.sitePerformanceCanvas) {
      return;
    }

    this.createCompletionTrendChart();
    this.createDefectDistributionChart();
    this.createSitePerformanceChart();
  }

  private createCompletionTrendChart(): void {
    if (this.completionTrendChart) {
      this.completionTrendChart.destroy();
    }

    // TODO: Replace with real historical completion rate data from API
    // Backend needs to provide 7-day time-series data for completion rates
    const last7Days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'];
    const completionRates = [72, 75, 78, 76, 82, 85, 88];

    const config: ChartConfiguration = {
      type: 'line',
      data: {
        labels: last7Days,
        datasets: [{
          label: 'Completion Rate (%)',
          data: completionRates,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointBackgroundColor: '#3b82f6',
          pointBorderColor: '#fff',
          pointBorderWidth: 2
        }]
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
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: (value) => value + '%'
            }
          }
        }
      }
    };

    this.completionTrendChart = new Chart(this.completionTrendCanvas.nativeElement, config);
  }

  private createDefectDistributionChart(): void {
    if (this.defectDistributionChart) {
      this.defectDistributionChart.destroy();
    }

    // TODO: Replace with real defect distribution data from API
    // Backend needs to provide defect counts grouped by priority (Critical, High, Medium, Low)
    const config: ChartConfiguration = {
      type: 'doughnut',
      data: {
        labels: ['Critical', 'High', 'Medium', 'Low'],
        datasets: [{
          data: [5, 12, 18, 8],
          backgroundColor: [
            '#ef4444', // Red for Critical
            '#f97316', // Orange for High
            '#eab308', // Yellow for Medium
            '#22c55e'  // Green for Low
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

    this.defectDistributionChart = new Chart(this.defectDistributionCanvas.nativeElement, config);
  }

  private createSitePerformanceChart(): void {
    if (this.sitePerformanceChart) {
      this.sitePerformanceChart.destroy();
    }

    // Uses real site data from API metrics.site_details
    // Fallback to mock data if API data is not available
    const siteNames = this.metrics?.site_details.slice(0, 5).map(s => s.site_name) ||
                      ['Site A', 'Site B', 'Site C', 'Site D', 'Site E'];
    const completionRates = this.metrics?.site_details.slice(0, 5).map(s => s.completion_rate) ||
                            [85, 78, 92, 65, 88];

    const config: ChartConfiguration = {
      type: 'bar',
      data: {
        labels: siteNames,
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
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: false
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            ticks: {
              callback: (value) => value + '%'
            }
          }
        }
      }
    };

    this.sitePerformanceChart = new Chart(this.sitePerformanceCanvas.nativeElement, config);
  }

  ngOnDestroy(): void {
    // Clean up charts on component destruction
    if (this.completionTrendChart) {
      this.completionTrendChart.destroy();
    }
    if (this.defectDistributionChart) {
      this.defectDistributionChart.destroy();
    }
    if (this.sitePerformanceChart) {
      this.sitePerformanceChart.destroy();
    }
  }
}
