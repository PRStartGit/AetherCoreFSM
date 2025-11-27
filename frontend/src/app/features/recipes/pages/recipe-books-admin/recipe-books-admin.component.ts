import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RecipeBookService, RecipeBook, RecipeBookWithRecipes, RecipeInBook } from '../../services/recipe-book.service';
import { RecipeService } from '../../services/recipe.service';
import { SiteService } from '../../../../core/services/site.service';
import { AuthService } from '../../../../core/auth/auth.service';
import { Site, UserRole } from '../../../../core/models';

@Component({
  selector: 'app-recipe-books-admin',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatSnackBarModule
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

  selectedSiteIds: number[] = [];

  constructor(
    private recipeBookService: RecipeBookService,
    private recipeService: RecipeService,
    private siteService: SiteService,
    private authService: AuthService,
    private fb: FormBuilder,
    private snackBar: MatSnackBar,
    private http: HttpClient
  ) {
    this.bookForm = this.fb.group({
      title: ['', [Validators.required, Validators.maxLength(255)]],
      description: [''],
      site_ids: [[]],  // Multiple sites
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

    // Super admin can see all sites across all organizations
    if (user?.role === UserRole.SUPER_ADMIN) {
      this.http.get<Site[]>('/api/v1/sites/all').subscribe({
        next: (sites) => {
          this.sites = sites;
        },
        error: (error) => {
          console.error('Error loading all sites:', error);
          // Fallback to empty array
          this.sites = [];
        }
      });
    } else if (user?.organization_id) {
      // Regular users see only their organization's sites
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
    const siteIds = book.sites?.map(s => s.id) || [];
    this.bookForm.patchValue({
      title: book.title,
      description: book.description,
      site_ids: siteIds,
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
      site_ids: [],
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

  getSiteNames(book: RecipeBook): string {
    if (book.sites && book.sites.length > 0) {
      return book.sites.map(s => s.name).join(', ');
    }
    if (book.site_id) {
      return this.getSiteName(book.site_id);
    }
    return 'All Sites';
  }

  getRecipeCount(bookId: number): string {
    // This would need to be fetched from the API in a real scenario
    // For now, we'll show a placeholder
    return '—';
  }
}
