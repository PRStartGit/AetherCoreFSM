import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { SiteService } from '../../../core/services/site.service';
import { AuthService } from '../../../core/auth/auth.service';
import { OrganizationService } from '../../../core/services/organization.service';
import { Site, SiteCreate, SiteUpdate, Organization, UserRole } from '../../../core/models';

@Component({
  selector: 'app-sites-form',
  templateUrl: './sites-form.component.html',
  styleUrls: ['./sites-form.component.scss']
})
export class SitesFormComponent implements OnInit {
  siteForm!: FormGroup;
  isEditMode = false;
  siteId: number | null = null;
  loading = false;
  error: string | null = null;
  submitting = false;
  organizations: Organization[] = [];
  isSuperAdmin = false;
  UserRole = UserRole;
  postcode = '';
  postcodeLookupLoading = false;
  postcodeLookupError: string | null = null;

  constructor(
    private fb: FormBuilder,
    private siteService: SiteService,
    private authService: AuthService,
    private organizationService: OrganizationService,
    private route: ActivatedRoute,
    private router: Router,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    // Check if user is Super Admin
    const currentUser = this.authService.getUser();
    this.isSuperAdmin = currentUser?.role === UserRole.SUPER_ADMIN;

    this.initializeForm();

    // Load organizations if Super Admin
    if (this.isSuperAdmin && !this.isEditMode) {
      this.loadOrganizations();
    }

    // Check if we're in edit mode
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.isEditMode = true;
        this.siteId = +params['id'];
        this.loadSite(this.siteId);
      }
    });
  }

  initializeForm(): void {
    const orgValidators = this.isSuperAdmin && !this.isEditMode ? [Validators.required] : [];

    this.siteForm = this.fb.group({
      organization_id: ['', orgValidators],
      name: ['', [Validators.required, Validators.minLength(3)]],
      site_code: ['', [Validators.required, Validators.pattern(/^[A-Z0-9-]+$/)]],
      address: ['', Validators.required],
      city: ['', Validators.required],
      postcode: ['', Validators.required],
      country: ['UK', Validators.required],
      is_active: [true],
      daily_report_enabled: [false],
      daily_report_time: ['09:00'],
      weekly_report_enabled: [false],
      weekly_report_day: [1],
      weekly_report_time: ['09:00'],
      report_recipients: ['']
    });
  }

  loadOrganizations(): void {
    this.organizationService.getAll().subscribe({
      next: (orgs) => {
        this.organizations = orgs;
      },
      error: (err) => {
        console.error('Error loading organizations:', err);
        this.error = 'Failed to load organizations';
      }
    });
  }

  loadSite(id: number): void {
    this.loading = true;
    this.error = null;

    this.siteService.getById(id).subscribe({
      next: (site) => {
        this.siteForm.patchValue({
          name: site.name,
          site_code: site.site_code,
          address: site.address,
          city: site.city,
          postcode: site.postcode,
          country: site.country,
          is_active: site.is_active,
          daily_report_enabled: site.daily_report_enabled || false,
          daily_report_time: site.daily_report_time || '09:00',
          weekly_report_enabled: site.weekly_report_enabled || false,
          weekly_report_day: site.weekly_report_day || 1,
          weekly_report_time: site.weekly_report_time || '09:00',
          report_recipients: site.report_recipients || ''
        });
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load site';
        this.loading = false;
        console.error('Error loading site:', err);
      }
    });
  }

  onSubmit(): void {
    if (this.siteForm.invalid) {
      this.siteForm.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.error = null;

    const formValue = this.siteForm.value;

    if (this.isEditMode && this.siteId) {
      // Update existing site
      const updateData: SiteUpdate = {
        name: formValue.name,
        site_code: formValue.site_code,
        address: formValue.address,
        city: formValue.city,
        postcode: formValue.postcode,
        country: formValue.country,
        is_active: formValue.is_active,
        daily_report_enabled: formValue.daily_report_enabled,
        daily_report_time: formValue.daily_report_time,
        weekly_report_enabled: formValue.weekly_report_enabled,
        weekly_report_day: formValue.weekly_report_day,
        weekly_report_time: formValue.weekly_report_time,
        report_recipients: formValue.report_recipients
      };

      this.siteService.update(this.siteId, updateData).subscribe({
        next: () => {
          this.router.navigate(['/org-admin/sites']);
        },
        error: (err) => {
          this.error = 'Failed to update site';
          this.submitting = false;
          console.error('Error updating site:', err);
        }
      });
    } else {
      // Create new site
      let organizationId: number;

      if (this.isSuperAdmin) {
        // Super Admin selects organization from dropdown
        organizationId = formValue.organization_id;
        if (!organizationId) {
          this.error = 'Please select an organization';
          this.submitting = false;
          return;
        }
      } else {
        // Org Admin uses their organization
        const currentUser = this.authService.getUser();
        if (!currentUser || !currentUser.organization_id) {
          this.error = 'Organization ID not found';
          this.submitting = false;
          return;
        }
        organizationId = currentUser.organization_id;
      }

      const createData: SiteCreate = {
        name: formValue.name,
        site_code: formValue.site_code,
        organization_id: organizationId,
        address: formValue.address,
        city: formValue.city,
        postcode: formValue.postcode,
        country: formValue.country,
        daily_report_enabled: formValue.daily_report_enabled,
        daily_report_time: formValue.daily_report_time,
        weekly_report_enabled: formValue.weekly_report_enabled,
        weekly_report_day: formValue.weekly_report_day,
        weekly_report_time: formValue.weekly_report_time,
        report_recipients: formValue.report_recipients
      };

      this.siteService.create(createData).subscribe({
        next: () => {
          this.router.navigate(['/org-admin/sites']);
        },
        error: (err) => {
          this.error = err.error?.detail || 'Failed to create site';
          this.submitting = false;
          console.error('Error creating site:', err);
        }
      });
    }
  }

  onCancel(): void {
    this.router.navigate(['/org-admin/sites']);
  }

  // Helper methods for form validation
  isFieldInvalid(fieldName: string): boolean {
    const field = this.siteForm.get(fieldName);
    return !!(field && field.invalid && (field.dirty || field.touched));
  }

  getFieldError(fieldName: string): string {
    const field = this.siteForm.get(fieldName);
    if (!field || !field.errors) return '';

    if (field.errors['required']) return 'This field is required';
    if (field.errors['minlength']) return `Minimum length is ${field.errors['minlength'].requiredLength}`;
    if (field.errors['pattern']) return 'Invalid format (use uppercase letters, numbers, and hyphens)';

    return '';
  }

  lookupPostcode(): void {
    if (!this.postcode || this.postcode.trim() === '') {
      this.postcodeLookupError = 'Please enter a postcode';
      return;
    }

    this.postcodeLookupLoading = true;
    this.postcodeLookupError = null;

    // Clean the postcode (remove spaces)
    const cleanedPostcode = this.postcode.replace(/\s/g, '');

    // Call our backend proxy endpoint (avoids CORS issues with Authorization header)
    this.http.get<any>(`/api/v1/utils/postcode-lookup/${cleanedPostcode}`).subscribe({
      next: (response) => {
        if (response.status === 200 && response.result) {
          const result = response.result;

          // Extract address components from postcode data
          const address = result.admin_ward || result.parish || '';
          const city = result.admin_district || '';
          const country = result.country || 'UK';
          const postcode = this.postcode.toUpperCase();

          // Populate the separate address fields
          this.siteForm.patchValue({
            address: address,
            city: city,
            postcode: postcode,
            country: country
          });

          this.postcodeLookupLoading = false;
        } else {
          this.postcodeLookupError = 'Postcode not found';
          this.postcodeLookupLoading = false;
        }
      },
      error: (err) => {
        this.postcodeLookupError = 'Invalid postcode or lookup failed';
        this.postcodeLookupLoading = false;
        console.error('Postcode lookup error:', err);
      }
    });
  }
}
