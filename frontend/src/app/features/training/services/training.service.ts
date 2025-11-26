import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { JobRole, UserModuleAccess, Course, CourseCreate, CourseUpdate, CourseCategory, CourseModule, CourseModuleCreate, CourseModuleUpdate, CourseEnrollment, CourseEnrollmentWithCourse, AssignCoursesRequest, EnrollmentStatus } from '../models/training.models';

@Injectable({
  providedIn: 'root'
})
export class TrainingService {
  private apiUrl = '/api/v1';

  constructor(private http: HttpClient) {}

  /**
   * Get all job roles (for dropdown)
   */
  getJobRoles(): Observable<JobRole[]> {
    return this.http.get<JobRole[]>(`${this.apiUrl}/job-roles`);
  }

  /**
   * Get all job roles including system roles (for management interface - Super Admin only)
   */
  getAllJobRoles(): Observable<JobRole[]> {
    return this.http.get<JobRole[]>(`${this.apiUrl}/job-roles/all`);
  }

  /**
   * Get a specific job role by ID
   */
  getJobRole(id: number): Observable<JobRole> {
    return this.http.get<JobRole>(`${this.apiUrl}/job-roles/${id}`);
  }

  /**
   * Create a new job role
   */
  createJobRole(jobRole: { name: string; is_system_role: boolean }): Observable<JobRole> {
    return this.http.post<JobRole>(`${this.apiUrl}/job-roles`, jobRole);
  }

  /**
   * Update a job role
   */
  updateJobRole(id: number, jobRole: { name: string; is_system_role: boolean }): Observable<JobRole> {
    return this.http.put<JobRole>(`${this.apiUrl}/job-roles/${id}`, jobRole);
  }

  /**
   * Delete a job role
   */
  deleteJobRole(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/job-roles/${id}`);
  }

  /**
   * Get user's module access
   */
  getUserModuleAccess(userId: number): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/users/${userId}/module-access`);
  }

  /**
   * Grant module access to a user
   */
  grantModuleAccess(userId: number, moduleName: string): Observable<UserModuleAccess> {
    return this.http.post<UserModuleAccess>(`${this.apiUrl}/users/${userId}/module-access`, {
      module_name: moduleName
    });
  }

  /**
   * Revoke module access from a user
   */
  revokeModuleAccess(userId: number, moduleName: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/users/${userId}/module-access/${moduleName}`);
  }

  // ========== Course Category Methods ==========
  /**
   * Get all course categories
   */
  getCourseCategories(): Observable<CourseCategory[]> {
    return this.http.get<CourseCategory[]>(`${this.apiUrl}/courses/categories`);
  }

  /**
   * Create a course category
   */
  createCourseCategory(category: Partial<CourseCategory>): Observable<CourseCategory> {
    return this.http.post<CourseCategory>(`${this.apiUrl}/courses/categories`, category);
  }

  /**
   * Update a course category
   */
  updateCourseCategory(categoryId: number, category: Partial<CourseCategory>): Observable<CourseCategory> {
    return this.http.put<CourseCategory>(`${this.apiUrl}/courses/categories/${categoryId}`, category);
  }

  /**
   * Delete a course category
   */
  deleteCourseCategory(categoryId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/courses/categories/${categoryId}`);
  }

  // ========== Course Methods ==========
  /**
   * Get all courses
   */
  getCourses(publishedOnly: boolean = false, categoryId?: number): Observable<Course[]> {
    let params = new HttpParams();
    if (publishedOnly) {
      params = params.set('published_only', 'true');
    }
    if (categoryId) {
      params = params.set('category_id', categoryId.toString());
    }
    return this.http.get<Course[]>(`${this.apiUrl}/courses`, { params });
  }

  /**
   * Get a course by ID
   */
  getCourseById(courseId: number): Observable<Course> {
    return this.http.get<Course>(`${this.apiUrl}/courses/${courseId}`);
  }

  /**
   * Create a course
   */
  createCourse(course: CourseCreate): Observable<Course> {
    return this.http.post<Course>(`${this.apiUrl}/courses`, course);
  }

  /**
   * Update a course
   */
  updateCourse(courseId: number, course: CourseUpdate): Observable<Course> {
    return this.http.put<Course>(`${this.apiUrl}/courses/${courseId}`, course);
  }

  /**
   * Delete a course
   */
  deleteCourse(courseId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/courses/${courseId}`);
  }

  // ========== Course Module Methods ==========
  /**
   * Get modules for a course
   */
  getCourseModules(courseId: number): Observable<CourseModule[]> {
    return this.http.get<CourseModule[]>(`${this.apiUrl}/courses/${courseId}/modules`);
  }

  /**
   * Create a course module
   */
  createCourseModule(courseId: number, module: CourseModuleCreate): Observable<CourseModule> {
    return this.http.post<CourseModule>(`${this.apiUrl}/courses/${courseId}/modules`, module);
  }

  /**
   * Update a course module
   */
  updateCourseModule(moduleId: number, module: CourseModuleUpdate): Observable<CourseModule> {
    return this.http.put<CourseModule>(`${this.apiUrl}/courses/modules/${moduleId}`, module);
  }

  /**
   * Delete a course module
   */
  deleteCourseModule(moduleId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/courses/modules/${moduleId}`);
  }

  /**
   * Reorder course modules
   */
  reorderCourseModules(courseId: number, moduleOrders: {[key: number]: number}): Observable<any> {
    return this.http.post(`${this.apiUrl}/courses/${courseId}/modules/reorder`, {
      module_orders: moduleOrders
    });
  }

  // ========== Course Enrollment Methods ==========
  /**
   * Get current user's course enrollments
   */
  getMyCourses(): Observable<CourseEnrollmentWithCourse[]> {
    return this.http.get<CourseEnrollmentWithCourse[]>(`${this.apiUrl}/enrollments/my-courses`);
  }

  /**
   * Get enrollments for a specific user
   */
  getUserEnrollments(userId: number): Observable<CourseEnrollment[]> {
    return this.http.get<CourseEnrollment[]>(`${this.apiUrl}/enrollments/users/${userId}`);
  }

  /**
   * Get all enrollments for a course
   */
  getCourseEnrollments(courseId: number): Observable<CourseEnrollment[]> {
    return this.http.get<CourseEnrollment[]>(`${this.apiUrl}/enrollments/courses/${courseId}`);
  }

  /**
   * Assign courses to users (bulk)
   */
  assignCourses(request: AssignCoursesRequest): Observable<CourseEnrollment[]> {
    return this.http.post<CourseEnrollment[]>(`${this.apiUrl}/enrollments/assign`, request);
  }

  /**
   * Update enrollment progress
   */
  updateEnrollment(enrollmentId: number, status: EnrollmentStatus, progressPercentage?: number): Observable<CourseEnrollment> {
    return this.http.put<CourseEnrollment>(`${this.apiUrl}/enrollments/${enrollmentId}`, {
      status,
      progress_percentage: progressPercentage
    });
  }

  /**
   * Mark enrollment as accessed
   */
  markEnrollmentAccessed(enrollmentId: number): Observable<CourseEnrollment> {
    return this.http.post<CourseEnrollment>(`${this.apiUrl}/enrollments/${enrollmentId}/access`, {});
  }

  /**
   * Delete an enrollment
   */
  deleteEnrollment(enrollmentId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/enrollments/${enrollmentId}`);
  }
}
