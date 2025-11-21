import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Promotion {
  id: number;
  name: string;
  description: string | null;
  trial_days: number;
  is_active: boolean;
  created_at: string;
  updated_at: string | null;
  start_date: string | null;
  end_date: string | null;
}

export interface PromotionCreate {
  name: string;
  description?: string;
  trial_days: number;
  is_active?: boolean;
  start_date?: string;
  end_date?: string;
}

export interface PromotionUpdate {
  name?: string;
  description?: string;
  trial_days?: number;
  is_active?: boolean;
  start_date?: string;
  end_date?: string;
}

@Injectable({
  providedIn: 'root'
})
export class PromotionService {
  private apiUrl = '/api/v1/promotions';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Promotion[]> {
    return this.http.get<Promotion[]>(this.apiUrl);
  }

  getById(id: number): Observable<Promotion> {
    return this.http.get<Promotion>(`${this.apiUrl}/${id}`);
  }

  getActive(): Observable<Promotion | null> {
    return this.http.get<Promotion | null>(`${this.apiUrl}/active`);
  }

  create(data: PromotionCreate): Observable<Promotion> {
    return this.http.post<Promotion>(this.apiUrl, data);
  }

  update(id: number, data: PromotionUpdate): Observable<Promotion> {
    return this.http.put<Promotion>(`${this.apiUrl}/${id}`, data);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  activate(id: number): Observable<Promotion> {
    return this.http.post<Promotion>(`${this.apiUrl}/${id}/activate`, {});
  }
}
