import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TaskService } from '../../../core/services/task.service';
import { Task, Category, Site } from '../../../core/models/monitoring.model';

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
  frequencies = ['daily', 'weekly', 'monthly', 'quarterly', 'yearly'];

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

    this.taskForm = this.fb.group({
      name: [data.task?.name || '', [Validators.required, Validators.maxLength(200)]],
      description: [data.task?.description || ''],
      category_id: [data.task?.category_id || null, Validators.required],
      frequency: [data.task?.frequency || 'daily', Validators.required],
      site_ids: [data.task?.site_ids || []],
      is_active: [data.task?.is_active !== undefined ? data.task.is_active : true]
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
      ? this.taskService.updateTask(this.data.task!.id, formValue)
      : this.taskService.createTask(formValue);

    request.subscribe({
      next: () => {
        this.snackBar.open(
          `Task ${this.isEditMode ? 'updated' : 'created'} successfully`,
          'Close',
          { duration: 3000 }
        );
        this.dialogRef.close(true);
      },
      error: (error) => {
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

  onCancel(): void {
    this.dialogRef.close(false);
  }
}
