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
      org_id: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^[A-Z0-9-]+$/)]],
      contact_person: ['', [Validators.required, Validators.maxLength(100)]],
      contact_email: ['', [Validators.required, Validators.email]],
      contact_phone: [''],
      address: [''],
      subscription_tier: ['basic', Validators.required],
      custom_price_per_site: [null, [Validators.min(0)]],
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
          org_id: org.org_id,
          contact_person: org.contact_person,
          contact_email: org.contact_email,
          contact_phone: org.contact_phone,
          address: org.address,
          subscription_tier: org.subscription_tier,
          custom_price_per_site: org.custom_price_per_site,
          is_active: org.is_active
        });
        // Disable org_id editing for existing organizations
        this.organizationForm.get('org_id')?.disable();
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
    if (field?.hasError('required')) {
      const labels: {[key: string]: string} = {
        'name': 'Organization name',
        'org_id': 'Organization ID',
        'contact_person': 'Contact person',
        'contact_email': 'Contact email',
        'subscription_tier': 'Subscription tier'
      };
      return `${labels[fieldName] || fieldName} is required`;
    }
    if (field?.hasError('email')) return 'Invalid email format';
    if (field?.hasError('pattern')) return 'Organization ID must contain only uppercase letters, numbers, and hyphens (e.g., VIG001, ACME-CORP)';
    if (field?.hasError('maxlength')) return `Field is too long (max ${field.errors?.['maxlength'].requiredLength} characters)`;
    if (field?.hasError('min')) return `Value must be at least ${field.errors?.['min'].min}`;
    return '';
  }
}
