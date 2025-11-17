import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category, CategoryCreate } from '../models';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private readonly API_URL = '/api/v1/categories';

  constructor(private http: HttpClient) {}

  getAll(isGlobal?: boolean, organizationId?: number): Observable<Category[]> {
    let params = new HttpParams();
    if (isGlobal !== undefined) {
      params = params.set('is_global', isGlobal.toString());
    }
    if (organizationId) {
      params = params.set('organization_id', organizationId.toString());
    }
    return this.http.get<Category[]>(this.API_URL, { params });
  }

  getById(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.API_URL}/${id}`);
  }

  create(category: CategoryCreate): Observable<Category> {
    return this.http.post<Category>(this.API_URL, category);
  }

  update(id: number, category: Partial<CategoryCreate>): Observable<Category> {
    return this.http.put<Category>(`${this.API_URL}/${id}`, category);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }
}
