import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ModuleProgress } from '../models/training.models';

export interface ModuleProgressUpdate {
  is_completed?: boolean;
  time_spent_seconds?: number;
  last_position_seconds?: number;
}

@Injectable({
  providedIn: 'root'
})
export class ModuleProgressService {
  private readonly API_URL = '/api/v1/progress';

  constructor(private http: HttpClient) {}

  getEnrollmentProgress(enrollmentId: number): Observable<ModuleProgress[]> {
    return this.http.get<ModuleProgress[]>(`${this.API_URL}/enrollments/${enrollmentId}/progress`);
  }

  updateProgress(
    enrollmentId: number,
    moduleId: number,
    update: ModuleProgressUpdate
  ): Observable<ModuleProgress> {
    return this.http.put<ModuleProgress>(
      `${this.API_URL}/enrollments/${enrollmentId}/modules/${moduleId}/progress`,
      update
    );
  }

  completeModule(
    enrollmentId: number,
    moduleId: number,
    timeSpentSeconds: number = 0
  ): Observable<ModuleProgress> {
    return this.http.post<ModuleProgress>(
      `${this.API_URL}/enrollments/${enrollmentId}/modules/${moduleId}/complete`,
      { time_spent_seconds: timeSpentSeconds }
    );
  }
}
