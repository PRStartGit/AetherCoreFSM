import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { OrganizationService } from '../../../../core/services/organization.service';
import { Organization, OrganizationCreate, OrganizationUpdate } from '../../../../core/models';

@Component({
  selector: 'app-organization-form',
  templateUrl: './organization-form.component.html',
  styleUrls: ['./organization-form.component.scss']
})
export class OrganizationFormComponent implements OnInit {
  organizationForm: FormGroup;
  isEditMode = false;
  organizationId?: number;
  loading = false;
  error: string | null = null;

  subscriptionTiers = ['free', 'basic', 'professional', 'enterprise'];

  constructor(
    private fb: FormBuilder,
    private organizationService: OrganizationService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.organizationForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      slug: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[a-z0-9-]+$/)]],
      contact_email: ['', [Validators.required, Validators.email]],
      subscription_tier: ['free', Validators.required],
      max_sites: [10, [Validators.required, Validators.min(1)]],
      is_active: [true]
    });
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.isEditMode = true;
      this.organizationId = +id;
      this.loadOrganization();
    }
  }

  loadOrganization(): void {
    if (!this.organizationId) return;

    this.loading = true;
    this.organizationService.getById(this.organizationId).subscribe({
      next: (org) => {
        this.organizationForm.patchValue({
          name: org.name,
          slug: org.slug,
          contact_email: org.contact_email,
          subscription_tier: org.subscription_tier,
          max_sites: org.max_sites,
          is_active: org.is_active
        });
        // Disable slug editing for existing organizations
        this.organizationForm.get('slug')?.disable();
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load organization';
        this.loading = false;
        console.error('Error loading organization:', err);
      }
    });
  }

  onSubmit(): void {
    if (this.organizationForm.invalid) {
      this.organizationForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.error = null;

    if (this.isEditMode && this.organizationId) {
      const updateData: OrganizationUpdate = this.organizationForm.value;
      this.organizationService.update(this.organizationId, updateData).subscribe({
        next: () => {
          this.router.navigate(['/super-admin/organizations']);
        },
        error: (err) => {
          this.error = 'Failed to update organization';
          this.loading = false;
          console.error('Error updating organization:', err);
        }
      });
    } else {
      const createData: OrganizationCreate = this.organizationForm.value;
      this.organizationService.create(createData).subscribe({
        next: () => {
          this.router.navigate(['/super-admin/organizations']);
        },
        error: (err) => {
          this.error = 'Failed to create organization';
          this.loading = false;
          console.error('Error creating organization:', err);
        }
      });
    }
  }

  cancel(): void {
    this.router.navigate(['/super-admin/organizations']);
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.organizationForm.get(fieldName);
    return !!(field && field.invalid && field.touched);
  }

  getFieldError(fieldName: string): string {
    const field = this.organizationForm.get(fieldName);
    if (field?.hasError('required')) return `${fieldName} is required`;
    if (field?.hasError('email')) return 'Invalid email format';
    if (field?.hasError('pattern')) return 'Slug must contain only lowercase letters, numbers, and hyphens';
    if (field?.hasError('maxlength')) return `${fieldName} is too long`;
    if (field?.hasError('min')) return `${fieldName} must be at least 1`;
    return '';
  }
}
