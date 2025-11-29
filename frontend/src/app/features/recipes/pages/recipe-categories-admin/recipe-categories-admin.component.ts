import { Component, OnInit } from '@angular/core';
import { CommonModule, Location } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RecipeService } from '../../services/recipe.service';
import { RecipeCategory } from '../../models/recipe.models';

@Component({
  selector: 'app-recipe-categories-admin',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatSnackBarModule
  ],
  templateUrl: './recipe-categories-admin.component.html',
  styleUrls: ['./recipe-categories-admin.component.scss']
})
export class RecipeCategoriesAdminComponent implements OnInit {
  categories: RecipeCategory[] = [];
  displayedColumns: string[] = ['name', 'sort_order', 'actions'];
  categoryForm: FormGroup;
  isEditing = false;
  editingId: number | null = null;

  constructor(
    private recipeService: RecipeService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private location: Location
  ) {
    this.categoryForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(100)]],
      sort_order: [0, [Validators.required, Validators.min(0)]]
    });
  }

  ngOnInit(): void {
    this.loadCategories();
  }

  loadCategories(): void {
    this.recipeService.getRecipeCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (error) => {
        this.snackBar.open('Failed to load categories', 'Close', { duration: 3000 });
        console.error('Error loading categories:', error);
      }
    });
  }

  onSubmit(): void {
    if (this.categoryForm.invalid) {
      return;
    }

    const categoryData = this.categoryForm.value;

    if (this.isEditing && this.editingId) {
      this.recipeService.updateRecipeCategory(this.editingId, categoryData).subscribe({
        next: () => {
          this.snackBar.open('Category updated successfully', 'Close', { duration: 3000 });
          this.loadCategories();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open('Failed to update category', 'Close', { duration: 3000 });
          console.error('Error updating category:', error);
        }
      });
    } else {
      this.recipeService.createRecipeCategory(categoryData).subscribe({
        next: () => {
          this.snackBar.open('Category created successfully', 'Close', { duration: 3000 });
          this.loadCategories();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open('Failed to create category', 'Close', { duration: 3000 });
          console.error('Error creating category:', error);
        }
      });
    }
  }

  editCategory(category: RecipeCategory): void {
    this.isEditing = true;
    this.editingId = category.id;
    this.categoryForm.patchValue({
      name: category.name,
      sort_order: category.sort_order
    });
  }

  deleteCategory(category: RecipeCategory): void {
    if (!confirm(`Are you sure you want to delete "${category.name}"?`)) {
      return;
    }

    this.recipeService.deleteRecipeCategory(category.id).subscribe({
      next: () => {
        this.snackBar.open('Category deleted successfully', 'Close', { duration: 3000 });
        this.loadCategories();
      },
      error: (error) => {
        this.snackBar.open('Failed to delete category', 'Close', { duration: 3000 });
        console.error('Error deleting category:', error);
      }
    });
  }

  resetForm(): void {
    this.categoryForm.reset({ sort_order: 0 });
    this.isEditing = false;
    this.editingId = null;
  }

  goBack(): void {
    this.location.back();
  }
}
