import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatSelectModule } from '@angular/material/select';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RecipeService } from '../../services/recipe.service';
import { IngredientUnit } from '../../models/recipe.models';

@Component({
  selector: 'app-ingredient-units-admin',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatTableModule,
    MatButtonModule,
    MatIconModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatCardModule,
    MatSelectModule,
    MatSnackBarModule
  ],
  templateUrl: './ingredient-units-admin.component.html',
  styleUrls: ['./ingredient-units-admin.component.scss']
})
export class IngredientUnitsAdminComponent implements OnInit {
  units: IngredientUnit[] = [];
  displayedColumns: string[] = ['name', 'display_name', 'category', 'sort_order', 'actions'];
  unitForm: FormGroup;
  isEditing = false;
  editingId: number | null = null;

  categories = ['weight', 'volume', 'count', 'other'];

  constructor(
    private recipeService: RecipeService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {
    this.unitForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(50)]],
      display_name: ['', [Validators.required, Validators.maxLength(50)]],
      category: [''],
      sort_order: [0, [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    this.loadUnits();
  }

  loadUnits(): void {
    this.recipeService.getIngredientUnits().subscribe({
      next: (units) => {
        this.units = units;
      },
      error: (error) => {
        this.snackBar.open('Failed to load units', 'Close', { duration: 3000 });
        console.error('Error loading units:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.unitForm.invalid) {
      return;
    }

    const unitData = this.unitForm.value;

    if (this.isEditing && this.editingId) {
      this.recipeService.updateIngredientUnit(this.editingId, unitData).subscribe({
        next: () => {
          this.snackBar.open('Unit updated successfully', 'Close', { duration: 3000 });
          this.loadUnits();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open('Failed to update unit', 'Close', { duration: 3000 });
          console.error('Error updating unit:', error);
        }
      });
    } else {
      this.recipeService.createIngredientUnit(unitData).subscribe({
        next: () => {
          this.snackBar.open('Unit created successfully', 'Close', { duration: 3000 });
          this.loadUnits();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open('Failed to create unit', 'Close', { duration: 3000 });
          console.error('Error creating unit:', error);
        }
      });
    }
  }

  editUnit(unit: IngredientUnit): void {
    this.isEditing = true;
    this.editingId = unit.id;
    this.unitForm.patchValue({
      name: unit.name,
      display_name: unit.display_name,
      category: unit.category,
      sort_order: unit.sort_order
    });
  }

  deleteUnit(unit: IngredientUnit): void {
    if (!confirm(`Are you sure you want to delete "${unit.display_name}"?`)) {
      return;
    }

    this.recipeService.deleteIngredientUnit(unit.id).subscribe({
      next: () => {
        this.snackBar.open('Unit deleted successfully', 'Close', { duration: 3000 });
        this.loadUnits();
      },
      error: (error) => {
        this.snackBar.open('Failed to delete unit', 'Close', { duration: 3000 });
        console.error('Error deleting unit:', error);
      }
    });
  }

  resetForm(): void {
    this.unitForm.reset({ sort_order: 0, category: '' });
    this.isEditing = false;
    this.editingId = null;
  }
}
