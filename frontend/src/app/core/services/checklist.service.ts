import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Checklist, ChecklistCreate, ChecklistItemUpdate, ChecklistStatus } from '../models';

@Injectable({
  providedIn: 'root'
})
export class ChecklistService {
  private readonly API_URL = '/api/v1/checklists';

  constructor(private http: HttpClient) {}

  getAll(
    siteId?: number,
    categoryId?: number,
    status?: ChecklistStatus,
    startDate?: string,
    endDate?: string
  ): Observable<Checklist[]> {
    let params = new HttpParams();
    if (siteId) params = params.set('site_id', siteId.toString());
    if (categoryId) params = params.set('category_id', categoryId.toString());
    if (status) params = params.set('status_filter', status);
    if (startDate) params = params.set('start_date', startDate);
    if (endDate) params = params.set('end_date', endDate);

    return this.http.get<Checklist[]>(this.API_URL, { params });
  }

  getById(id: number): Observable<Checklist> {
    return this.http.get<Checklist>(`${this.API_URL}/${id}`);
  }

  create(checklist: ChecklistCreate): Observable<Checklist> {
    return this.http.post<Checklist>(this.API_URL, checklist);
  }

  update(id: number, checklist: Partial<ChecklistCreate>): Observable<Checklist> {
    return this.http.put<Checklist>(`${this.API_URL}/${id}`, checklist);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }

  updateItem(checklistId: number, itemId: number, update: ChecklistItemUpdate): Observable<any> {
    return this.http.put(`${this.API_URL}/${checklistId}/items/${itemId}`, update);
  }
}
