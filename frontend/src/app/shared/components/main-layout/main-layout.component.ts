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

    // Flat icon SVGs
    const icons = {
      dashboard: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>',
      organizations: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>',
      users: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>',
      sites: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>',
      category: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path></svg>',
      tasks: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>',
      checklist: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>',
      defects: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>',
      profile: '<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>'
    };

    switch (this.user.role) {
      case UserRole.SUPER_ADMIN:
        this.navigationItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/super-admin' },
          { label: 'Organizations', icon: icons.organizations, route: '/super-admin/organizations' },
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
