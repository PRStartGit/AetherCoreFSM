import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
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
  postcodeLookupLoading = false;
  postcodeLookupError: string | null = null;
  postcode: string = '';
  addressList: any[] = [];
  selectedAddressIndex: number | null = null;

  subscriptionTiers = ['platform_admin', 'free', 'basic', 'professional', 'enterprise'];

  // Module management
  modules = [
    { name: 'recipes', displayName: 'Recipe Book', enabled: false },
    { name: 'Zynthio Training', displayName: 'Training Module', enabled: false }
  ];
  moduleLoading = false;
  checklistRegenerating = false;

  constructor(
    private fb: FormBuilder,
    private organizationService: OrganizationService,
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient
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
      subscription_end_date: [null],
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
          subscription_end_date: org.subscription_end_date ? org.subscription_end_date.split('T')[0] : null,
          is_active: org.is_active
        });
        // Disable org_id editing for existing organizations
        this.organizationForm.get('org_id')?.disable();
        this.loading = false;

        // Load module statuses
        this.loadModuleStatuses();
      },
      error: (err) => {
        this.error = 'Failed to load organization';
        this.loading = false;
        console.error('Error loading organization:', err);
      }
    });
  }

  loadModuleStatuses(): void {
    if (!this.organizationId) return;

    this.http.get<any[]>(`/api/v1/organizations/${this.organizationId}/modules`).subscribe({
      next: (orgModules) => {
        // Update module enabled states
        this.modules.forEach(module => {
          const orgModule = orgModules.find(om => om.module_name === module.name);
          module.enabled = orgModule ? orgModule.is_enabled : false;
        });
      },
      error: (err) => {
        console.error('Error loading module statuses:', err);
      }
    });
  }

  toggleModule(module: any): void {
    if (!this.organizationId || this.moduleLoading) return;

    this.moduleLoading = true;
    const endpoint = module.enabled ? 'disable' : 'enable';

    this.http.post(`/api/v1/organizations/${this.organizationId}/modules/${module.name}/${endpoint}`, {}).subscribe({
      next: () => {
        module.enabled = !module.enabled;
        this.moduleLoading = false;
      },
      error: (err) => {
        this.error = `Failed to ${endpoint} ${module.displayName}`;
        this.moduleLoading = false;
        console.error(`Error toggling module:`, err);
      }
    });
  }

  grantModuleToAllUsers(module: any): void {
    if (!this.organizationId || this.moduleLoading) return;

    const confirmed = confirm(`Are you sure you want to grant ${module.displayName} access to ALL users in this organization?`);
    if (!confirmed) return;

    this.moduleLoading = true;

    this.http.post(`/api/v1/organizations/${this.organizationId}/modules/${module.name}/grant-all`, {}).subscribe({
      next: (response: any) => {
        this.moduleLoading = false;
        alert(`Successfully granted ${module.displayName} access to ${response.users_granted} users`);
      },
      error: (err) => {
        this.error = `Failed to grant ${module.displayName} access to all users`;
        this.moduleLoading = false;
        console.error('Error granting module to all users:', err);
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

  lookupPostcode(): void {
    if (!this.postcode || this.postcode.trim() === '') {
      this.postcodeLookupError = 'Please enter a postcode';
      return;
    }

    this.postcodeLookupLoading = true;
    this.postcodeLookupError = null;
    this.addressList = [];
    this.selectedAddressIndex = null;

    const cleanedPostcode = this.postcode.replace(/\s/g, '');

    this.http.get<any>(`/api/v1/utils/postcode-lookup/${cleanedPostcode}`).subscribe({
      next: (response) => {
        if (response.status === 200 && response.addresses && response.addresses.length > 0) {
          this.addressList = response.addresses;

          // Auto-select if only one address
          if (this.addressList.length === 1) {
            this.selectAddress(0);
          }
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

  selectAddress(index: number): void {
    this.selectedAddressIndex = index;
    const addr = this.addressList[index];

    // Build full address string
    const parts = [addr.line_1, addr.line_2, addr.line_3, addr.town_or_city, addr.county, addr.postcode, addr.country]
      .filter(l => l && l.trim());
    const address = parts.join(', ');

    this.organizationForm.patchValue({ address });
  }

  getAddressDisplay(addr: any): string {
    if (addr.formatted && addr.formatted.length > 0) {
      return addr.formatted.filter((l: string) => l && l.trim()).join(', ');
    }
    const parts = [addr.line_1, addr.line_2, addr.town_or_city].filter(l => l && l.trim());
    return parts.join(', ');
  }

  regenerateChecklists(): void {
    if (!this.organizationId || this.checklistRegenerating) return;

    const confirmed = confirm('Are you sure you want to regenerate all checklists for this organization? This will create missing checklists for all active sites.');
    if (!confirmed) return;

    this.checklistRegenerating = true;

    this.http.post<any>(`/api/v1/organizations/${this.organizationId}/regenerate-checklists`, {}).subscribe({
      next: (response) => {
        this.checklistRegenerating = false;
        alert(`Successfully regenerated checklists!\n\nCreated: ${response.created}\nSkipped: ${response.skipped}\nSites Processed: ${response.sites_processed}`);
      },
      error: (err) => {
        this.checklistRegenerating = false;
        this.error = 'Failed to regenerate checklists';
        console.error('Error regenerating checklists:', err);
        alert('Failed to regenerate checklists. Please try again.');
      }
    });
  }
}
