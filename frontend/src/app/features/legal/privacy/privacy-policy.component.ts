import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { UserRole } from '../../../core/models';

@Component({
  selector: 'app-privacy-policy',
  templateUrl: './privacy-policy.component.html'
})
export class PrivacyPolicyComponent implements OnInit {
  isLoggedIn: boolean = false;
  isMobileMenuOpen: boolean = false;

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.isLoggedIn = state.isAuthenticated;
    });
  }

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }

  navigateToDashboard(): void {
    const user = this.authService.getUser();
    if (!user) {
      this.router.navigate(['/login']);
      return;
    }

    switch (user.role) {
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

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }
}
