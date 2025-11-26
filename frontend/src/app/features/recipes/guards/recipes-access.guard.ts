import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map, catchError, switchMap } from 'rxjs/operators';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '../../../core/auth/auth.service';
import { UserRole } from '../../../core/models';

@Injectable({
  providedIn: 'root'
})
export class RecipesAccessGuard implements CanActivate {
  private apiUrl = '/api/v1';

  constructor(
    private authService: AuthService,
    private http: HttpClient,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    return this.authService.getCurrentUser().pipe(
      switchMap(currentUser => {
        if (!currentUser) {
          this.router.navigate(['/login']);
          return of(false);
        }

        // Super admins have automatic access to everything
        if (currentUser.role === UserRole.SUPER_ADMIN) {
          return of(true);
        }

        // Org admins have access if module is enabled for their organization
        // Regular users need "Zynthio Recipes" module access
        return this.getUserModuleAccess(currentUser.id).pipe(
          map(modules => {
            const hasAccess = modules.includes('Zynthio Recipes');
            if (!hasAccess) {
              // Redirect to recipes landing page which shows "request access" message
              this.router.navigate(['/recipes']);
            }
            return hasAccess;
          }),
          catchError(() => {
            this.router.navigate(['/recipes']);
            return of(false);
          })
        );
      }),
      catchError(() => {
        this.router.navigate(['/login']);
        return of(false);
      })
    );
  }

  private getUserModuleAccess(userId: number): Observable<string[]> {
    return this.http.get<string[]>(`${this.apiUrl}/users/${userId}/module-access`);
  }
}
