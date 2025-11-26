import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Course, CourseCreate, CourseUpdate } from '../models/training.models';

@Injectable({
  providedIn: 'root'
})
export class CourseService {
  private readonly API_URL = '/api/v1/courses';

  constructor(private http: HttpClient) {}

  getCourses(): Observable<Course[]> {
    return this.http.get<Course[]>(this.API_URL);
  }

  getCourse(id: number): Observable<Course> {
    return this.http.get<Course>(`${this.API_URL}/${id}`);
  }

  createCourse(course: CourseCreate): Observable<Course> {
    return this.http.post<Course>(this.API_URL, course);
  }

  updateCourse(id: number, course: CourseUpdate): Observable<Course> {
    return this.http.put<Course>(`${this.API_URL}/${id}`, course);
  }

  deleteCourse(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }
}
