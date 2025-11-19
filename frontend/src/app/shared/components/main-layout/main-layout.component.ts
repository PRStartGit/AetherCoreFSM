import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../core/auth/auth.service';
import { User, UserRole } from '../../../core/models';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.css']
})
export class MainLayoutComponent implements OnInit {
  user: User | null = null;
  UserRole = UserRole;
  sidenavOpened = true;
  isMobileMenuOpen = false;

  navigationItems: any[] = [];

  constructor(
    public authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.user = state.user;
      this.updateNavigation();
    });
  }

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }

  updateNavigation(): void {
    if (!this.user) {
      this.navigationItems = [];
      return;
    }

    // Font Awesome Icons
    const icons = {
      dashboard: 'fa-solid fa-chart-line',
      organizations: 'fa-solid fa-building',
      users: 'fa-solid fa-users',
      sites: 'fa-solid fa-location-dot',
      category: 'fa-solid fa-tag',
      tasks: 'fa-solid fa-list-check',
      checklist: 'fa-solid fa-clipboard-check',
      defects: 'fa-solid fa-triangle-exclamation',
      profile: 'fa-solid fa-user'
    };

    switch (this.user.role) {
      case UserRole.SUPER_ADMIN:
        this.navigationItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/super-admin' },
          { label: 'Organizations', icon: icons.organizations, route: '/super-admin/organizations' },
          { label: 'Sites', icon: icons.sites, route: '/org-admin/sites' },
          { label: 'Users', icon: icons.users, route: '/org-admin/users' },
          { label: 'Users', icon: icons.users, route: '/super-admin/users' },
          { label: 'Categories', icon: icons.category, route: '/categories' },
          { label: 'Tasks', icon: icons.tasks, route: '/tasks' },
          { label: 'Checklists', icon: icons.checklist, route: '/checklists' },
          { label: 'Defects', icon: icons.defects, route: '/defects' },
          { label: 'Profile', icon: icons.profile, route: '/profile' }
        ];
        break;
      case UserRole.ORG_ADMIN:
        this.navigationItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/org-admin' },
          { label: 'Sites', icon: icons.sites, route: '/org-admin/sites' },
          { label: 'Users', icon: icons.users, route: '/org-admin/users' },
          { label: 'Categories', icon: icons.category, route: '/categories' },
          { label: 'Tasks', icon: icons.tasks, route: '/tasks' },
          { label: 'Checklists', icon: icons.checklist, route: '/checklists' },
          { label: 'Defects', icon: icons.defects, route: '/defects' },
          { label: 'Profile', icon: icons.profile, route: '/profile' }
        ];
        break;
      case UserRole.SITE_USER:
        this.navigationItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/site-user' },
          { label: 'Checklists', icon: icons.checklist, route: '/checklists' },
          { label: 'Defects', icon: icons.defects, route: '/defects' },
          { label: 'Profile', icon: icons.profile, route: '/profile' }
        ];
        break;
    }
  }

  logout(): void {
    this.authService.logout();
  }
}
