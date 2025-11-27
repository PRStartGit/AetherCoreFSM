import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { RecipeService } from '../../services/recipe.service';
import { Recipe, RecipeCategory } from '../../models/recipe.models';
import { AuthService } from '../../../../core/auth/auth.service';
import { User, UserRole } from '../../../../core/models';

@Component({
  selector: 'app-recipe-list',
  templateUrl: './recipe-list.component.html',
  styleUrls: ['./recipe-list.component.css']
})
export class RecipeListComponent implements OnInit {
  recipes: Recipe[] = [];
  categories: RecipeCategory[] = [];
  loading = true;
  error: string | null = null;
  currentUser: User | null = null;

  // Filters
  searchTerm: string = '';
  selectedCategoryId: number | null = null;
  selectedAllergen: string = '';
  showArchived: boolean = false;

  // UK 14 Allergens
  allergens: string[] = [
    'Celery', 'Cereals containing gluten', 'Crustaceans', 'Eggs', 'Fish',
    'Lupin', 'Milk', 'Molluscs', 'Mustard', 'Nuts', 'Peanuts',
    'Sesame seeds', 'Soybeans', 'Sulphur dioxide and sulphites'
  ];

  constructor(
    private recipeService: RecipeService,
    private authService: AuthService,
    private router: Router,
    private location: Location
  ) {}

  ngOnInit(): void {
    this.authService.getCurrentUser().subscribe(user => {
      this.currentUser = user;
    });
    this.loadCategories();
    this.loadRecipes();
  }

  loadCategories(): void {
    this.recipeService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (err) => console.error('Failed to load categories:', err)
    });
  }

  loadRecipes(): void {
    this.loading = true;
    this.error = null;

    const filters = {
      search: this.searchTerm || undefined,
      category_id: this.selectedCategoryId || undefined,
      allergen: this.selectedAllergen || undefined,
      include_archived: this.showArchived
    };

    this.recipeService.getRecipes(filters).subscribe({
      next: (recipes) => {
        this.recipes = recipes;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load recipes:', err);
        this.error = 'Failed to load recipes. Please try again later.';
        this.loading = false;
      }
    });
  }

  applyFilters(): void {
    this.loadRecipes();
  }

  clearFilters(): void {
    this.searchTerm = '';
    this.selectedCategoryId = null;
    this.selectedAllergen = '';
    this.showArchived = false;
    this.loadRecipes();
  }

  viewRecipe(id: number): void {
    this.router.navigate(['/recipes', id]);
  }

  canCreate(): boolean {
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

  createRecipe(): void {
    this.router.navigate(['/recipes/create']);
  }

  goBack(): void {
    this.location.back();
  }
}
