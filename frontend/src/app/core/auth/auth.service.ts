import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { User, LoginRequest, LoginResponse, AuthState, UserRole } from '../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_URL = 'http://localhost:8000/api/v1';
  private readonly TOKEN_KEY = 'riskproof_token';
  private readonly USER_KEY = 'riskproof_user';

  private authStateSubject = new BehaviorSubject<AuthState>({
    isAuthenticated: false,
    user: null,
    token: null
  });

  public authState$ = this.authStateSubject.asObservable();

  constructor(
    private http: HttpClient,
    private router: Router
  ) {
    this.initializeAuthState();
  }

  private initializeAuthState(): void {
    const token = localStorage.getItem(this.TOKEN_KEY);
    const userJson = localStorage.getItem(this.USER_KEY);

    if (token && userJson) {
      try {
        const user = JSON.parse(userJson);
        this.authStateSubject.next({
          isAuthenticated: true,
          user,
          token
        });
      } catch (e) {
        this.clearAuthState();
      }
    }
  }

  login(credentials: LoginRequest): Observable<LoginResponse> {
    const formData = new URLSearchParams();
    formData.append('username', credentials.email);
    formData.append('password', credentials.password);
    formData.append('organization_id', credentials.organization_id);

    return this.http.post<LoginResponse>(`${this.API_URL}/login`, formData.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).pipe(
      tap(response => {
        this.setAuthState(response.access_token, response.user);
      }),
      catchError(error => {
        console.error('Login error:', error);
        return throwError(() => error);
      })
    );
  }

  logout(): void {
    this.http.post(`${this.API_URL}/logout`, {}).subscribe({
      complete: () => {
        this.clearAuthState();
        this.router.navigate(['/login']);
      },
      error: () => {
        this.clearAuthState();
        this.router.navigate(['/login']);
      }
    });
  }

  getCurrentUser(): Observable<User> {
    return this.http.get<User>(`${this.API_URL}/me`).pipe(
      tap(user => {
        const currentState = this.authStateSubject.value;
        if (currentState.token) {
          this.setAuthState(currentState.token, user);
        }
      })
    );
  }

  private setAuthState(token: string, user: User): void {
    localStorage.setItem(this.TOKEN_KEY, token);
    localStorage.setItem(this.USER_KEY, JSON.stringify(user));

    this.authStateSubject.next({
      isAuthenticated: true,
      user,
      token
    });
  }

  private clearAuthState(): void {
    localStorage.removeItem(this.TOKEN_KEY);
    localStorage.removeItem(this.USER_KEY);

    this.authStateSubject.next({
      isAuthenticated: false,
      user: null,
      token: null
    });
  }

  getToken(): string | null {
    return this.authStateSubject.value.token;
  }

  getUser(): User | null {
    return this.authStateSubject.value.user;
  }

  isAuthenticated(): boolean {
    return this.authStateSubject.value.isAuthenticated;
  }

  hasRole(role: UserRole): boolean {
    const user = this.getUser();
    return user?.role === role;
  }

  isSuperAdmin(): boolean {
    return this.hasRole(UserRole.SUPER_ADMIN);
  }

  isOrgAdmin(): boolean {
    return this.hasRole(UserRole.ORG_ADMIN);
  }

  isSiteUser(): boolean {
    return this.hasRole(UserRole.SITE_USER);
  }
}
