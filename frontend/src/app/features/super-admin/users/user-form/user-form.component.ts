import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { UserService, UserCreate, UserUpdate } from '../../../../core/services/user.service';
import { AuthService } from '../../../../core/auth/auth.service';
import { OrganizationService } from '../../../../core/services/organization.service';
import { SiteService } from '../../../../core/services/site.service';
import { User, Organization, Site, UserRole } from '../../../../core/models';
import { TrainingService } from '../../../training/services/training.service';
import { JobRole } from '../../../training/models/training.models';

@Component({
  selector: 'app-user-form',
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.scss']
})
export class UserFormComponent implements OnInit {
  userForm: FormGroup;
  isEditMode = false;
  userId?: number;
  loading = false;
  error: string | null = null;

  organizations: Organization[] = [];
  sites: Site[] = [];
  jobRoles: JobRole[] = [];
  roles = [
    { value: UserRole.SUPER_ADMIN, label: 'Super Admin' },
    { value: UserRole.ORG_ADMIN, label: 'Org Admin' },
    { value: UserRole.SITE_USER, label: 'Site User' }
  ];

  // Module access management
  availableModules = [
    { name: 'Zynthio Recipes', enabled: false },
    { name: 'Zynthio Training', enabled: false }
  ];
  moduleLoading = false;

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private organizationService: OrganizationService,
    private siteService: SiteService,
    private trainingService: TrainingService,
    private router: Router,
    private route: ActivatedRoute,
    private authService: AuthService
  ) {
    this.userForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      first_name: ['', [Validators.required, Validators.maxLength(50)]],
      last_name: ['', [Validators.required, Validators.maxLength(50)]],
      password: [''],
      role: [UserRole.SITE_USER, Validators.required],
      organization_id: [null],
      site_ids: [[]],
      is_active: [true],
      job_role_id: [null],
      hire_date: [null]
    });
  }

  ngOnInit(): void {
    this.loadOrganizations();
    this.loadJobRoles();

    // For org admins, auto-set their organization and filter roles
    if (this.isOrgAdmin) {
      const currentUser = this.authService.getUser();
      if (currentUser?.organization_id) {
        this.userForm.patchValue({ organization_id: currentUser.organization_id });
        this.loadSites(currentUser.organization_id);
      }
      // Org admins cannot create super admins
      this.roles = this.roles.filter(r => r.value !== UserRole.SUPER_ADMIN);
    }

    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.isEditMode = true;
      this.userId = +id;
      this.userForm.get('password')?.clearValidators();
      this.userForm.get('password')?.updateValueAndValidity();
      this.loadUser();
    }

    // Watch role and organization changes
    this.userForm.get('role')?.valueChanges.subscribe(role => {
      this.onRoleChange(role);
    });

    this.userForm.get('organization_id')?.valueChanges.subscribe(orgId => {
      this.onOrganizationChange(orgId);
    });
  }

  loadOrganizations(): void {
    // Org admins can only see their own organization
    if (this.isOrgAdmin) {
      const currentUser = this.authService.getUser();
      if (currentUser?.organization_id) {
        // Load just the current users organization
        this.organizationService.getById(currentUser.organization_id).subscribe({
          next: (org) => {
            this.organizations = [org];
          },
          error: (err) => {
            console.error("Error loading organization:", err);
          }
        });
      }
      return;
    }

    // Super admins can see all organizations
    this.organizationService.getAll().subscribe({
      next: (orgs) => {
        this.organizations = orgs;
      },
      error: (err) => {
        console.error("Error loading organizations:", err);
      }
    });
  }

  loadSites(organizationId: number): void {
    this.siteService.getAll(organizationId).subscribe({
      next: (sites) => {
        this.sites = sites;
      },
      error: (err) => {
        console.error('Error loading sites:', err);
      }
    });
  }

  loadJobRoles(): void {
    this.trainingService.getJobRoles().subscribe({
      next: (roles) => {
        this.jobRoles = roles;
      },
      error: (err) => {
        console.error('Error loading job roles:', err);
      }
    });
  }

  loadUser(): void {
    if (!this.userId) return;

    this.loading = true;
    this.userService.getById(this.userId).subscribe({
      next: (user) => {
        this.userForm.patchValue({
          email: user.email,
          first_name: user.first_name,
          last_name: user.last_name,
          role: user.role,
          organization_id: user.organization_id,
          site_ids: user.site_ids || [],
          is_active: user.is_active,
          job_role_id: user.job_role_id,
          hire_date: user.hire_date
        });

        if (user.organization_id) {
          this.loadSites(user.organization_id);
        }

        // Load module access for this user
        this.loadUserModuleAccess();

        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load user';
        this.loading = false;
        console.error('Error loading user:', err);
      }
    });
  }

  loadUserModuleAccess(): void {
    if (!this.userId) return;

    this.userService.getUserModuleAccess(this.userId).subscribe({
      next: (modules: string[]) => {
        // Update enabled state for each module
        this.availableModules.forEach(module => {
          module.enabled = modules.includes(module.name);
        });
      },
      error: (err) => {
        console.error('Error loading user module access:', err);
      }
    });
  }

  toggleModuleAccess(module: any): void {
    if (!this.userId || this.moduleLoading) return;

    this.moduleLoading = true;

    if (module.enabled) {
      // Remove access
      this.userService.removeModuleAccess(this.userId, module.name).subscribe({
        next: () => {
          module.enabled = false;
          this.moduleLoading = false;
        },
        error: (err) => {
          this.error = `Failed to remove ${module.name} access`;
          this.moduleLoading = false;
          console.error('Error removing module access:', err);
        }
      });
    } else {
      // Grant access
      this.userService.grantModuleAccess(this.userId, module.name).subscribe({
        next: () => {
          module.enabled = true;
          this.moduleLoading = false;
        },
        error: (err) => {
          this.error = `Failed to grant ${module.name} access`;
          this.moduleLoading = false;
          console.error('Error granting module access:', err);
        }
      });
    }
  }

  onRoleChange(role: UserRole): void {
    const orgControl = this.userForm.get('organization_id');
    const sitesControl = this.userForm.get('site_ids');

    if (role === UserRole.SUPER_ADMIN) {
      // Super Admin doesn't need organization or sites
      orgControl?.clearValidators();
      orgControl?.setValue(null);
      sitesControl?.setValue([]);
    } else {
      // Org Admin and Site User need organization
      orgControl?.setValidators([Validators.required]);
    }

    orgControl?.updateValueAndValidity();
  }

  onOrganizationChange(orgId: number | null): void {
    if (orgId) {
      this.loadSites(orgId);
    } else {
      this.sites = [];
      this.userForm.get('site_ids')?.setValue([]);
    }
  }

  onSubmit(): void {
    if (this.userForm.invalid) {
      this.userForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.error = null;

    const formValue = this.userForm.value;

    if (this.isEditMode && this.userId) {
      const updateData: UserUpdate = {
        email: formValue.email,
        first_name: formValue.first_name,
        last_name: formValue.last_name,
        role: formValue.role,
        organization_id: formValue.organization_id,
        is_active: formValue.is_active,
        site_ids: formValue.site_ids || [],
        job_role_id: formValue.job_role_id,
        hire_date: formValue.hire_date
      };

      // Only include password if it was entered
      if (formValue.password) {
        updateData.password = formValue.password;
      }

      this.userService.update(this.userId, updateData).subscribe({
        next: () => {
          this.router.navigate([this.getBaseRoute()]);
        },
        error: (err) => {
          this.error = 'Failed to update user';
          this.loading = false;
          console.error('Error updating user:', err);
        }
      });
    } else {
      // Generate a random temporary password
      const tempPassword = this.generateRandomPassword();

      const createData: UserCreate = {
        email: formValue.email,
        password: tempPassword,
        first_name: formValue.first_name,
        last_name: formValue.last_name,
        role: formValue.role,
        organization_id: formValue.organization_id,
        site_ids: formValue.site_ids || [],
        is_active: formValue.is_active,
        job_role_id: formValue.job_role_id,
        hire_date: formValue.hire_date
      };

      this.userService.create(createData).subscribe({
        next: () => {
          alert('User created successfully! A password reset email will be sent to the user.');
          this.router.navigate([this.getBaseRoute()]);
        },
        error: (err) => {
          this.error = 'Failed to create user';
          this.loading = false;
          console.error('Error creating user:', err);
        }
      });
    }
  }

  cancel(): void {
    this.router.navigate([this.getBaseRoute()]);
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.userForm.get(fieldName);
    return !!(field && field.invalid && field.touched);
  }

  getFieldError(fieldName: string): string {
    const field = this.userForm.get(fieldName);
    const labels: {[key: string]: string} = {
      'first_name': 'First name',
      'last_name': 'Last name',
      'email': 'Email'
    };
    const label = labels[fieldName] || fieldName;
    if (field?.hasError('required')) return `${label} is required`;
    if (field?.hasError('email')) return 'Invalid email format';
    if (field?.hasError('minlength')) return `${label} must be at least 8 characters`;
    if (field?.hasError('maxlength')) return `${label} is too long`;
    return '';
  }

  get selectedRole(): UserRole {
    return this.userForm.get('role')?.value;
  }

  get showOrganizationField(): boolean {
    return this.selectedRole !== UserRole.SUPER_ADMIN;
  }

  get showSitesField(): boolean {
    return this.selectedRole === UserRole.SITE_USER && !!this.userForm.get('organization_id')?.value;
  }

  onSiteToggle(siteId: number, event: any): void {
    const siteIds = this.userForm.get('site_ids')?.value || [];
    if (event.target.checked) {
      if (!siteIds.includes(siteId)) {
        this.userForm.get('site_ids')?.setValue([...siteIds, siteId]);
      }
    } else {
      this.userForm.get('site_ids')?.setValue(siteIds.filter((id: number) => id !== siteId));
    }
  }

  getBaseRoute(): string {
    const currentUser = this.authService.getUser();
    return currentUser?.role === 'super_admin' ? '/super-admin/users' : '/org-admin/users';
  }

  get currentUserRole(): string {
    return this.authService.getUser()?.role || '';
  }

  get isOrgAdmin(): boolean {
    return this.currentUserRole === 'org_admin';
  }

  get isSuperAdmin(): boolean {
    return this.currentUserRole === 'super_admin';
  }

  generateRandomPassword(): string {
    // Generate a random secure password
    const length = 16;
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*';
    let password = '';
    for (let i = 0; i < length; i++) {
      password += charset.charAt(Math.floor(Math.random() * charset.length));
    }
    return password;
  }
}
