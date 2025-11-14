import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DefectService } from '../../../core/services/defect.service';
import { SiteService } from '../../../core/services/site.service';
import { UserService } from '../../../core/services/user.service';
import { Defect, DefectCreate, DefectUpdate, DefectSeverity, Site, User } from '../../../core/models';

@Component({
  selector: 'app-defect-form',
  templateUrl: './defect-form.component.html',
  styleUrls: ['./defect-form.component.scss']
})
export class DefectFormComponent implements OnInit {
  defectForm!: FormGroup;
  defectId: number | null = null;
  isEditMode = false;
  loading = false;
  error: string | null = null;
  sites: Site[] = [];
  users: User[] = [];

  DefectSeverity = DefectSeverity;

  constructor(
    private fb: FormBuilder,
    private defectService: DefectService,
    private siteService: SiteService,
    private userService: UserService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.loadSites();
    this.loadUsers();

    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.defectId = +id;
      this.isEditMode = true;
      this.loadDefect();
    }
  }

  initForm(): void {
    this.defectForm = this.fb.group({
      site_id: ['', Validators.required],
      title: ['', [Validators.required, Validators.maxLength(200)]],
      description: ['', Validators.required],
      severity: [DefectSeverity.MEDIUM, Validators.required],
      assigned_to: [null],
      due_date: [null]
    });
  }

  loadSites(): void {
    this.siteService.getAll().subscribe({
      next: (sites) => this.sites = sites,
      error: (err) => console.error('Error loading sites:', err)
    });
  }

  loadUsers(): void {
    this.userService.getAll().subscribe({
      next: (users) => this.users = users,
      error: (err) => console.error('Error loading users:', err)
    });
  }

  loadDefect(): void {
    if (this.defectId) {
      this.loading = true;
      this.defectService.getById(this.defectId).subscribe({
        next: (defect) => {
          this.defectForm.patchValue({
            site_id: defect.site_id,
            title: defect.title,
            description: defect.description,
            severity: defect.severity,
            assigned_to: defect.assigned_to,
            due_date: defect.due_date ? this.formatDateForInput(defect.due_date) : null
          });
          this.loading = false;
        },
        error: (err) => {
          this.error = 'Failed to load defect';
          this.loading = false;
          console.error('Error loading defect:', err);
        }
      });
    }
  }

  formatDateForInput(dateString: string): string {
    const date = new Date(dateString);
    return date.toISOString().slice(0, 16);
  }

  onSubmit(): void {
    if (this.defectForm.invalid) {
      Object.keys(this.defectForm.controls).forEach(key => {
        this.defectForm.get(key)?.markAsTouched();
      });
      return;
    }

    this.loading = true;
    this.error = null;

    const formValue = this.defectForm.value;

    if (this.isEditMode && this.defectId) {
      const updateData: DefectUpdate = {
        title: formValue.title,
        description: formValue.description,
        severity: formValue.severity,
        assigned_to: formValue.assigned_to || null,
        due_date: formValue.due_date || null
      };

      this.defectService.update(this.defectId, updateData).subscribe({
        next: () => {
          this.router.navigate(['/defects']);
        },
        error: (err) => {
          this.error = 'Failed to update defect';
          this.loading = false;
          console.error('Error updating defect:', err);
        }
      });
    } else {
      const createData: DefectCreate = {
        site_id: formValue.site_id,
        title: formValue.title,
        description: formValue.description,
        severity: formValue.severity,
        assigned_to: formValue.assigned_to || undefined,
        due_date: formValue.due_date || undefined
      };

      this.defectService.create(createData).subscribe({
        next: () => {
          this.router.navigate(['/defects']);
        },
        error: (err) => {
          this.error = 'Failed to create defect';
          this.loading = false;
          console.error('Error creating defect:', err);
        }
      });
    }
  }

  cancel(): void {
    this.router.navigate(['/defects']);
  }

  getFieldError(fieldName: string): string {
    const field = this.defectForm.get(fieldName);
    if (field?.hasError('required')) {
      return `${fieldName.replace('_', ' ')} is required`;
    }
    if (field?.hasError('maxlength')) {
      return `${fieldName.replace('_', ' ')} is too long`;
    }
    return '';
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.defectForm.get(fieldName);
    return !!(field && field.invalid && field.touched);
  }
}
