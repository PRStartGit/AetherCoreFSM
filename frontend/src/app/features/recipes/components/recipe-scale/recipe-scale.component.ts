import { Component, Input, Output, EventEmitter, OnInit } from '@angular/core';
import { RecipeWithDetails, RecipeScaled } from '../../models/recipe.models';
import { RecipeService } from '../../services/recipe.service';

@Component({
  selector: 'app-recipe-scale',
  templateUrl: './recipe-scale.component.html',
  styleUrls: ['./recipe-scale.component.css']
})
export class RecipeScaleComponent implements OnInit {
  @Input() recipe!: RecipeWithDetails;
  @Output() close = new EventEmitter<void>();

  newYield: number = 0;
  scaledRecipe: RecipeScaled | null = null;
  loading = false;
  error: string | null = null;

  constructor(private recipeService: RecipeService) {}

  ngOnInit(): void {
    if (this.recipe.yield_quantity) {
      this.newYield = this.recipe.yield_quantity;
    }
  }

  scaleRecipe(): void {
    if (!this.newYield || this.newYield <= 0) {
      this.error = 'Please enter a valid yield quantity';
      return;
    }

    this.loading = true;
    this.error = null;

    this.recipeService.getScaledRecipe(this.recipe.id, this.newYield).subscribe({
      next: (scaled) => {
        this.scaledRecipe = scaled;
        this.loading = false;
      },
      error: (err) => {
        console.error('Failed to scale recipe:', err);
        this.error = 'Failed to scale recipe. Please try again.';
        this.loading = false;
      }
    });
  }

  printScaled(): void {
    window.print();
  }

  closeModal(): void {
    this.close.emit();
  }
}
