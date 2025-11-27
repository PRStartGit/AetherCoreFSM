import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

export interface Module {
  id: number;
  name: string;
  code: string;
  description: string | null;
  icon: string | null;
  is_core: boolean;
  addon_price_per_site: number | null;
  addon_price_per_org: number | null;
  stripe_addon_price_id: string | null;
  is_active: boolean;
  display_order: number;
  created_at: string;
  updated_at: string | null;
}

export interface ModuleCreate {
  name: string;
  code: string;
  description?: string;
  icon?: string;
  is_core?: boolean;
  addon_price_per_site?: number;
  addon_price_per_org?: number;
  is_active?: boolean;
  display_order?: number;
}

export interface ModuleUpdate {
  name?: string;
  description?: string;
  icon?: string;
  is_core?: boolean;
  addon_price_per_site?: number | null;
  addon_price_per_org?: number | null;
  stripe_addon_price_id?: string;
  is_active?: boolean;
  display_order?: number;
}

export interface PackageModule {
  module_id: number;
  module_name: string;
  module_code: string;
  is_included: boolean;
}

export interface SubscriptionPackage {
  id: number;
  name: string;
  code: string;
  description: string | null;
  min_sites: number;
  max_sites: number | null;
  monthly_price: number;
  annual_price: number | null;
  stripe_monthly_price_id: string | null;
  stripe_annual_price_id: string | null;
  features_json: string | null;
  is_active: boolean;
  is_popular: boolean;
  display_order: number;
  created_at: string;
  updated_at: string | null;
  included_modules: PackageModule[];
}

export interface SubscriptionPackageCreate {
  name: string;
  code: string;
  description?: string;
  min_sites?: number;
  max_sites?: number | null;
  monthly_price?: number;
  annual_price?: number | null;
  features_json?: string;
  is_active?: boolean;
  is_popular?: boolean;
  display_order?: number;
  included_module_ids?: number[];
}

export interface SubscriptionPackageUpdate {
  name?: string;
  description?: string;
  min_sites?: number;
  max_sites?: number | null;
  monthly_price?: number;
  annual_price?: number | null;
  stripe_monthly_price_id?: string;
  stripe_annual_price_id?: string;
  features_json?: string;
  is_active?: boolean;
  is_popular?: boolean;
  display_order?: number;
  included_module_ids?: number[];
}

export interface PricingTier {
  id: number;
  name: string;
  code: string;
  description: string | null;
  site_range: string;
  monthly_price: number;
  annual_price: number | null;
  features: string[];
  included_modules: string[];
  is_popular: boolean;
}

export interface PricingResponse {
  tiers: PricingTier[];
  available_addons: Module[];
}

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  private readonly API_URL = `${environment.apiUrl}/subscriptions`;

  constructor(private http: HttpClient) {}

  // ============ Module Methods ============

  getModules(): Observable<Module[]> {
    return this.http.get<Module[]>(`${this.API_URL}/modules`);
  }

  createModule(data: ModuleCreate): Observable<Module> {
    return this.http.post<Module>(`${this.API_URL}/modules`, data);
  }

  updateModule(id: number, data: ModuleUpdate): Observable<Module> {
    return this.http.put<Module>(`${this.API_URL}/modules/${id}`, data);
  }

  deleteModule(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/modules/${id}`);
  }

  // ============ Package Methods ============

  getPackages(): Observable<SubscriptionPackage[]> {
    return this.http.get<SubscriptionPackage[]>(`${this.API_URL}/packages`);
  }

  createPackage(data: SubscriptionPackageCreate): Observable<SubscriptionPackage> {
    return this.http.post<SubscriptionPackage>(`${this.API_URL}/packages`, data);
  }

  updatePackage(id: number, data: SubscriptionPackageUpdate): Observable<SubscriptionPackage> {
    return this.http.put<SubscriptionPackage>(`${this.API_URL}/packages/${id}`, data);
  }

  deletePackage(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/packages/${id}`);
  }

  // ============ Public Pricing ============

  getPricing(): Observable<PricingResponse> {
    return this.http.get<PricingResponse>(`${this.API_URL}/pricing`);
  }
}
