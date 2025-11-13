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

  updateNavigation(): void {
    if (!this.user) {
      this.navigationItems = [];
      return;
    }

    switch (this.user.role) {
      case UserRole.SUPER_ADMIN:
        this.navigationItems = [
          { label: 'Dashboard', icon: 'dashboard', route: '/super-admin' },
          { label: 'Organizations', icon: 'business', route: '/super-admin/organizations' },
          { label: 'Users', icon: 'people', route: '/super-admin/users' },
          { label: 'Sites', icon: 'location_on', route: '/super-admin/sites' },
          { label: 'Reports', icon: 'assessment', route: '/super-admin/reports' }
        ];
        break;
      case UserRole.ORG_ADMIN:
        this.navigationItems = [
          { label: 'Dashboard', icon: 'dashboard', route: '/org-admin' },
          { label: 'Sites', icon: 'location_on', route: '/org-admin/sites' },
          { label: 'Users', icon: 'people', route: '/org-admin/users' },
          { label: 'Categories', icon: 'category', route: '/org-admin/categories' },
          { label: 'Tasks', icon: 'task', route: '/org-admin/tasks' },
          { label: 'Defects', icon: 'bug_report', route: '/org-admin/defects' },
          { label: 'Reports', icon: 'assessment', route: '/org-admin/reports' }
        ];
        break;
      case UserRole.SITE_USER:
        this.navigationItems = [
          { label: 'Dashboard', icon: 'dashboard', route: '/site-user' },
          { label: 'Checklists', icon: 'checklist', route: '/site-user/checklists' },
          { label: 'Defects', icon: 'bug_report', route: '/site-user/defects' }
        ];
        break;
    }
  }

  logout(): void {
    this.authService.logout();
  }
}
