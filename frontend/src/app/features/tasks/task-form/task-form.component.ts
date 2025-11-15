import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TaskService } from '../../../core/services/task.service';
import { Task, Category } from '../../../core/models/monitoring.model';
import { Site } from '../../../core/models';

@Component({
  selector: 'app-task-form',
  templateUrl: './task-form.component.html',
  styleUrls: ['./task-form.component.scss']
})
export class TaskFormComponent implements OnInit {
  taskForm: FormGroup;
  loading = false;
  isEditMode = false;
  categories: Category[] = [];
  sites: Site[] = [];

  // Dynamic fields configuration
  showFieldBuilder = false;
  savedTaskId: number | null = null;

  constructor(
    private fb: FormBuilder,
    private taskService: TaskService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<TaskFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {
      task: Task | null;
      categories: Category[];
      sites: Site[];
    }
  ) {
    this.isEditMode = !!data.task;
    this.categories = data.categories || [];
    this.sites = data.sites || [];

    // Set savedTaskId if in edit mode
    if (this.isEditMode && data.task) {
      this.savedTaskId = data.task.id;
    }

    this.taskForm = this.fb.group({
      name: [data.task?.name || '', [Validators.required, Validators.maxLength(200)]],
      description: [data.task?.description || ''],
      category_id: [data.task?.category_id || null, Validators.required],
      order_index: [data.task?.order_index || 0],
      site_ids: [data.task?.site_ids || []],
      is_active: [data.task?.is_active !== undefined ? data.task.is_active : true],
      has_dynamic_form: [data.task?.has_dynamic_form || false]
    });
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    if (this.taskForm.invalid) {
      return;
    }

    this.loading = true;
    const formValue = this.taskForm.getRawValue();

    const request = this.isEditMode
      ? this.taskService.update(this.data.task!.id, formValue)
      : this.taskService.create(formValue);

    request.subscribe({
      next: (response: Task) => {
        this.snackBar.open(
          `Task ${this.isEditMode ? 'updated' : 'created'} successfully`,
          'Close',
          { duration: 3000 }
        );

        // If user wants dynamic fields, show the field builder
        if (formValue.has_dynamic_form) {
          this.savedTaskId = response.id;
          this.showFieldBuilder = true;
          this.loading = false;
        } else {
          this.dialogRef.close(true);
        }
      },
      error: (error: any) => {
        console.error('Error saving task:', error);
        this.snackBar.open(
          `Failed to ${this.isEditMode ? 'update' : 'create'} task`,
          'Close',
          { duration: 3000 }
        );
        this.loading = false;
      }
    });
  }

  onConfigureFields(): void {
    // If task is already saved, just show the field builder
    if (this.savedTaskId) {
      this.showFieldBuilder = true;
    } else {
      // Save the task first, then show field builder
      this.taskForm.patchValue({ has_dynamic_form: true });
      this.onSubmit();
    }
  }

  onBackToTaskForm(): void {
    this.showFieldBuilder = false;
  }

  onFieldsConfigured(): void {
    // Close dialog after fields are configured
    this.snackBar.open('Dynamic fields configured successfully', 'Close', { duration: 3000 });
    this.dialogRef.close(true);
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}
