import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { TrainingService } from '../../training/services/training.service';
import { JobRole } from '../../training/models/training.models';

@Component({
  selector: 'app-job-role-form',
  templateUrl: './job-role-form.component.html',
  styleUrls: ['./job-role-form.component.scss']
})
export class JobRoleFormComponent implements OnInit {
  jobRoleForm: FormGroup;
  isEditMode = false;
  roleId?: number;
  loading = false;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private trainingService: TrainingService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.jobRoleForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      is_system_role: [false]
    });
  }

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.isEditMode = true;
      this.roleId = +id;
      this.loadJobRole();
    }
  }

  loadJobRole(): void {
    if (!this.roleId) return;

    this.loading = true;
    this.trainingService.getJobRole(this.roleId).subscribe({
      next: (role) => {
        this.jobRoleForm.patchValue({
          name: role.name,
          is_system_role: role.is_system_role
        });
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load job role';
        this.loading = false;
        console.error('Error loading job role:', err);
      }
    });
  }

  onSubmit(): void {
    if (this.jobRoleForm.invalid) {
      this.jobRoleForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.error = null;

    const formValue = this.jobRoleForm.value;

    if (this.isEditMode && this.roleId) {
      this.trainingService.updateJobRole(this.roleId, formValue).subscribe({
        next: () => {
          this.router.navigate(['/super-admin/job-roles']);
        },
        error: (err) => {
          this.error = 'Failed to update job role';
          this.loading = false;
          console.error('Error updating job role:', err);
        }
      });
    } else {
      this.trainingService.createJobRole(formValue).subscribe({
        next: () => {
          this.router.navigate(['/super-admin/job-roles']);
        },
        error: (err) => {
          this.error = 'Failed to create job role';
          this.loading = false;
          console.error('Error creating job role:', err);
        }
      });
    }
  }

  cancel(): void {
    this.router.navigate(['/super-admin/job-roles']);
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.jobRoleForm.get(fieldName);
    return !!(field && field.invalid && field.touched);
  }

  getFieldError(fieldName: string): string {
    const field = this.jobRoleForm.get(fieldName);
    if (field?.hasError('required')) return 'Job role name is required';
    if (field?.hasError('maxlength')) return 'Job role name is too long';
    return '';
  }
}
