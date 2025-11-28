export interface RecipeCategory {
  id: number;
  name: string;
  sort_order: number;
  created_at: string;
}

export interface IngredientUnit {
  id: number;
  name: string;
  display_name: string;
  category?: string;
  sort_order: number;
}

export interface RecipeIngredient {
  id?: number;
  recipe_id?: number;
  name: string;
  quantity?: number;
  unit?: string;
  order_index: number;
}

export interface Recipe {
  id: number;
  organization_id: number;
  category_id?: number;
  title: string;
  description?: string;
  method?: string;  // Instructions/method from backend
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  total_time_minutes?: number;
  yield_quantity?: number;
  yield_unit?: string;
  cost_per_unit?: number;
  notes?: string;
  photo_url?: string;  // Recipe photo
  is_archived: boolean;
  created_by_user_id: number;
  created_at: string;
  updated_at?: string;
  category_name?: string;
}

export interface RecipeWithDetails extends Recipe {
  ingredients: RecipeIngredient[];
  allergens: string[];
}

export interface RecipeScaledIngredient {
  name: string;
  original_quantity?: number;
  scaled_quantity?: number;
  unit?: string;
}

export interface RecipeScaled extends Recipe {
  original_yield?: number;
  scaled_yield: number;
  scale_factor: number;
  ingredients: RecipeScaledIngredient[];
  allergens: string[];
}

export interface RecipeCreateRequest {
  category_id?: number;
  title: string;
  description?: string;
  method?: string;
  prep_time_minutes?: number;
  cook_time_minutes?: number;
  yield_quantity?: number;
  yield_unit?: string;
  cost_per_unit?: number;
  notes?: string;
  photo_url?: string;
  ingredients: RecipeIngredient[];
  allergens?: string[];
}

export interface RecipeUpdateRequest extends Partial<RecipeCreateRequest> {}

export interface RecipeFilters {
  search?: string;
  category_id?: number;
  allergen?: string;
  recipe_book_id?: number;
  include_archived?: boolean;
  skip?: number;
  limit?: number;
}
