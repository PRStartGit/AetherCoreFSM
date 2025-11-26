import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Recipe,
  RecipeWithDetails,
  RecipeScaled,
  RecipeCreateRequest,
  RecipeUpdateRequest,
  RecipeFilters,
  RecipeCategory,
  IngredientUnit
} from '../models/recipe.models';

@Injectable({
  providedIn: 'root'
})
export class RecipeService {
  private readonly API_URL = '/api/v1/recipes';

  constructor(private http: HttpClient) {}

  getRecipes(filters?: RecipeFilters): Observable<Recipe[]> {
    let params = new HttpParams();

    if (filters) {
      if (filters.search) params = params.set('search', filters.search);
      if (filters.category_id !== undefined) params = params.set('category_id', filters.category_id.toString());
      if (filters.allergen) params = params.set('allergen', filters.allergen);
      if (filters.include_archived !== undefined) params = params.set('include_archived', filters.include_archived.toString());
      if (filters.skip !== undefined) params = params.set('skip', filters.skip.toString());
      if (filters.limit !== undefined) params = params.set('limit', filters.limit.toString());
    }

    return this.http.get<Recipe[]>(this.API_URL, { params });
  }

  getRecipe(id: number): Observable<RecipeWithDetails> {
    return this.http.get<RecipeWithDetails>(`${this.API_URL}/${id}`);
  }

  getScaledRecipe(id: number, yieldQuantity: number): Observable<RecipeScaled> {
    const params = new HttpParams().set('yield_quantity', yieldQuantity.toString());
    return this.http.get<RecipeScaled>(`${this.API_URL}/${id}/scaled`, { params });
  }

  createRecipe(recipe: RecipeCreateRequest): Observable<Recipe> {
    return this.http.post<Recipe>(this.API_URL, recipe);
  }

  updateRecipe(id: number, recipe: RecipeUpdateRequest): Observable<Recipe> {
    return this.http.put<Recipe>(`${this.API_URL}/${id}`, recipe);
  }

  deleteRecipe(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/${id}`);
  }

  getCategories(): Observable<RecipeCategory[]> {
    return this.http.get<RecipeCategory[]>(`${this.API_URL}/categories`);
  }

  getIngredientUnits(): Observable<IngredientUnit[]> {
    return this.http.get<IngredientUnit[]>(`${this.API_URL}/units`);
  }
}
