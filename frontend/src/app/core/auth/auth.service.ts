import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { tap, catchError, switchMap, map } from 'rxjs/operators';
import { Router } from '@angular/router';
import { User, LoginRequest, LoginResponse, AuthState, UserRole } from '../models';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_URL = '/api/v1';
  private readonly TOKEN_KEY = 'zynthio_token';
  private readonly USER_KEY = 'zynthio_user';

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

  login(credentials: LoginRequest): Observable<{user: User, must_change_password: boolean}> {
    return this.http.post<{access_token: string, token_type: string, must_change_password?: boolean}>(`${this.API_URL}/login`, credentials).pipe(
      tap(response => {
        // Update auth state with token immediately so interceptor can use it
        this.authStateSubject.next({
          isAuthenticated: false,
          user: null,
          token: response.access_token
        });
        localStorage.setItem(this.TOKEN_KEY, response.access_token);
      }),
      // Fetch user data after successful login
      switchMap((loginResponse) => this.getCurrentUser().pipe(
        tap(user => {
          const token = localStorage.getItem(this.TOKEN_KEY)!;
          this.setAuthState(token, user);
        }),
        // Return both user and must_change_password flag
        map(user => ({ user, must_change_password: loginResponse.must_change_password || false }))
      )),
      catchError(error => {
        console.error('Login error:', error);
        localStorage.removeItem(this.TOKEN_KEY);
        this.clearAuthState();
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

  requestPasswordReset(data: { organization_id: string; email: string }): Observable<any> {
    return this.http.post(`${this.API_URL}/auth/forgot-password`, data);
  }

  resetPassword(data: { token: string; new_password: string }): Observable<any> {
    return this.http.post(`${this.API_URL}/auth/reset-password`, data);
  }

  changePassword(data: { old_password: string; new_password: string }): Observable<any> {
    return this.http.post(`${this.API_URL}/change-password`, data);
  }

  register(data: {
    company_name: string;
    org_id: string;
    contact_person: string;
    contact_email: string;
    contact_phone?: string;
    address?: string;
    admin_first_name: string;
    admin_last_name: string;
    admin_email: string;
    admin_password: string;
  }): Observable<any> {
    return this.http.post(`${this.API_URL}/register`, data);
  }
}
