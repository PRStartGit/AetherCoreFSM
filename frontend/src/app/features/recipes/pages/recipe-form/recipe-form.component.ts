import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { RecipeService } from '../../services/recipe.service';
import { RecipeCategory, IngredientUnit, RecipeWithDetails } from '../../models/recipe.models';

@Component({
  selector: 'app-recipe-form',
  templateUrl: './recipe-form.component.html',
  styleUrls: ['./recipe-form.component.css']
})
export class RecipeFormComponent implements OnInit {
  recipeForm!: FormGroup;
  categories: RecipeCategory[] = [];
  units: IngredientUnit[] = [];
  isEditMode = false;
  recipeId: number | null = null;
  loading = true;
  submitting = false;
  error: string | null = null;

  // UK 14 Allergens
  allergens: string[] = [
    'Celery', 'Cereals containing gluten', 'Crustaceans', 'Eggs', 'Fish',
    'Lupin', 'Milk', 'Molluscs', 'Mustard', 'Nuts', 'Peanuts',
    'Sesame seeds', 'Soybeans', 'Sulphur dioxide and sulphites'
  ];
  selectedAllergens: Set<string> = new Set();

  constructor(
    private fb: FormBuilder,
    private recipeService: RecipeService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.initForm();
    this.loadReferenceData();

    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.isEditMode = true;
      this.recipeId = parseInt(id);
      this.loadRecipe(this.recipeId);
    } else {
      this.loading = false;
    }
  }

  initForm(): void {
    this.recipeForm = this.fb.group({
      category_id: [null],
      title: ['', [Validators.required, Validators.maxLength(255)]],
      description: [''],
      instructions: [''],
      prep_time_minutes: [null, [Validators.min(0)]],
      cook_time_minutes: [null, [Validators.min(0)]],
      yield_quantity: [null, [Validators.min(0)]],
      yield_unit: [''],
      cost_per_unit: [null, [Validators.min(0)]],
      notes: [''],
      ingredients: this.fb.array([])
    });
  }

  get ingredients(): FormArray {
    return this.recipeForm.get('ingredients') as FormArray;
  }

  addIngredient(): void {
    const ingredientGroup = this.fb.group({
      name: ['', Validators.required],
      quantity: [null],
      unit: [''],
      order_index: [this.ingredients.length]
    });
    this.ingredients.push(ingredientGroup);
  }

  removeIngredient(index: number): void {
    this.ingredients.removeAt(index);
    // Update order indices
    this.ingredients.controls.forEach((control, i) => {
      control.patchValue({ order_index: i });
    });
  }

  loadReferenceData(): void {
    this.recipeService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (err) => console.error('Failed to load categories:', err)
    });

    this.recipeService.getIngredientUnits().subscribe({
      next: (units) => {
        this.units = units;
      },
      error: (err) => console.error('Failed to load units:', err)
    });
  }

  loadRecipe(id: number): void {
    this.recipeService.getRecipe(id).subscribe({
      next: (recipe) => {
        this.recipeForm.patchValue({
          category_id: recipe.category_id,
          title: recipe.title,
          description: recipe.description,
          instructions: recipe.instructions,
          prep_time_minutes: recipe.prep_time_minutes,
          cook_time_minutes: recipe.cook_time_minutes,
          yield_quantity: recipe.yield_quantity,
          yield_unit: recipe.yield_unit,
          cost_per_unit: recipe.cost_per_unit,
          notes: recipe.notes
        });

        // Load ingredients
        recipe.ingredients.forEach(ingredient => {
          const ingredientGroup = this.fb.group({
            name: [ingredient.name, Validators.required],
            quantity: [ingredient.quantity],
            unit: [ingredient.unit],
            order_index: [ingredient.order_index]
          });
          this.ingredients.push(ingredientGroup);
        });

        // Load allergens
        if (recipe.allergens) {
          this.selectedAllergens = new Set(recipe.allergens);
        }

        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to load recipe:', err);
        this.error = 'Failed to load recipe. Please try again.';
        this.loading = false;
      }
    });
  }

  toggleAllergen(allergen: string): void {
    if (this.selectedAllergens.has(allergen)) {
      this.selectedAllergens.delete(allergen);
    } else {
      this.selectedAllergens.add(allergen);
    }
  }

  isAllergenSelected(allergen: string): boolean {
    return this.selectedAllergens.has(allergen);
  }

  getSelectedAllergensArray(): string[] {
    return Array.from(this.selectedAllergens);
  }

  onSubmit(): void {
    if (this.recipeForm.invalid) {
      this.recipeForm.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.error = null;

    const formValue = {
      ...this.recipeForm.value,
      allergens: Array.from(this.selectedAllergens)
    };

    if (this.isEditMode && this.recipeId) {
      this.recipeService.updateRecipe(this.recipeId, formValue).subscribe({
        next: () => {
          this.router.navigate(['/recipes/list']);
        },
        error: (err) => {
          console.error('Failed to update recipe:', err);
          this.error = err.error?.detail || 'Failed to update recipe. Please try again.';
          this.submitting = false;
        }
      });
    } else {
      this.recipeService.createRecipe(formValue).subscribe({
        next: () => {
          this.router.navigate(['/recipes/list']);
        },
        error: (err) => {
          console.error('Failed to create recipe:', err);
          this.error = err.error?.detail || 'Failed to create recipe. Please try again.';
          this.submitting = false;
        }
      });
    }
  }

  cancel(): void {
    this.router.navigate(['/recipes/list']);
  }
}
