import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { SuperAdminMetrics, OrgAdminMetrics, SiteUserMetrics } from '../models';

@Injectable({
  providedIn: 'root'
})
export class DashboardService {
  private readonly API_URL = '/api/v1/dashboards';

  constructor(private http: HttpClient) {}

  getSuperAdminMetrics(): Observable<SuperAdminMetrics> {
    return this.http.get<SuperAdminMetrics>(`${this.API_URL}/super-admin`);
  }

  getOrgAdminMetrics(): Observable<OrgAdminMetrics> {
    return this.http.get<OrgAdminMetrics>(`${this.API_URL}/org-admin`);
  }

  getSiteUserMetrics(): Observable<SiteUserMetrics> {
    return this.http.get<SiteUserMetrics>(`${this.API_URL}/site-user`);
  }
}
