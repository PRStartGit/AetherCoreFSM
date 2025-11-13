import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Site, SiteCreate, SiteUpdate, SiteRAGStatus } from '../models';

@Injectable({
  providedIn: 'root'
})
export class SiteService {
  private readonly API_URL = 'http://localhost:8000/api/v1/sites';

  constructor(private http: HttpClient) {}

  getAll(organizationId?: number): Observable<Site[]> {
    let params = new HttpParams();
    if (organizationId) {
      params = params.set('organization_id', organizationId.toString());
    }
    return this.http.get<Site[]>(this.API_URL, { params });
  }

  getById(id: number): Observable<Site> {
    return this.http.get<Site>(`${this.API_URL}/${id}`);
  }

  create(site: SiteCreate): Observable<Site> {
    return this.http.post<Site>(this.API_URL, site);
  }

  update(id: number, site: SiteUpdate): Observable<Site> {
    return this.http.put<Site>(`${this.API_URL}/${id}`, site);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }

  getRAGStatus(id: number): Observable<SiteRAGStatus> {
    return this.http.get<SiteRAGStatus>(`${this.API_URL}/${id}/rag-status`);
  }
}
