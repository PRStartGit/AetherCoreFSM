import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { CourseEnrollment } from '../models/training.models';

@Injectable({
  providedIn: 'root'
})
export class EnrollmentService {
  private readonly API_URL = '/api/v1/enrollments';

  constructor(private http: HttpClient) {}

  getEnrollment(id: number): Observable<CourseEnrollment> {
    return this.http.get<CourseEnrollment>(`${this.API_URL}/${id}`);
  }

  getMyEnrollments(): Observable<CourseEnrollment[]> {
    return this.http.get<CourseEnrollment[]>(`${this.API_URL}/my-courses`);
  }
}
