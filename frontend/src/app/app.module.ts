import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

// Angular Material Modules
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatListModule } from '@angular/material/list';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatSortModule } from '@angular/material/sort';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSelectModule } from '@angular/material/select';
import { MatChipsModule } from '@angular/material/chips';
import { MatBadgeModule } from '@angular/material/badge';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatDividerModule } from '@angular/material/divider';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatTooltipModule } from '@angular/material/tooltip';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthInterceptor } from './core/auth/auth.interceptor';

// Components
import { LoginComponent } from './core/auth/login/login.component';
import { RegisterComponent } from './core/auth/register/register.component';
import { MainLayoutComponent } from './shared/components/main-layout/main-layout.component';
import { SuperAdminDashboardComponent } from './features/super-admin/super-admin-dashboard/super-admin-dashboard.component';
import { OrgAdminDashboardComponent } from './features/org-admin/org-admin-dashboard/org-admin-dashboard.component';
import { SiteUserDashboardComponent } from './features/site-user/site-user-dashboard/site-user-dashboard.component';
import { CategoryListComponent } from './features/categories/category-list/category-list.component';
import { CategoryFormComponent } from './features/categories/category-form/category-form.component';
import { TaskListComponent } from './features/tasks/task-list/task-list.component';
import { TaskFormComponent } from './features/tasks/task-form/task-form.component';
import { ChecklistListComponent } from './features/checklists/checklist-list/checklist-list.component';
import { ChecklistFormComponent } from './features/checklists/checklist-form/checklist-form.component';
import { ChecklistCompletionComponent } from './features/checklists/checklist-completion/checklist-completion.component';
// import { DefectListComponent } from './features/defects/defect-list/defect-list.component';
// import { DefectFormComponent } from './features/defects/defect-form/defect-form.component';
import { OrganizationListComponent } from './features/super-admin/organizations/organization-list/organization-list.component';
import { OrganizationFormComponent } from './features/super-admin/organizations/organization-form/organization-form.component';
import { UserListComponent } from './features/super-admin/users/user-list/user-list.component';
import { UserFormComponent } from './features/super-admin/users/user-form/user-form.component';
// import { SiteListComponent } from './features/super-admin/sites/site-list/site-list.component';
// import { SiteFormComponent } from './features/super-admin/sites/site-form/site-form.component';
// import { ReportsComponent } from './features/super-admin/reports/reports.component';
import { SitesListComponent } from './features/org-admin/sites-list/sites-list.component';
import { SitesFormComponent } from './features/org-admin/sites-form/sites-form.component';
import { ProfileComponent } from './features/profile/profile.component';
import { LandingPageComponent } from './features/landing-page/landing-page.component';
import { TaskFieldBuilderComponent } from './features/tasks/task-field-builder/task-field-builder.component';
import { DynamicTaskFormComponent } from './features/checklists/dynamic-task-form/dynamic-task-form.component';
import { TermsOfServiceComponent } from './features/legal/terms/terms-of-service.component';
import { PrivacyPolicyComponent } from './features/legal/privacy/privacy-policy.component';
import { CookiePolicyComponent } from './features/legal/cookies/cookie-policy.component';
import { PromotionListComponent } from './features/super-admin/promotions/promotion-list/promotion-list.component';
import { FaqComponent } from './features/support/faq/faq.component';
import { SystemMessageBannerComponent } from './shared/components/system-message-banner/system-message-banner.component';
import { BroadcastModalComponent } from './shared/components/broadcast-modal/broadcast-modal.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    RegisterComponent,
    MainLayoutComponent,
    SuperAdminDashboardComponent,
    OrgAdminDashboardComponent,
    SiteUserDashboardComponent,
    CategoryListComponent,
    CategoryFormComponent,
    TaskListComponent,
    TaskFormComponent,
    ChecklistListComponent,
    ChecklistFormComponent,
    ChecklistCompletionComponent,
    // DefectListComponent,
    // DefectFormComponent,
    OrganizationListComponent,
    OrganizationFormComponent,
    UserListComponent,
    UserFormComponent,
    // SiteListComponent,
    // SiteFormComponent,
    // ReportsComponent,
    SitesListComponent,
    SitesFormComponent,
    ProfileComponent,
    LandingPageComponent,
    TermsOfServiceComponent,
    PrivacyPolicyComponent,
    CookiePolicyComponent,
    PromotionListComponent,
    FaqComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    AppRoutingModule,
    // Material Modules
    MatToolbarModule,
    MatButtonModule,
    MatCardModule,
    MatInputModule,
    MatFormFieldModule,
    MatIconModule,
    MatSidenavModule,
    MatListModule,
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatProgressSpinnerModule,
    MatSnackBarModule,
    MatDialogModule,
    MatSelectModule,
    MatChipsModule,
    MatBadgeModule,
    MatMenuModule,
    MatProgressBarModule,
    MatDividerModule,
    MatCheckboxModule,
    MatTooltipModule,
    // Standalone Components
    TaskFieldBuilderComponent,
    DynamicTaskFormComponent,
    SystemMessageBannerComponent,
    BroadcastModalComponent
  ],
  providers: [
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
