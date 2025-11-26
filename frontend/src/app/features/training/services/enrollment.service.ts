import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { CourseEnrollment } from '../models/training.models';

@Injectable({
  providedIn: 'root'
})
export class EnrollmentService {
  private apiUrl = `${environment.apiUrl}/enrollments`;

  constructor(private http: HttpClient) {}

  getEnrollment(id: number): Observable<CourseEnrollment> {
    return this.http.get<CourseEnrollment>(`${this.apiUrl}/${id}`);
  }

  getMyEnrollments(): Observable<CourseEnrollment[]> {
    return this.http.get<CourseEnrollment[]>(`${this.apiUrl}/my-courses`);
  }
}
