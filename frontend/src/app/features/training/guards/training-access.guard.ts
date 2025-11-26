import { Injectable } from '@angular/core';
import { CanActivate, Router, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { AuthService } from '../../../core/auth/auth.service';
import { TrainingService } from '../services/training.service';
import { UserRole } from '../../../core/models';

@Injectable({
  providedIn: 'root'
})
export class TrainingAccessGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private trainingService: TrainingService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): Observable<boolean> {
    const currentUser = this.authService.getCurrentUser();

    if (!currentUser) {
      this.router.navigate(['/login']);
      return of(false);
    }

    // Super admins have automatic access to everything
    if (currentUser.role === UserRole.SUPER_ADMIN) {
      return of(true);
    }

    // Check if user has TRAINING module access
    return this.trainingService.getUserModuleAccess(currentUser.id).pipe(
      map(modules => {
        const hasAccess = modules.includes('TRAINING');
        if (!hasAccess) {
          // Redirect to training landing page which shows "request access" message
          this.router.navigate(['/training']);
        }
        return hasAccess;
      }),
      catchError(() => {
        this.router.navigate(['/training']);
        return of(false);
      })
    );
  }
}
