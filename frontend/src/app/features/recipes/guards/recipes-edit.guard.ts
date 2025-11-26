import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable, of } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { AuthService } from '../../../core/auth/auth.service';
import { UserRole } from '../../../core/models';

@Injectable({
  providedIn: 'root'
})
export class RecipesEditGuard implements CanActivate {
  // CRUD roles for Recipe Book
  private readonly CRUD_ROLES = [
    'Head Chef',
    'Sous Chef',
    'General Manager',
    'Assistant Manager'
  ];

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    return this.authService.getCurrentUser().pipe(
      map(currentUser => {
        if (!currentUser) {
          this.router.navigate(['/login']);
          return false;
        }

        // Super admins and org admins always have CRUD permissions
        if (currentUser.role === UserRole.SUPER_ADMIN || currentUser.role === UserRole.ORG_ADMIN) {
          return true;
        }

        // Check if user's job role is in the CRUD roles list
        if (currentUser.job_role && currentUser.job_role.name) {
          const hasCrudAccess = this.CRUD_ROLES.includes(currentUser.job_role.name);
          if (!hasCrudAccess) {
            // Redirect to recipe list page (view-only)
            this.router.navigate(['/recipes/list']);
          }
          return hasCrudAccess;
        }

        // No job role assigned, no CRUD access
        this.router.navigate(['/recipes/list']);
        return false;
      }),
      catchError(() => {
        this.router.navigate(['/login']);
        return of(false);
      })
    );
  }
}
