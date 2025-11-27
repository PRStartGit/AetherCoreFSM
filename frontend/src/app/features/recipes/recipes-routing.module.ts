import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RecipesLandingComponent } from './pages/recipes-landing/recipes-landing.component';
import { RecipeListComponent } from './pages/recipe-list/recipe-list.component';
import { RecipeFormComponent } from './pages/recipe-form/recipe-form.component';
import { RecipeDetailComponent } from './pages/recipe-detail/recipe-detail.component';
import { RecipesAccessGuard } from './guards/recipes-access.guard';
import { RecipesEditGuard } from './guards/recipes-edit.guard';
import { RoleGuard } from '../../core/guards/role.guard';

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
    path: 'admin/categories',
    loadComponent: () => import('./pages/recipe-categories-admin/recipe-categories-admin.component')
      .then(m => m.RecipeCategoriesAdminComponent),
    canActivate: [RoleGuard],
    data: { roles: ['super_admin'] }
  },
  {
    path: 'admin/units',
    loadComponent: () => import('./pages/ingredient-units-admin/ingredient-units-admin.component')
      .then(m => m.IngredientUnitsAdminComponent),
    canActivate: [RoleGuard],
    data: { roles: ['super_admin'] }
  },
  {
    path: 'admin/allergens',
    loadComponent: () => import('./pages/allergen-keywords-admin/allergen-keywords-admin.component')
      .then(m => m.AllergenKeywordsAdminComponent),
    canActivate: [RoleGuard],
    data: { roles: ['super_admin'] }
  },
  {
    path: 'admin/books',
    loadComponent: () => import('./pages/recipe-books-admin/recipe-books-admin.component')
      .then(m => m.RecipeBooksAdminComponent),
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
