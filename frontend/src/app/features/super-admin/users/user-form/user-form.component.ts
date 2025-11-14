import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { UserService, UserCreate, UserUpdate } from '../../../../core/services/user.service';
import { OrganizationService } from '../../../../core/services/organization.service';
import { SiteService } from '../../../../core/services/site.service';
import { User, Organization, Site, UserRole } from '../../../../core/models';

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
  roles = [
    { value: UserRole.SUPER_ADMIN, label: 'Super Admin' },
    { value: UserRole.ORG_ADMIN, label: 'Org Admin' },
    { value: UserRole.SITE_USER, label: 'Site User' }
  ];

  constructor(
    private fb: FormBuilder,
    private userService: UserService,
    private organizationService: OrganizationService,
    private siteService: SiteService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.userForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      full_name: ['', [Validators.required, Validators.maxLength(100)]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      role: [UserRole.SITE_USER, Validators.required],
      organization_id: [null],
      site_ids: [[]],
      is_active: [true]
    });
  }

  ngOnInit(): void {
    this.loadOrganizations();

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
    this.organizationService.getAll().subscribe({
      next: (orgs) => {
        this.organizations = orgs;
      },
      error: (err) => {
        console.error('Error loading organizations:', err);
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

  loadUser(): void {
    if (!this.userId) return;

    this.loading = true;
    this.userService.getById(this.userId).subscribe({
      next: (user) => {
        this.userForm.patchValue({
          email: user.email,
          full_name: user.full_name,
          role: user.role,
          organization_id: user.organization_id,
          site_ids: user.site_ids || [],
          is_active: user.is_active
        });

        if (user.organization_id) {
          this.loadSites(user.organization_id);
        }

        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load user';
        this.loading = false;
        console.error('Error loading user:', err);
      }
    });
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
        full_name: formValue.full_name,
        role: formValue.role,
        is_active: formValue.is_active,
        site_ids: formValue.site_ids || []
      };

      // Only include password if it was entered
      if (formValue.password) {
        updateData.password = formValue.password;
      }

      this.userService.update(this.userId, updateData).subscribe({
        next: () => {
          this.router.navigate(['/super-admin/users']);
        },
        error: (err) => {
          this.error = 'Failed to update user';
          this.loading = false;
          console.error('Error updating user:', err);
        }
      });
    } else {
      const createData: UserCreate = {
        email: formValue.email,
        password: formValue.password,
        full_name: formValue.full_name,
        role: formValue.role,
        organization_id: formValue.organization_id,
        site_ids: formValue.site_ids || [],
        is_active: formValue.is_active
      };

      this.userService.create(createData).subscribe({
        next: () => {
          this.router.navigate(['/super-admin/users']);
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
    this.router.navigate(['/super-admin/users']);
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.userForm.get(fieldName);
    return !!(field && field.invalid && field.touched);
  }

  getFieldError(fieldName: string): string {
    const field = this.userForm.get(fieldName);
    if (field?.hasError('required')) return `${fieldName} is required`;
    if (field?.hasError('email')) return 'Invalid email format';
    if (field?.hasError('minlength')) return `${fieldName} must be at least 8 characters`;
    if (field?.hasError('maxlength')) return `${fieldName} is too long`;
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
}
