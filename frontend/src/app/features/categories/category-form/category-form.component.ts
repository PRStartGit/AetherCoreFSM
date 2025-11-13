import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { CategoryService } from '../../../core/services/category.service';
import { AuthService } from '../../../core/auth/auth.service';
import { Category } from '../../../core/models/monitoring.model';

@Component({
  selector: 'app-category-form',
  templateUrl: './category-form.component.html',
  styleUrls: ['./category-form.component.css']
})
export class CategoryFormComponent implements OnInit {
  categoryForm: FormGroup;
  loading = false;
  isEditMode = false;

  constructor(
    private fb: FormBuilder,
    private categoryService: CategoryService,
    private authService: AuthService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<CategoryFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { category: Category | null }
  ) {
    this.isEditMode = !!data.category;

    this.categoryForm = this.fb.group({
      name: [data.category?.name || '', [Validators.required, Validators.maxLength(100)]],
      description: [data.category?.description || ''],
      is_global: [data.category?.is_global || false],
      is_active: [data.category?.is_active !== undefined ? data.category.is_active : true]
    });
  }

  ngOnInit(): void {
    // Disable is_global for non-super admins
    if (!this.isSuperAdmin()) {
      this.categoryForm.get('is_global')?.disable();
    }
  }

  onSubmit(): void {
    if (this.categoryForm.invalid) {
      return;
    }

    this.loading = true;
    const formValue = this.categoryForm.getRawValue();

    const request = this.isEditMode
      ? this.categoryService.updateCategory(this.data.category!.id, formValue)
      : this.categoryService.createCategory(formValue);

    request.subscribe({
      next: () => {
        this.snackBar.open(
          `Category ${this.isEditMode ? 'updated' : 'created'} successfully`,
          'Close',
          { duration: 3000 }
        );
        this.dialogRef.close(true);
      },
      error: (error) => {
        console.error('Error saving category:', error);
        this.snackBar.open(
          `Failed to ${this.isEditMode ? 'update' : 'create'} category`,
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

  isSuperAdmin(): boolean {
    return this.authService.isSuperAdmin();
  }
}
