import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { SiteService } from '../../../core/services/site.service';
import { AuthService } from '../../../core/auth/auth.service';
import { Site, SiteCreate, SiteUpdate } from '../../../core/models';

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

  constructor(
    private fb: FormBuilder,
    private siteService: SiteService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initializeForm();

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
    this.siteForm = this.fb.group({
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
      const currentUser = this.authService.getUser();
      if (!currentUser || !currentUser.organization_id) {
        this.error = 'Organization ID not found';
        this.submitting = false;
        return;
      }

      const createData: SiteCreate = {
        name: formValue.name,
        site_code: formValue.site_code,
        organization_id: currentUser.organization_id,
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
}
