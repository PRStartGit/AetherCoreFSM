import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { User } from '../models';

export interface UserCreate {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: string;
  organization_id?: number;
  site_ids?: number[];
  is_active?: boolean;
  job_role_id?: number | null;
  hire_date?: string | null;
}

export interface UserUpdate {
  email?: string;
  first_name?: string;
  last_name?: string;
  role?: string;
  organization_id?: number;
  is_active?: boolean;
  site_ids?: number[];
  password?: string;
  job_role_id?: number | null;
  hire_date?: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly API_URL = '/api/v1/users';

  constructor(private http: HttpClient) {}

  getAll(organizationId?: number): Observable<User[]> {
    let params = new HttpParams();
    if (organizationId) {
      params = params.set('organization_id', organizationId.toString());
    }
    return this.http.get<any[]>(this.API_URL, { params }).pipe(
      map(users => users.map(user => this.transformUserResponse(user)))
    );
  }

  getById(id: number): Observable<User> {
    return this.http.get<any>(`${this.API_URL}/${id}`).pipe(
      map(user => this.transformUserResponse(user))
    );
  }

  create(user: UserCreate): Observable<User> {
    const payload: any = {
      email: user.email,
      password: user.password,
      first_name: user.first_name,
      last_name: user.last_name,
      role: user.role,
      organization_id: user.organization_id,
      site_ids: user.site_ids || [],
      is_active: user.is_active !== undefined ? user.is_active : true
    };

    if (user.job_role_id !== undefined) payload.job_role_id = user.job_role_id;
    if (user.hire_date !== undefined) payload.hire_date = user.hire_date;

    return this.http.post<any>(this.API_URL, payload).pipe(
      map(response => this.transformUserResponse(response))
    );
  }

  update(id: number, user: UserUpdate): Observable<User> {
    const payload: any = {};

    if (user.email !== undefined) payload.email = user.email;
    if (user.first_name !== undefined) payload.first_name = user.first_name;
    if (user.last_name !== undefined) payload.last_name = user.last_name;
    if (user.role !== undefined) payload.role = user.role;
    if (user.is_active !== undefined) payload.is_active = user.is_active;
    if (user.site_ids !== undefined) payload.site_ids = user.site_ids;
    if (user.password !== undefined && user.password) payload.password = user.password;
    if (user.job_role_id !== undefined) payload.job_role_id = user.job_role_id;
    if (user.hire_date !== undefined) payload.hire_date = user.hire_date;

    return this.http.put<any>(`${this.API_URL}/${id}`, payload).pipe(
      map(response => this.transformUserResponse(response))
    );
  }

  private transformUserResponse(response: any): User {
    return {
      ...response,
      first_name: response.first_name || '',
      last_name: response.last_name || '',
      full_name: response.full_name || `${response.first_name || ''} ${response.last_name || ''}`.trim()
    };
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }

  // Module Access Management
  getUserModuleAccess(userId: number): Observable<string[]> {
    return this.http.get<string[]>(`${this.API_URL}/${userId}/module-access`);
  }

  grantModuleAccess(userId: number, moduleName: string): Observable<any> {
    return this.http.post(`${this.API_URL}/${userId}/module-access`, { module_name: moduleName });
  }

  removeModuleAccess(userId: number, moduleName: string): Observable<any> {
    return this.http.delete(`${this.API_URL}/${userId}/module-access/${moduleName}`);
  }
}
