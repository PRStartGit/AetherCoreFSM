import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './core/auth/login/login.component';
import { MainLayoutComponent } from './shared/components/main-layout/main-layout.component';
import { SuperAdminDashboardComponent } from './features/super-admin/super-admin-dashboard/super-admin-dashboard.component';
import { OrgAdminDashboardComponent } from './features/org-admin/org-admin-dashboard/org-admin-dashboard.component';
import { SiteUserDashboardComponent } from './features/site-user/site-user-dashboard/site-user-dashboard.component';
import { AuthGuard } from './core/guards/auth.guard';
import { RoleGuard } from './core/guards/role.guard';
import { UserRole } from './core/models';

const routes: Routes = [
  {
    path: 'login',
    component: LoginComponent
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
        path: 'org-admin',
        component: OrgAdminDashboardComponent,
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
        path: '',
        redirectTo: '/login',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '**',
    redirectTo: '/login'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
