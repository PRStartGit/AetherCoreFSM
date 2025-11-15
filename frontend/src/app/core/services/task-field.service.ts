import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  TaskField,
  TaskFieldCreate,
  TaskFieldBulkCreate,
  TaskFieldResponse,
  TaskFieldResponseCreate,
  TaskFieldResponseSubmission
} from '../models/monitoring.model';

@Injectable({
  providedIn: 'root'
})
export class TaskFieldService {
  private readonly API_URL = 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  // Task Fields CRUD
  getAllFields(taskId?: number): Observable<TaskField[]> {
    let params = new HttpParams();
    if (taskId) {
      params = params.set('task_id', taskId.toString());
    }
    return this.http.get<TaskField[]>(`${this.API_URL}/task-fields`, { params });
  }

  getFieldById(id: number): Observable<TaskField> {
    return this.http.get<TaskField>(`${this.API_URL}/task-fields/${id}`);
  }

  createField(field: TaskFieldCreate): Observable<TaskField> {
    return this.http.post<TaskField>(`${this.API_URL}/task-fields`, field);
  }

  createFieldsBulk(bulkData: TaskFieldBulkCreate): Observable<TaskField[]> {
    return this.http.post<TaskField[]>(`${this.API_URL}/task-fields/bulk`, bulkData);
  }

  updateField(id: number, field: Partial<TaskFieldCreate>): Observable<TaskField> {
    return this.http.put<TaskField>(`${this.API_URL}/task-fields/${id}`, field);
  }

  deleteField(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/task-fields/${id}`);
  }

  // Task Field Responses
  submitResponses(submission: TaskFieldResponseSubmission): Observable<TaskFieldResponse[]> {
    return this.http.post<TaskFieldResponse[]>(`${this.API_URL}/task-field-responses`, submission);
  }

  getResponses(checklistItemId?: number, taskFieldId?: number): Observable<TaskFieldResponse[]> {
    let params = new HttpParams();
    if (checklistItemId) {
      params = params.set('checklist_item_id', checklistItemId.toString());
    }
    if (taskFieldId) {
      params = params.set('task_field_id', taskFieldId.toString());
    }
    return this.http.get<TaskFieldResponse[]>(`${this.API_URL}/task-field-responses`, { params });
  }

  getResponseById(id: number): Observable<TaskFieldResponse> {
    return this.http.get<TaskFieldResponse>(`${this.API_URL}/task-field-responses/${id}`);
  }
}
