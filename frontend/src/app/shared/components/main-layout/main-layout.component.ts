import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthService } from '../../../core/auth/auth.service';
import { User, UserRole } from '../../../core/models';
import { Router } from '@angular/router';
import { SystemMessageService, SystemMessage } from '../../../core/services/system-message.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-main-layout',
  templateUrl: './main-layout.component.html',
  styleUrls: ['./main-layout.component.css']
})
export class MainLayoutComponent implements OnInit, OnDestroy {
  user: User | null = null;
  UserRole = UserRole;
  sidenavOpened = true;
  isMobileMenuOpen = false;
  sidebarCollapsed = false;
  showBroadcastModal = false;
  showNotifications = false;
  showProfileDropdown = false;
  notifications: SystemMessage[] = [];
  unreadCount = 0;
  private subscription?: Subscription;

  navigationItems: any[] = [];

  constructor(
    public authService: AuthService,
    private router: Router,
    private systemMessageService: SystemMessageService
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.user = state.user;
      this.updateNavigation();
      if (this.user) {
        this.loadNotifications();
      }
    });
    this.subscription = this.systemMessageService.messages$.subscribe(messages => {
      this.notifications = messages;
      this.unreadCount = messages.length;
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  loadNotifications(): void {
    this.systemMessageService.loadMessages();
  }

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }

  toggleSidebar(): void {
    this.sidebarCollapsed = !this.sidebarCollapsed;
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
          { label: 'Users', icon: icons.users, route: '/super-admin/users' },
          { label: 'Promo Settings', icon: 'fa-solid fa-percent', route: '/super-admin/promotions' },
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

  canBroadcast(): boolean {
    return this.user?.role === UserRole.SUPER_ADMIN || this.user?.role === UserRole.ORG_ADMIN;
  }

  openBroadcastModal(): void {
    this.showBroadcastModal = true;
  }

  closeBroadcastModal(): void {
    this.showBroadcastModal = false;
  }

  toggleNotifications(): void {
    this.showNotifications = !this.showNotifications;
    this.showProfileDropdown = false; // Close profile dropdown when opening notifications
  }

  toggleProfileDropdown(): void {
    this.showProfileDropdown = !this.showProfileDropdown;
    this.showNotifications = false; // Close notifications when opening profile dropdown
  }

  dismissNotification(id: number): void {
    this.systemMessageService.dismissMessage(id).subscribe(() => {
      this.loadNotifications();
    });
  }
}
