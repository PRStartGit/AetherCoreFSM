import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Defect, DefectCreate, DefectUpdate, DefectStatus, DefectSeverity } from '../models';

@Injectable({
  providedIn: 'root'
})
export class DefectService {
  private readonly API_URL = 'http://localhost:8000/api/v1/defects';

  constructor(private http: HttpClient) {}

  getAll(
    siteId?: number,
    status?: DefectStatus,
    severity?: DefectSeverity
  ): Observable<Defect[]> {
    let params = new HttpParams();
    if (siteId) params = params.set('site_id', siteId.toString());
    if (status) params = params.set('status', status);
    if (severity) params = params.set('severity', severity);

    return this.http.get<Defect[]>(this.API_URL, { params });
  }

  getById(id: number): Observable<Defect> {
    return this.http.get<Defect>(`${this.API_URL}/${id}`);
  }

  create(defect: DefectCreate): Observable<Defect> {
    return this.http.post<Defect>(this.API_URL, defect);
  }

  update(id: number, defect: DefectUpdate): Observable<Defect> {
    return this.http.put<Defect>(`${this.API_URL}/${id}`, defect);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }

  close(id: number): Observable<Defect> {
    return this.http.post<Defect>(`${this.API_URL}/${id}/close`, {});
  }
}
