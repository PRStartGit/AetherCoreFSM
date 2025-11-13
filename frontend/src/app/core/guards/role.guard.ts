import { Injectable } from '@angular/core';
import { Router, CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot } from '@angular/router';
import { AuthService } from '../auth/auth.service';
import { UserRole } from '../models';

@Injectable({
  providedIn: 'root'
})
export class RoleGuard implements CanActivate {
  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  canActivate(
    route: ActivatedRouteSnapshot,
    state: RouterStateSnapshot
  ): boolean {
    const user = this.authService.getUser();
    const allowedRoles = route.data['roles'] as UserRole[];

    if (!user) {
      this.router.navigate(['/login']);
      return false;
    }

    if (allowedRoles && allowedRoles.includes(user.role)) {
      return true;
    }

    // Redirect to appropriate dashboard based on role
    this.redirectToDashboard(user.role);
    return false;
  }

  private redirectToDashboard(role: UserRole): void {
    switch (role) {
      case UserRole.SUPER_ADMIN:
        this.router.navigate(['/super-admin']);
        break;
      case UserRole.ORG_ADMIN:
        this.router.navigate(['/org-admin']);
        break;
      case UserRole.SITE_USER:
        this.router.navigate(['/site-user']);
        break;
      default:
        this.router.navigate(['/login']);
    }
  }
}
