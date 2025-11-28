import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import { RecipeBookService, RecipeBook } from '../../services/recipe-book.service';
import { RecipeWithDetails } from '../../models/recipe.models';
import { AuthService } from '../../../../core/auth/auth.service';
import { User, UserRole } from '../../../../core/models';

@Component({
  selector: 'app-recipe-detail',
  templateUrl: './recipe-detail.component.html',
  styleUrls: ['./recipe-detail.component.css']
})
export class RecipeDetailComponent implements OnInit {
  recipe: RecipeWithDetails | null = null;
  loading = true;
  error: string | null = null;
  currentUser: User | null = null;
  showScaleModal = false;
  showDeleteConfirm = false;
  deleting = false;

  // Add to collection modal
  showAddToCollectionModal = false;
  recipeBooks: RecipeBook[] = [];
  loadingBooks = false;
  addingToBook = false;
  selectedBookId: number | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private recipeService: RecipeService,
    private recipeBookService: RecipeBookService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe(user => {
      this.currentUser = user;
    });

    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadRecipe(parseInt(id));
    }
  }

  loadRecipe(id: number): void {
    this.loading = true;
    this.error = null;

    this.recipeService.getRecipe(id).subscribe({
      next: (recipe) => {
        this.recipe = recipe;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load recipe:', err);
        this.error = 'Failed to load recipe. Please try again later.';
        this.loading = false;
      }
    });
  }

  canEdit(): boolean {
    if (!this.currentUser) return false;

    // Super admins and org admins always have CRUD
    if (this.currentUser.role === UserRole.SUPER_ADMIN || this.currentUser.role === UserRole.ORG_ADMIN) {
      return true;
    }

    // Check job role for CRUD access
    const crudRoles = ['Head Chef', 'Sous Chef', 'General Manager', 'Assistant Manager'];
    if (this.currentUser.job_role && this.currentUser.job_role.name) {
      return crudRoles.includes(this.currentUser.job_role.name);
    }

    return false;
  }

  editRecipe(): void {
    if (this.recipe) {
      this.router.navigate(['/recipes', this.recipe.id, 'edit']);
    }
  }

  openScaleModal(): void {
    this.showScaleModal = true;
  }

  closeScaleModal(): void {
    this.showScaleModal = false;
  }

  printRecipe(): void {
    window.print();
  }

  confirmDelete(): void {
    this.showDeleteConfirm = true;
  }

  cancelDelete(): void {
    this.showDeleteConfirm = false;
  }

  deleteRecipe(): void {
    if (!this.recipe) return;

    this.deleting = true;
    this.recipeService.deleteRecipe(this.recipe.id).subscribe({
      next: () => {
        this.router.navigate(['/recipes']);
      },
      error: (err) => {
        console.error('Failed to delete recipe:', err);
        this.error = 'Failed to delete recipe. Please try again.';
        this.deleting = false;
        this.showDeleteConfirm = false;
      }
    });
  }

  backToList(): void {
    this.router.navigate(['/recipes']);
  }

  onImageError(event: Event): void {
    // Hide the broken image
    (event.target as HTMLImageElement).style.display = 'none';
  }

  openAddToCollectionModal(): void {
    this.showAddToCollectionModal = true;
    this.loadRecipeBooks();
  }

  closeAddToCollectionModal(): void {
    this.showAddToCollectionModal = false;
    this.selectedBookId = null;
  }

  loadRecipeBooks(): void {
    this.loadingBooks = true;
    this.recipeBookService.getAll({ include_inactive: false }).subscribe({
      next: (books) => {
        this.recipeBooks = books;
        this.loadingBooks = false;
      },
      error: (err) => {
        console.error('Failed to load recipe books:', err);
        this.loadingBooks = false;
      }
    });
  }

  addToCollection(): void {
    if (!this.selectedBookId || !this.recipe) return;

    this.addingToBook = true;
    this.recipeBookService.addRecipe(this.selectedBookId, { recipe_id: this.recipe.id }).subscribe({
      next: () => {
        this.addingToBook = false;
        this.closeAddToCollectionModal();
        // Show success message (could use a snackbar)
        alert('Recipe added to collection successfully!');
      },
      error: (err) => {
        console.error('Failed to add recipe to collection:', err);
        this.addingToBook = false;
        if (err.error?.detail) {
          alert(err.error.detail);
        } else {
          alert('Failed to add recipe to collection. Please try again.');
        }
      }
    });
  }
}
