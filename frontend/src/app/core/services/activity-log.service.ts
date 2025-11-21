import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ActivityLog {
  id: number;
  log_type: string;
  message: string;
  details?: string;
  user_email?: string;
  organization_name?: string;
  ip_address?: string;
  created_at: string;
}

export interface LogsResponse {
  logs: ActivityLog[];
  total: number;
}

@Injectable({
  providedIn: 'root'
})
export class ActivityLogService {
  private baseUrl = '/api/v1/logs';

  constructor(private http: HttpClient) {}

  getTaskCompletions(days: number = 30, limit: number = 100, offset: number = 0): Observable<LogsResponse> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    return this.http.get<LogsResponse>(`${this.baseUrl}/task-completions`, { params });
  }

  getLogins(days: number = 30, limit: number = 100, offset: number = 0): Observable<LogsResponse> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    return this.http.get<LogsResponse>(`${this.baseUrl}/logins`, { params });
  }

  getRegistrations(days: number = 30, limit: number = 100, offset: number = 0): Observable<LogsResponse> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    return this.http.get<LogsResponse>(`${this.baseUrl}/registrations`, { params });
  }

  getErrors(days: number = 30, limit: number = 100, offset: number = 0): Observable<LogsResponse> {
    const params = new HttpParams()
      .set('days', days.toString())
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    return this.http.get<LogsResponse>(`${this.baseUrl}/errors`, { params });
  }
}
