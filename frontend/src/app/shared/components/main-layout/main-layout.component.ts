import { Component, OnInit, OnDestroy } from '@angular/core';
import { AuthService } from '../../../core/auth/auth.service';
import { User, UserRole } from '../../../core/models';
import { Router } from '@angular/router';
import { SystemMessageService, SystemMessage } from '../../../core/services/system-message.service';
import { NotificationService, Notification } from '../../../core/services/notification.service';
import { SubscriptionService, ModuleAccessResponse } from '../../../core/services/subscription.service';
import { Subscription } from 'rxjs';

interface NavItem {
  label: string;
  icon: string;
  route: string;
}

interface NavSection {
  label: string;
  icon: string;
  expanded: boolean;
  items: NavItem[];
}

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
  ticketNotifications: Notification[] = [];
  unreadCount = 0;
  ticketUnreadCount = 0;
  private subscription?: Subscription;
  private notificationSubscription?: Subscription;

  // Single items (like Dashboard)
  topNavItems: NavItem[] = [];

  // Collapsible sections
  navSections: NavSection[] = [];

  constructor(
    public authService: AuthService,
    private router: Router,
    private systemMessageService: SystemMessageService,
    private notificationService: NotificationService,
    private subscriptionService: SubscriptionService
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.user = state.user;
      this.updateNavigation();
      if (this.user) {
        this.loadNotifications();
        this.loadModuleAccess();
      }
    });
    this.subscription = this.systemMessageService.messages$.subscribe(messages => {
      this.notifications = messages;
      this.unreadCount = messages.length;
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
    this.notificationSubscription?.unsubscribe();
  }

  loadNotifications(): void {
    this.systemMessageService.loadMessages();
    this.loadTicketNotifications();
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

  toggleSection(section: NavSection): void {
    section.expanded = !section.expanded;
  }

  updateNavigation(): void {
    if (!this.user) {
      this.topNavItems = [];
      this.navSections = [];
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
      profile: 'fa-solid fa-user',
      promotions: 'fa-solid fa-percent',
      logs: 'fa-solid fa-clock-rotate-left',
      tickets: 'fa-solid fa-ticket',
      training: 'fa-solid fa-graduation-cap',
      recipes: 'fa-solid fa-book-open',
      reports: 'fa-solid fa-file-pdf',
      // Section icons
      userMgmt: 'fa-solid fa-users-gear',
      orgSection: 'fa-solid fa-building',
      fsm: 'fa-solid fa-utensils',
      maintenance: 'fa-solid fa-wrench',
      support: 'fa-solid fa-headset',
      cms: 'fa-solid fa-bullhorn',
      system: 'fa-solid fa-gear',
      trainingSection: 'fa-solid fa-graduation-cap',
      recipesSection: 'fa-solid fa-book-open'
    };

    switch (this.user.role) {
      case UserRole.SUPER_ADMIN:
        this.topNavItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/super-admin' },
          { label: 'Recipe Book', icon: icons.recipesSection, route: '/recipes' }
        ];
        this.navSections = [
          {
            label: 'User Management',
            icon: icons.userMgmt,
            expanded: false,
            items: [
              { label: 'Users', icon: icons.users, route: '/super-admin/users' }
            ]
          },
          {
            label: 'Organizations',
            icon: icons.orgSection,
            expanded: false,
            items: [
              { label: 'Organizations', icon: icons.organizations, route: '/super-admin/organizations' },
              { label: 'Sites', icon: icons.sites, route: '/org-admin/sites' }
            ]
          },
          {
            label: 'Food Safety Management',
            icon: icons.fsm,
            expanded: false,
            items: [
              { label: 'Categories', icon: icons.category, route: '/categories' },
              { label: 'Tasks', icon: icons.tasks, route: '/tasks' },
              { label: 'Checklists', icon: icons.checklist, route: '/checklists' },
              { label: 'Reports', icon: icons.reports, route: '/reports' }
            ]
          },
          {
            label: 'Zynthio Training',
            icon: icons.trainingSection,
            expanded: false,
            items: [
              { label: 'My Courses', icon: icons.training, route: '/training/my-courses' },
              { label: 'Course Management', icon: icons.category, route: '/training/courses' }
            ]
          },
          {
            label: 'Maintenance',
            icon: icons.maintenance,
            expanded: false,
            items: [
              { label: 'Defects', icon: icons.defects, route: '/defects' }
            ]
          },
          {
            label: 'Support',
            icon: icons.support,
            expanded: false,
            items: [
              { label: 'Tickets', icon: icons.tickets, route: '/super-admin/tickets' }
            ]
          },
          {
            label: 'Sales',
            icon: icons.cms,
            expanded: false,
            items: [
              { label: 'Promotions', icon: icons.promotions, route: '/super-admin/promotions' },
              { label: 'Subscriptions', icon: 'fa-solid fa-credit-card', route: '/super-admin/subscriptions' }
            ]
          },
          {
            label: 'Content',
            icon: 'fa-solid fa-pen-to-square',
            expanded: false,
            items: [
              { label: 'News & Blog', icon: 'fa-solid fa-newspaper', route: '/news' }
            ]
          },
          {
            label: 'System',
            icon: icons.system,
            expanded: false,
            items: [
              { label: 'Activity Logs', icon: icons.logs, route: '/super-admin/logs' }
            ]
          }
        ];
        break;
      case UserRole.ORG_ADMIN:
        this.topNavItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/org-admin' },
          { label: 'Recipe Book', icon: icons.recipesSection, route: '/recipes' }
        ];
        this.navSections = [
          {
            label: 'User Management',
            icon: icons.userMgmt,
            expanded: false,
            items: [
              { label: 'Users', icon: icons.users, route: '/org-admin/users' }
            ]
          },
          {
            label: 'Organization',
            icon: icons.orgSection,
            expanded: false,
            items: [
              { label: 'Sites', icon: icons.sites, route: '/org-admin/sites' }
            ]
          },
          {
            label: 'Food Safety Management',
            icon: icons.fsm,
            expanded: false,
            items: [
              { label: 'Categories', icon: icons.category, route: '/categories' },
              { label: 'Tasks', icon: icons.tasks, route: '/tasks' },
              { label: 'Checklists', icon: icons.checklist, route: '/checklists' },
              { label: 'Reports', icon: icons.reports, route: '/reports' }
            ]
          },
          {
            label: 'Zynthio Training',
            icon: icons.trainingSection,
            expanded: false,
            items: [
              { label: 'My Courses', icon: icons.training, route: '/training/my-courses' }
            ]
          },
          {
            label: 'Maintenance',
            icon: icons.maintenance,
            expanded: false,
            items: [
              { label: 'Defects', icon: icons.defects, route: '/defects' }
            ]
          },
          {
            label: 'Support',
            icon: icons.support,
            expanded: false,
            items: [
              { label: 'My Tickets', icon: icons.tickets, route: '/support/tickets' }
            ]
          }
        ];
        break;
      case UserRole.SITE_USER:
        this.topNavItems = [
          { label: 'Dashboard', icon: icons.dashboard, route: '/site-user' },
          { label: 'Recipe Book', icon: icons.recipesSection, route: '/recipes' }
        ];
        this.navSections = [
          {
            label: 'Food Safety Management',
            icon: icons.fsm,
            expanded: false,
            items: [
              { label: 'Checklists', icon: icons.checklist, route: '/checklists' },
              { label: 'Reports', icon: icons.reports, route: '/reports' }
            ]
          },
          {
            label: 'Zynthio Training',
            icon: icons.trainingSection,
            expanded: false,
            items: [
              { label: 'My Courses', icon: icons.training, route: '/training/my-courses' }
            ]
          },
          {
            label: 'Maintenance',
            icon: icons.maintenance,
            expanded: false,
            items: [
              { label: 'Defects', icon: icons.defects, route: '/defects' }
            ]
          },
          {
            label: 'Support',
            icon: icons.support,
            expanded: false,
            items: [
              { label: 'My Tickets', icon: icons.tickets, route: '/support/tickets' }
            ]
          }
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
    this.showProfileDropdown = false;
  }

  toggleProfileDropdown(): void {
    this.showProfileDropdown = !this.showProfileDropdown;
    this.showNotifications = false;
  }

  dismissNotification(id: number): void {
    this.systemMessageService.dismissMessage(id).subscribe(() => {
      this.loadNotifications();
    });
  }

  loadModuleAccess(): void {
    // Load module access and cache it in the subscription service
    this.subscriptionService.getMyModuleAccess().subscribe({
      error: (error: any) => {
        // Fail silently - module access will be checked on-demand
        console.warn('Failed to load module access:', error);
      }
    });
  }

  loadTicketNotifications(): void {
    this.notificationService.getNotifications(true, 10).subscribe(notifications => {
      this.ticketNotifications = notifications;
    });
    this.notificationSubscription = this.notificationService.unreadCount$.subscribe(count => {
      this.ticketUnreadCount = count;
    });
    this.notificationService.refreshUnreadCount();
  }

  dismissTicketNotification(id: number): void {
    this.notificationService.markAsRead([id]).subscribe(() => {
      this.loadTicketNotifications();
    });
  }

  navigateToTicket(notification: Notification): void {
    if (notification.related_url) {
      this.router.navigate([notification.related_url]);
      this.dismissTicketNotification(notification.id);
      this.showNotifications = false;
    }
  }
}
