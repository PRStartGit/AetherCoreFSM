import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Organization, OrganizationCreate, OrganizationUpdate } from '../models';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  private readonly API_URL = 'http://localhost:8000/api/v1/organizations';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Organization[]> {
    return this.http.get<Organization[]>(this.API_URL);
  }

  getById(id: number): Observable<Organization> {
    return this.http.get<Organization>(`${this.API_URL}/${id}`);
  }

  create(org: OrganizationCreate): Observable<Organization> {
    return this.http.post<Organization>(this.API_URL, org);
  }

  update(id: number, org: OrganizationUpdate): Observable<Organization> {
    return this.http.put<Organization>(`${this.API_URL}/${id}`, org);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }
}
