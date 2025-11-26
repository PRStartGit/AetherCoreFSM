import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { RecipesRoutingModule } from './recipes-routing.module';
import { RecipesLandingComponent } from './pages/recipes-landing/recipes-landing.component';
import { RecipeListComponent } from './pages/recipe-list/recipe-list.component';
import { RecipeFormComponent } from './pages/recipe-form/recipe-form.component';
import { RecipeDetailComponent } from './pages/recipe-detail/recipe-detail.component';
import { RecipeScaleComponent } from './components/recipe-scale/recipe-scale.component';
import { RecipeService } from './services/recipe.service';
import { RecipesAccessGuard } from './guards/recipes-access.guard';
import { RecipesEditGuard } from './guards/recipes-edit.guard';

@NgModule({
  declarations: [
    RecipesLandingComponent,
    RecipeListComponent,
    RecipeFormComponent,
    RecipeDetailComponent,
    RecipeScaleComponent
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    RecipesRoutingModule
  ],
  providers: [
    RecipeService,
    RecipesAccessGuard,
    RecipesEditGuard
  ]
})
export class RecipesModule { }
