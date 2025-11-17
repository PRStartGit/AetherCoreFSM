import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Task, TaskCreate, TaskAssignment } from '../models';

@Injectable({
  providedIn: 'root'
})
export class TaskService {
  private readonly API_URL = '/api/v1/tasks';

  constructor(private http: HttpClient) {}

  getAll(categoryId?: number): Observable<Task[]> {
    let params = new HttpParams();
    if (categoryId) {
      params = params.set('category_id', categoryId.toString());
    }
    return this.http.get<Task[]>(this.API_URL, { params });
  }

  getById(id: number): Observable<Task> {
    return this.http.get<Task>(`${this.API_URL}/${id}`);
  }

  create(task: TaskCreate): Observable<Task> {
    return this.http.post<Task>(this.API_URL, task);
  }

  update(id: number, task: Partial<TaskCreate>): Observable<Task> {
    return this.http.put<Task>(`${this.API_URL}/${id}`, task);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }

  assignToSites(id: number, siteIds: number[]): Observable<Task> {
    return this.http.post<Task>(`${this.API_URL}/${id}/assign`, { site_ids: siteIds });
  }
}
