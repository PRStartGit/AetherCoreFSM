import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../../core/auth/auth.service';
import { UserRole } from '../../../core/models';
import { SystemMessageService, SystemMessage } from '../../../core/services/system-message.service';

interface FaqSection {
  id: string;
  title: string;
  icon: string;
  roles: UserRole[];
  expanded: boolean;
}

@Component({
  selector: 'app-faq',
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.scss']
})
export class FaqComponent implements OnInit {
  userRole: UserRole | null = null;
  UserRole = UserRole;
  activeSection: string = 'getting-started';

  sections: FaqSection[] = [
    { id: 'system-messages', title: 'System Messages', icon: 'fa-solid fa-bullhorn', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER], expanded: false },
    { id: 'getting-started', title: 'Getting Started', icon: 'fa-solid fa-rocket', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER], expanded: true },
    { id: 'checklists', title: 'Completing Checklists', icon: 'fa-solid fa-clipboard-check', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER], expanded: false },
    { id: 'defects', title: 'Reporting Defects', icon: 'fa-solid fa-triangle-exclamation', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER], expanded: false },
    { id: 'categories', title: 'Managing Categories', icon: 'fa-solid fa-tag', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN], expanded: false },
    { id: 'tasks', title: 'Creating Tasks', icon: 'fa-solid fa-list-check', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN], expanded: false },
    { id: 'dynamic-forms', title: 'Dynamic Form Fields', icon: 'fa-solid fa-sliders', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN], expanded: false },
    { id: 'sites', title: 'Managing Sites', icon: 'fa-solid fa-location-dot', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN], expanded: false },
    { id: 'users', title: 'Managing Users', icon: 'fa-solid fa-users', roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN], expanded: false },
  ];

  systemMessages: SystemMessage[] = [];

  constructor(
    private authService: AuthService,
    private systemMessageService: SystemMessageService
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.userRole = state.user?.role || null;
    });
    this.loadSystemMessages();
  }

  loadSystemMessages(): void {
    this.systemMessageService.getMessages(true).subscribe(messages => {
      this.systemMessages = messages;
    });
  }

  canViewSection(section: FaqSection): boolean {
    if (!this.userRole) return false;
    return section.roles.includes(this.userRole);
  }

  setActiveSection(sectionId: string): void {
    this.activeSection = sectionId;
  }

  isAdmin(): boolean {
    return this.userRole === UserRole.SUPER_ADMIN || this.userRole === UserRole.ORG_ADMIN;
  }
}
