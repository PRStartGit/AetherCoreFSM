import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../models';

export interface UserCreate {
  email: string;
  password: string;
  full_name: string;
  role: string;
  organization_id?: number;
  site_ids?: number[];
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  role?: string;
  is_active?: boolean;
  site_ids?: number[];
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly API_URL = 'http://localhost:8000/api/v1/users';

  constructor(private http: HttpClient) {}

  getAll(organizationId?: number): Observable<User[]> {
    let params = new HttpParams();
    if (organizationId) {
      params = params.set('organization_id', organizationId.toString());
    }
    return this.http.get<User[]>(this.API_URL, { params });
  }

  getById(id: number): Observable<User> {
    return this.http.get<User>(`${this.API_URL}/${id}`);
  }

  create(user: UserCreate): Observable<User> {
    return this.http.post<User>(this.API_URL, user);
  }

  update(id: number, user: UserUpdate): Observable<User> {
    return this.http.put<User>(`${this.API_URL}/${id}`, user);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }
}
