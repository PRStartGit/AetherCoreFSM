import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReportService {
  private apiUrl = '/api/v1/reports';

  constructor(private http: HttpClient) {}

  /**
   * Download a PDF report for a single day's checklists
   */
  downloadDailyReport(siteId: number, date: string): Observable<Blob> {
    const params = new HttpParams()
      .set('site_id', siteId.toString())
      .set('report_date', date);

    return this.http.get(`${this.apiUrl}/pdf/checklist`, {
      params,
      responseType: 'blob'
    });
  }

  /**
   * Download PDF reports for a date range (returns ZIP if multiple days)
   */
  downloadRangeReport(siteId: number, startDate: string, endDate: string): Observable<Blob> {
    const params = new HttpParams()
      .set('site_id', siteId.toString())
      .set('start_date', startDate)
      .set('end_date', endDate);

    return this.http.get(`${this.apiUrl}/pdf/checklist/range`, {
      params,
      responseType: 'blob'
    });
  }

  /**
   * Helper method to trigger file download
   */
  downloadFile(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    link.click();
    window.URL.revokeObjectURL(url);
  }

  /**
   * Generate filename based on response content-disposition or fallback
   */
  getFilenameFromResponse(contentDisposition: string | null, fallback: string): string {
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
      if (filenameMatch && filenameMatch[1]) {
        return filenameMatch[1].replace(/['"]/g, '');
      }
    }
    return fallback;
  }
}
