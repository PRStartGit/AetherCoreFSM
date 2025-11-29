import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './core/auth/login/login.component';
import { RegisterComponent } from './core/auth/register/register.component';
import { ForgotPasswordComponent } from './features/auth/forgot-password/forgot-password.component';
import { ResetPasswordComponent } from './features/auth/reset-password/reset-password.component';
import { MainLayoutComponent } from './shared/components/main-layout/main-layout.component';
import { SuperAdminDashboardComponent } from './features/super-admin/super-admin-dashboard/super-admin-dashboard.component';
import { OrgAdminDashboardComponent } from './features/org-admin/org-admin-dashboard/org-admin-dashboard.component';
import { SiteUserDashboardComponent } from './features/site-user/site-user-dashboard/site-user-dashboard.component';
import { CategoryListComponent } from './features/categories/category-list/category-list.component';
import { TaskListComponent } from './features/tasks/task-list/task-list.component';
import { ChecklistListComponent } from './features/checklists/checklist-list/checklist-list.component';
import { ChecklistCompletionComponent } from './features/checklists/checklist-completion/checklist-completion.component';
import { OrganizationListComponent } from './features/super-admin/organizations/organization-list/organization-list.component';
import { OrganizationFormComponent } from './features/super-admin/organizations/organization-form/organization-form.component';
import { UserListComponent } from './features/super-admin/users/user-list/user-list.component';
import { UserFormComponent } from './features/super-admin/users/user-form/user-form.component';
import { SitesListComponent } from './features/org-admin/sites-list/sites-list.component';
import { SitesFormComponent } from './features/org-admin/sites-form/sites-form.component';
import { ProfileComponent } from './features/profile/profile.component';
import { LandingPageComponent } from './features/landing-page/landing-page.component';
import { TermsOfServiceComponent } from './features/legal/terms/terms-of-service.component';
import { PrivacyPolicyComponent } from './features/legal/privacy/privacy-policy.component';
import { CookiePolicyComponent } from './features/legal/cookies/cookie-policy.component';
import { PromotionListComponent } from './features/super-admin/promotions/promotion-list/promotion-list.component';
import { LogsComponent } from './features/super-admin/activity-logs/logs.component';
import { ContactComponent } from './features/contact/contact.component';
import { FaqComponent } from './features/support/faq/faq.component';
import { JobRolesListComponent } from './features/super-admin/job-roles/job-roles-list.component';
import { JobRoleFormComponent } from './features/super-admin/job-roles/job-role-form.component';
import { SubscriptionSettingsComponent } from './features/super-admin/subscription-settings/subscription-settings.component';

// Ticket Components
import { TicketListComponent } from './features/support/ticket-list/ticket-list.component';
import { TicketDetailComponent } from './features/support/ticket-detail/ticket-detail.component';
import { AdminTicketListComponent } from './features/super-admin/tickets/admin-ticket-list/admin-ticket-list.component';
import { TicketSettingsComponent } from './features/super-admin/tickets/ticket-settings/ticket-settings.component';

import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';
import { UserRole } from './core/models';
import { UpgradeComponent } from './features/upgrade/upgrade.component';

// Subscription Components
import { SubscriptionSuccessComponent } from './features/subscription/subscription-success/subscription-success.component';
import { SubscriptionCancelledComponent } from './features/subscription/subscription-cancelled/subscription-cancelled.component';
import { SubscriptionUpgradeComponent } from './features/subscription/subscription-upgrade/subscription-upgrade.component';
import { SubscriptionManageComponent } from './features/subscription/subscription-manage/subscription-manage.component';

// Reports
import { ReportGeneratorComponent } from './features/reports/pages/report-generator/report-generator.component';

// Blog
import { BlogAdminComponent } from './features/blog/pages/blog-admin/blog-admin.component';

const routes: Routes = [
  {
    path: '',
    component: LandingPageComponent
  },
  {
    path: 'pricing',
    component: LandingPageComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'register',
    component: RegisterComponent
  },
  {
    path: 'forgot-password',
    component: ForgotPasswordComponent
  },
  {
    path: 'reset-password',
    component: ResetPasswordComponent
  },
  {
    path: 'terms',
    component: TermsOfServiceComponent
  },
  {
    path: 'privacy',
    component: PrivacyPolicyComponent
  },
  {
    path: 'cookies',
    component: CookiePolicyComponent
  },
  {
    path: 'contact',
    component: ContactComponent
  },
  {
    path: 'upgrade',
    component: UpgradeComponent,
    canActivate: [AuthGuard]
  },
  // Subscription Flow Routes
  {
    path: 'subscription/success',
    component: SubscriptionSuccessComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'subscription/cancelled',
    component: SubscriptionCancelledComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'subscription/upgrade',
    component: SubscriptionUpgradeComponent,
    canActivate: [AuthGuard]
  },
  {
    path: 'subscription/manage',
    component: SubscriptionManageComponent,
    canActivate: [AuthGuard]
  },
  {
    path: '',
    component: MainLayoutComponent,
    canActivate: [AuthGuard],
    children: [
      {
        path: 'super-admin',
        component: SuperAdminDashboardComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/organizations',
        component: OrganizationListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/organizations/:id',
        component: OrganizationFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/users',
        component: UserListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/users/:id',
        component: UserFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/promotions',
        component: PromotionListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/logs',
        component: LogsComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/subscriptions',
        component: SubscriptionSettingsComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      // Job Roles Management
      {
        path: 'super-admin/job-roles',
        component: JobRolesListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/job-roles/:id',
        component: JobRoleFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      // Super Admin Tickets
      {
        path: 'super-admin/tickets',
        component: AdminTicketListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      // Blog/News Admin
      {
        path: 'news',
        component: BlogAdminComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/tickets/settings',
        component: TicketSettingsComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'super-admin/tickets/:id',
        component: TicketDetailComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN] }
      },
      {
        path: 'categories',
        component: CategoryListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'tasks',
        component: TaskListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'checklists',
        component: ChecklistListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER] }
      },
      {
        path: 'checklists/:id/complete',
        component: ChecklistCompletionComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER] }
      },
      {
        path: 'reports',
        component: ReportGeneratorComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER] }
      },
      {
        path: 'defects',
        loadChildren: () => import('./features/defects/defects.module').then(m => m.DefectsModule),
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN, UserRole.SITE_USER] }
      },
      {
        path: 'org-admin',
        component: OrgAdminDashboardComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/sites',
        component: SitesListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/sites/new',
        component: SitesFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/sites/edit/:id',
        component: SitesFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/users',
        component: UserListComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/users/new',
        component: UserFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/users/:id',
        component: UserFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SUPER_ADMIN, UserRole.ORG_ADMIN] }
      },
      {
        path: 'site-user',
        canActivate: [RoleGuard],
        component: SiteUserDashboardComponent,
        data: { roles: [UserRole.SITE_USER] }
      },
      {
        path: 'profile',
        component: ProfileComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'training',
        loadChildren: () => import('./features/training/training.module').then(m => m.TrainingModule),
        canActivate: [AuthGuard]
      },
      {
        path: 'recipes',
        loadChildren: () => import('./features/recipes/recipes.module').then(m => m.RecipesModule),
        canActivate: [AuthGuard]
      },
      {
        path: 'support/faq',
        component: FaqComponent,
        canActivate: [AuthGuard]
      },
      // User Support Tickets (all logged-in users)
      {
        path: 'support/tickets',
        component: TicketListComponent,
        canActivate: [AuthGuard]
      },
      {
        path: 'support/tickets/:id',
        component: TicketDetailComponent,
        canActivate: [AuthGuard]
      }
    ]
  },
  {
    path: '**',
    redirectTo: ''
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
