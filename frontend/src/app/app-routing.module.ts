import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './core/auth/login/login.component';
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
// import { DefectListComponent } from './features/defects/defect-list/defect-list.component';
import { OrganizationListComponent } from './features/super-admin/organizations/organization-list/organization-list.component';
import { OrganizationFormComponent } from './features/super-admin/organizations/organization-form/organization-form.component';
import { UserListComponent } from './features/super-admin/users/user-list/user-list.component';
import { UserFormComponent } from './features/super-admin/users/user-form/user-form.component';
// import { SiteListComponent } from './features/super-admin/sites/site-list/site-list.component';
// import { ReportsComponent } from './features/super-admin/reports/reports.component';
import { SitesListComponent } from './features/org-admin/sites-list/sites-list.component';
import { SitesFormComponent } from './features/org-admin/sites-form/sites-form.component';
import { ProfileComponent } from './features/profile/profile.component';
import { LandingPageComponent } from './features/landing-page/landing-page.component';
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';
import { UserRole } from './core/models';

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
    path: 'forgot-password',
    component: ForgotPasswordComponent
  },
  {
    path: 'reset-password',
    component: ResetPasswordComponent
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
      // {
      //   path: 'super-admin/sites',
      //   component: SiteListComponent,
      //   canActivate: [RoleGuard],
      //   data: { roles: [UserRole.SUPER_ADMIN] }
      // },
      // {
      //   path: 'super-admin/reports',
      //   component: ReportsComponent,
      //   canActivate: [RoleGuard],
      //   data: { roles: [UserRole.SUPER_ADMIN] }
      // },
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
        data: { roles: [UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/sites/new',
        component: SitesFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.ORG_ADMIN] }
      },
      {
        path: 'org-admin/sites/edit/:id',
        component: SitesFormComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.ORG_ADMIN] }
      },
      {
        path: 'site-user',
        component: SiteUserDashboardComponent,
        canActivate: [RoleGuard],
        data: { roles: [UserRole.SITE_USER] }
      },
      {
        path: 'profile',
        component: ProfileComponent,
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
