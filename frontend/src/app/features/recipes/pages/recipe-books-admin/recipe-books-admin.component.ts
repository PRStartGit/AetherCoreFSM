import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCardModule } from '@angular/material/card';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatCheckboxModule } from '@angular/material/check';
import { MatSelectModule } from '@angular/material/select';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatChipsModule } from '@angular/material/chips';
import { RecipeBookService, RecipeBook, RecipeBookWithRecipes, RecipeInBook } from '../../services/recipe-book.service';
import { RecipeService } from '../../services/recipe.service';
import { SiteService } from '../../../../core/services/site.service';
import { AuthService } from '../../../../core/auth/auth.service';
import { Site } from '../../../../core/models';

@Component({
  selector: 'app-recipe-books-admin',
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
    MatSnackBarModule,
    MatCheckboxModule,
    MatSelectModule,
    MatExpansionModule,
    MatChipsModule
  ],
  templateUrl: './recipe-books-admin.component.html',
  styleUrls: ['./recipe-books-admin.component.scss']
})
export class RecipeBooksAdminComponent implements OnInit {
  recipeBooks: RecipeBook[] = [];
  displayedColumns: string[] = ['title', 'site', 'recipe_count', 'is_active', 'actions'];
  bookForm: FormGroup;
  isEditing = false;
  editingId: number | null = null;

  selectedBook: RecipeBookWithRecipes | null = null;
  availableRecipes: any[] = [];
  sites: Site[] = [];

  constructor(
    private recipeBookService: RecipeBookService,
    private recipeService: RecipeService,
    private siteService: SiteService,
    private authService: AuthService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private dialog: MatDialog
  ) {
    this.bookForm = this.fb.group({
      title: ['', [Validators.required, Validators.maxLength(255)]],
      description: [''],
      site_id: [null],
      is_active: [true]
    });
  }

  ngOnInit(): void {
    this.loadRecipeBooks();
    this.loadSites();
  }

  loadRecipeBooks(): void {
    this.recipeBookService.getAll({ include_inactive: true }).subscribe({
      next: (books) => {
        this.recipeBooks = books;
      },
      error: (error) => {
        this.snackBar.open('Failed to load recipe books', 'Close', { duration: 3000 });
        console.error('Error loading recipe books:', error);
      }
    });
  }

  loadSites(): void {
    const user = this.authService.getUser();
    if (user?.organization_id) {
      this.siteService.getAll(user.organization_id).subscribe({
        next: (sites) => {
          this.sites = sites;
        },
        error: (error) => {
          console.error('Error loading sites:', error);
        }
      });
    }
  }

  onSubmit(): void {
    if (this.bookForm.invalid) {
      return;
    }

    const bookData = this.bookForm.value;

    if (this.isEditing && this.editingId) {
      this.recipeBookService.update(this.editingId, bookData).subscribe({
        next: () => {
          this.snackBar.open('Recipe book updated successfully', 'Close', { duration: 3000 });
          this.loadRecipeBooks();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open('Failed to update recipe book', 'Close', { duration: 3000 });
          console.error('Error updating recipe book:', error);
        }
      });
    } else {
      this.recipeBookService.create(bookData).subscribe({
        next: () => {
          this.snackBar.open('Recipe book created successfully', 'Close', { duration: 3000 });
          this.loadRecipeBooks();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open('Failed to create recipe book', 'Close', { duration: 3000 });
          console.error('Error creating recipe book:', error);
        }
      });
    }
  }

  editBook(book: RecipeBook): void {
    this.isEditing = true;
    this.editingId = book.id;
    this.bookForm.patchValue({
      title: book.title,
      description: book.description,
      site_id: book.site_id,
      is_active: book.is_active
    });
  }

  deleteBook(book: RecipeBook): void {
    if (confirm(`Are you sure you want to delete "${book.title}"?`)) {
      this.recipeBookService.delete(book.id).subscribe({
        next: () => {
          this.snackBar.open('Recipe book deleted successfully', 'Close', { duration: 3000 });
          this.loadRecipeBooks();
          if (this.selectedBook?.id === book.id) {
            this.selectedBook = null;
          }
        },
        error: (error) => {
          this.snackBar.open('Failed to delete recipe book', 'Close', { duration: 3000 });
          console.error('Error deleting recipe book:', error);
        }
      });
    }
  }

  viewBook(book: RecipeBook): void {
    this.recipeBookService.getById(book.id).subscribe({
      next: (bookWithRecipes) => {
        this.selectedBook = bookWithRecipes;
        this.loadAvailableRecipes();
      },
      error: (error) => {
        this.snackBar.open('Failed to load recipe book details', 'Close', { duration: 3000 });
        console.error('Error loading recipe book details:', error);
      }
    });
  }

  loadAvailableRecipes(): void {
    this.recipeService.getRecipes({}).subscribe({
      next: (recipes) => {
        // Filter out recipes already in the book
        const recipeIdsInBook = this.selectedBook?.recipes.map(r => r.id) || [];
        this.availableRecipes = recipes.filter(r => !recipeIdsInBook.includes(r.id));
      },
      error: (error) => {
        console.error('Error loading recipes:', error);
      }
    });
  }

  addRecipeToBook(recipeId: number): void {
    if (!this.selectedBook) return;

    this.recipeBookService.addRecipe(this.selectedBook.id, { recipe_id: recipeId }).subscribe({
      next: () => {
        this.snackBar.open('Recipe added to book', 'Close', { duration: 3000 });
        this.viewBook(this.selectedBook!);
      },
      error: (error) => {
        this.snackBar.open('Failed to add recipe to book', 'Close', { duration: 3000 });
        console.error('Error adding recipe to book:', error);
      }
    });
  }

  removeRecipeFromBook(recipeId: number): void {
    if (!this.selectedBook) return;

    if (confirm('Remove this recipe from the book?')) {
      this.recipeBookService.removeRecipe(this.selectedBook.id, recipeId).subscribe({
        next: () => {
          this.snackBar.open('Recipe removed from book', 'Close', { duration: 3000 });
          this.viewBook(this.selectedBook!);
        },
        error: (error) => {
          this.snackBar.open('Failed to remove recipe from book', 'Close', { duration: 3000 });
          console.error('Error removing recipe from book:', error);
        }
      });
    }
  }

  resetForm(): void {
    this.bookForm.reset({
      title: '',
      description: '',
      site_id: null,
      is_active: true
    });
    this.isEditing = false;
    this.editingId = null;
  }

  cancelEdit(): void {
    this.resetForm();
  }

  closeBookView(): void {
    this.selectedBook = null;
    this.availableRecipes = [];
  }

  getSiteName(siteId: number | null | undefined): string {
    if (!siteId) return 'All Sites';
    const site = this.sites.find(s => s.id === siteId);
    return site ? site.name : 'Unknown Site';
  }

  getRecipeCount(bookId: number): string {
    // This would need to be fetched from the API in a real scenario
    // For now, we'll show a placeholder
    return '—';
  }
}
