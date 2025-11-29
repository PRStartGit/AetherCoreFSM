import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ReportService } from '../../services/report.service';
import { AuthService } from '../../../../core/auth/auth.service';
import { User, UserRole } from '../../../../core/models';
import { HttpClient } from '@angular/common/http';

interface Site {
  id: number;
  name: string;
  site_code: string;
}

@Component({
  selector: 'app-report-generator',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    RouterModule,
    MatSnackBarModule
  ],
  templateUrl: './report-generator.component.html',
  styleUrls: ['./report-generator.component.scss']
})
export class ReportGeneratorComponent implements OnInit {
  sites: Site[] = [];
  selectedSiteId: number | null = null;
  reportType: 'single' | 'range' = 'single';
  singleDate: string = '';
  startDate: string = '';
  endDate: string = '';
  isLoading = false;
  isGenerating = false;
  currentUser: User | null = null;

  constructor(
    private reportService: ReportService,
    private authService: AuthService,
    private http: HttpClient,
    private snackBar: MatSnackBar
  ) {
    // Set default dates to today
    const today = new Date();
    this.singleDate = this.formatDate(today);
    this.startDate = this.formatDate(today);
    this.endDate = this.formatDate(today);
  }

  ngOnInit(): void {
    this.currentUser = this.authService.getUser();
    this.loadSites();
  }

  private formatDate(date: Date): string {
    return date.toISOString().split('T')[0];
  }

  loadSites(): void {
    this.isLoading = true;
    this.http.get<Site[]>('/api/v1/sites').subscribe({
      next: (sites) => {
        // Filter sites based on user role
        if (this.currentUser?.role === UserRole.SITE_USER && this.currentUser.site_ids?.length) {
          this.sites = sites.filter(site => this.currentUser!.site_ids!.includes(site.id));
        } else {
          this.sites = sites;
        }

        // Auto-select first site if only one
        if (this.sites.length === 1) {
          this.selectedSiteId = this.sites[0].id;
        }
        this.isLoading = false;
      },
      error: (error) => {
        this.snackBar.open('Failed to load sites', 'Close', { duration: 3000 });
        console.error('Error loading sites:', error);
        this.isLoading = false;
      }
    });
  }

  getSelectedSiteName(): string {
    const site = this.sites.find(s => s.id === this.selectedSiteId);
    return site?.name || '';
  }

  canGenerate(): boolean {
    if (!this.selectedSiteId) return false;

    if (this.reportType === 'single') {
      return !!this.singleDate;
    } else {
      return !!this.startDate && !!this.endDate && this.startDate <= this.endDate;
    }
  }

  generateReport(): void {
    if (!this.canGenerate() || !this.selectedSiteId) return;

    this.isGenerating = true;

    if (this.reportType === 'single') {
      this.reportService.downloadDailyReport(this.selectedSiteId, this.singleDate).subscribe({
        next: (blob) => {
          const filename = `checklist-report-${this.singleDate}.pdf`;
          this.reportService.downloadFile(blob, filename);
          this.snackBar.open('Report downloaded successfully', 'Close', { duration: 3000 });
          this.isGenerating = false;
        },
        error: (error) => {
          console.error('Error generating report:', error);
          let message = 'Failed to generate report';
          if (error.status === 403) {
            message = 'Reporting module is not enabled for your organization';
          }
          this.snackBar.open(message, 'Close', { duration: 5000 });
          this.isGenerating = false;
        }
      });
    } else {
      this.reportService.downloadRangeReport(this.selectedSiteId, this.startDate, this.endDate).subscribe({
        next: (blob) => {
          const isZip = this.startDate !== this.endDate;
          const filename = isZip
            ? `checklist-reports-${this.startDate}-to-${this.endDate}.zip`
            : `checklist-report-${this.startDate}.pdf`;
          this.reportService.downloadFile(blob, filename);
          this.snackBar.open('Report(s) downloaded successfully', 'Close', { duration: 3000 });
          this.isGenerating = false;
        },
        error: (error) => {
          console.error('Error generating reports:', error);
          let message = 'Failed to generate reports';
          if (error.status === 403) {
            message = 'Reporting module is not enabled for your organization';
          } else if (error.status === 400) {
            message = 'Invalid date range (maximum 31 days)';
          }
          this.snackBar.open(message, 'Close', { duration: 5000 });
          this.isGenerating = false;
        }
      });
    }
  }

  getDayCount(): number {
    if (!this.startDate || !this.endDate) return 0;
    const start = new Date(this.startDate);
    const end = new Date(this.endDate);
    const diff = Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    return diff + 1;
  }
}
