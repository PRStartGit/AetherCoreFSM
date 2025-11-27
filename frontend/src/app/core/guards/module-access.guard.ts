import { Injectable, inject } from '@angular/core';
import { CanActivate, CanActivateFn, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map, catchError, switchMap, take } from 'rxjs/operators';
import { AuthService } from '../auth/auth.service';
import { SubscriptionService, ModuleAccessCheck } from '../services/subscription.service';
import { UserRole } from '../models';

@Injectable({
  providedIn: 'root'
})
export class ModuleAccessGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private subscriptionService: SubscriptionService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    // Get module code from route data
    const moduleCode = route.data['moduleCode'] as string;
    if (!moduleCode) {
      console.error('ModuleAccessGuard: No moduleCode specified in route data');
      return of(true); // Allow access if no module specified
    }

    return this.authService.getCurrentUser().pipe(
      switchMap(currentUser => {
        if (!currentUser) {
          this.router.navigate(['/login']);
          return of(false);
        }

        // Super admins always have access
        if (currentUser.role === UserRole.SUPER_ADMIN) {
          return of(true);
        }

        // Check module access via subscription service
        return this.subscriptionService.checkModuleAccess(moduleCode).pipe(
          map((response: ModuleAccessCheck) => {
            if (response.has_access) {
              return true;
            }

            // Store the attempted module for the upgrade page
            sessionStorage.setItem('upgrade_requested_module', moduleCode);
            sessionStorage.setItem('upgrade_module_name', response.module_name || moduleCode);

            // Redirect to upgrade page
            this.router.navigate(['/upgrade'], {
              queryParams: { module: moduleCode }
            });
            return false;
          }),
          catchError(error => {
            console.error('Module access check failed:', error);
            // On error, allow access (fail-open for better UX during development)
            // In production, you might want to fail-closed
            return of(true);
          })
        );
      }),
      catchError(() => {
        this.router.navigate(['/login']);
        return of(false);
      })
    );
  }
}

/**
 * Functional guard factory for module access checks.
 * Usage in route config:
 * {
 *   path: 'recipes',
 *   canActivate: [moduleAccessGuard('recipes')]
 * }
 */
export function moduleAccessGuard(moduleCode: string): CanActivateFn {
  return (route: ActivatedRouteSnapshot, state: RouterStateSnapshot) => {
    const authService = inject(AuthService);
    const subscriptionService = inject(SubscriptionService);
    const router = inject(Router);

    return authService.getCurrentUser().pipe(
      take(1),
      switchMap(currentUser => {
        if (!currentUser) {
          router.navigate(['/login']);
          return of(false);
        }

        // Super admins always have access
        if (currentUser.role === UserRole.SUPER_ADMIN) {
          return of(true);
        }

        return subscriptionService.checkModuleAccess(moduleCode).pipe(
          map((response: ModuleAccessCheck) => {
            if (response.has_access) {
              return true;
            }

            sessionStorage.setItem('upgrade_requested_module', moduleCode);
            sessionStorage.setItem('upgrade_module_name', response.module_name || moduleCode);

            router.navigate(['/upgrade'], {
              queryParams: { module: moduleCode }
            });
            return false;
          }),
          catchError(() => of(true)) // Fail-open
        );
      }),
      catchError(() => {
        router.navigate(['/login']);
        return of(false);
      })
    );
  };
}
