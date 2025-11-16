import { Component, OnInit, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ChecklistService } from '../../../core/services/checklist.service';
import { CategoryService } from '../../../core/services/category.service';
import { Checklist, ChecklistCreate, Category } from '../../../core/models/monitoring.model';
import { Site } from '../../../core/models';

@Component({
  selector: 'app-checklist-form',
  templateUrl: './checklist-form.component.html',
  styleUrls: ['./checklist-form.component.scss']
})
export class ChecklistFormComponent implements OnInit {
  checklistForm: FormGroup;
  loading = false;
  categories: Category[] = [];
  sites: Site[];

  constructor(
    private fb: FormBuilder,
    private checklistService: ChecklistService,
    private categoryService: CategoryService,
    private snackBar: MatSnackBar,
    public dialogRef: MatDialogRef<ChecklistFormComponent>,
    @Inject(MAT_DIALOG_DATA) public data: {
      checklist: Checklist | null;
      sites: Site[];
    }
  ) {
    this.sites = data.sites || [];

    this.checklistForm = this.fb.group({
      site_id: [null, Validators.required],
      category_id: [null, Validators.required],
      scheduled_date: [new Date().toISOString().split('T')[0], Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(): void {
    this.categoryService.getAll().subscribe({
      next: (categories: any[]) => {
        this.categories = categories.filter((c: any) => c.is_active);
      },
      error: (error: any) => {
        console.error('Error loading categories:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.checklistForm.invalid) {
      return;
    }

    this.loading = true;
    const formValue: ChecklistCreate = this.checklistForm.getRawValue();

    this.checklistService.create(formValue).subscribe({
      next: () => {
        this.snackBar.open('Checklist created successfully', 'Close', { duration: 3000 });
        this.dialogRef.close(true);
      },
      error: (error: any) => {
        console.error('Error creating checklist:', error);
        this.snackBar.open('Failed to create checklist', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  onCancel(): void {
    this.dialogRef.close(false);
  }
}
