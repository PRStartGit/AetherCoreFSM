import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecipesLandingComponent } from './pages/recipes-landing/recipes-landing.component';
import { RecipeListComponent } from './pages/recipe-list/recipe-list.component';
import { RecipeFormComponent } from './pages/recipe-form/recipe-form.component';
import { RecipeDetailComponent } from './pages/recipe-detail/recipe-detail.component';
import { RecipesAccessGuard } from './guards/recipes-access.guard';
import { RecipesEditGuard } from './guards/recipes-edit.guard';

const routes: Routes = [
  {
    path: '',
    component: RecipesLandingComponent
  },
  {
    path: 'list',
    component: RecipeListComponent,
    canActivate: [RecipesAccessGuard]
  },
  {
    path: 'create',
    component: RecipeFormComponent,
    canActivate: [RecipesEditGuard]
  },
  {
    path: ':id',
    component: RecipeDetailComponent,
    canActivate: [RecipesAccessGuard]
  },
  {
    path: ':id/edit',
    component: RecipeFormComponent,
    canActivate: [RecipesEditGuard]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class RecipesRoutingModule { }
