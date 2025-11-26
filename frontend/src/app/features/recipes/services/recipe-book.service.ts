import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface RecipeBook {
  id: number;
  organization_id: number;
  site_id?: number | null;
  title: string;
  description?: string | null;
  is_active: boolean;
  created_by_user_id: number;
  created_at: string;
  updated_at?: string | null;
}

export interface RecipeInBook {
  id: number;
  title: string;
  description?: string | null;
  photo_url?: string | null;
  category_id?: number | null;
  order_index: number;
  added_at: string;
}

export interface RecipeBookWithRecipes extends RecipeBook {
  recipes: RecipeInBook[];
  recipe_count: number;
}

export interface RecipeBookCreate {
  title: string;
  description?: string | null;
  site_id?: number | null;
  is_active?: boolean;
}

export interface RecipeBookUpdate {
  title?: string;
  description?: string | null;
  site_id?: number | null;
  is_active?: boolean;
}

export interface AddRecipeToBook {
  recipe_id: number;
  order_index?: number;
}

@Injectable({
  providedIn: 'root'
})
export class RecipeBookService {
  private apiUrl = `${environment.apiUrl}/recipe-books`;

  constructor(private http: HttpClient) {}

  /**
   * Get all recipe books for the organization
   */
  getAll(params?: {
    site_id?: number | null;
    include_inactive?: boolean;
    skip?: number;
    limit?: number;
  }): Observable<RecipeBook[]> {
    let httpParams = new HttpParams();

    if (params) {
      if (params.site_id !== undefined && params.site_id !== null) {
        httpParams = httpParams.set('site_id', params.site_id.toString());
      }
      if (params.include_inactive !== undefined) {
        httpParams = httpParams.set('include_inactive', params.include_inactive.toString());
      }
      if (params.skip !== undefined) {
        httpParams = httpParams.set('skip', params.skip.toString());
      }
      if (params.limit !== undefined) {
        httpParams = httpParams.set('limit', params.limit.toString());
      }
    }

    return this.http.get<RecipeBook[]>(this.apiUrl, { params: httpParams });
  }

  /**
   * Get a single recipe book with its recipes
   */
  getById(id: number): Observable<RecipeBookWithRecipes> {
    return this.http.get<RecipeBookWithRecipes>(`${this.apiUrl}/${id}`);
  }

  /**
   * Create a new recipe book
   */
  create(book: RecipeBookCreate): Observable<RecipeBook> {
    return this.http.post<RecipeBook>(this.apiUrl, book);
  }

  /**
   * Update a recipe book
   */
  update(id: number, book: RecipeBookUpdate): Observable<RecipeBook> {
    return this.http.put<RecipeBook>(`${this.apiUrl}/${id}`, book);
  }

  /**
   * Delete a recipe book
   */
  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  /**
   * Add a recipe to a book
   */
  addRecipe(bookId: number, data: AddRecipeToBook): Observable<any> {
    return this.http.post(`${this.apiUrl}/${bookId}/recipes`, data);
  }

  /**
   * Remove a recipe from a book
   */
  removeRecipe(bookId: number, recipeId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${bookId}/recipes/${recipeId}`);
  }
}
