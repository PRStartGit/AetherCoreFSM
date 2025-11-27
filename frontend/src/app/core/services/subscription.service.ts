import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, tap } from 'rxjs';


export interface Module {
  id: number;
  name: string;
  code: string;
  description: string | null;
  icon: string | null;
  is_core: boolean;
  addon_price_per_site: number | null;
  addon_price_per_org: number | null;
  gocardless_addon_plan_id: string | null;
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
  gocardless_addon_plan_id?: string;
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
  gocardless_plan_id: string | null;
  gocardless_annual_plan_id: string | null;
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
  gocardless_plan_id?: string;
  gocardless_annual_plan_id?: string;
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

// Module Access Control Types
export interface ModuleAccessInfo {
  code: string;
  name: string;
  description: string | null;
  icon: string | null;
  has_access: boolean;
  access_type: 'core' | 'package' | 'addon' | null;
  addon_price_per_site: number | null;
  addon_price_per_org: number | null;
}

export interface ModuleAccessResponse {
  organization_id: number;
  organization_name: string;
  package_code: string | null;
  package_name: string | null;
  is_trial: boolean;
  modules: ModuleAccessInfo[];
}

export interface ModuleAccessCheck {
  has_access: boolean;
  access_type?: 'core' | 'package' | 'addon';
  reason?: 'no_organization' | 'organization_not_found' | 'module_not_found' | 'not_in_package';
  module_name?: string;
  addon_price_per_site?: number | null;
  addon_price_per_org?: number | null;
}

@Injectable({
  providedIn: 'root'
})
export class SubscriptionService {
  private readonly API_URL = '/api/v1/subscriptions';

  // Cache for module access - refreshed on login/navigation
  private moduleAccessSubject = new BehaviorSubject<ModuleAccessResponse | null>(null);
  public moduleAccess$ = this.moduleAccessSubject.asObservable();

  constructor(private http: HttpClient) {}

  // ============ Module Methods ============

  getModules(): Observable<Module[]> {
    return this.http.get<Module[]>(`${this.API_URL}/modules`);
  }

  createModule(data: ModuleCreate): Observable<Module> {
    return this.http.post<Module>(`${this.API_URL}/modules`, data);
  }

  updateModule(id: number, data: ModuleUpdate): Observable<Module> {
    return this.http.put<Module>(`${this.API_URL}/modules/\${id}`, data);
  }

  deleteModule(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/modules/\${id}`);
  }

  // ============ Package Methods ============

  getPackages(): Observable<SubscriptionPackage[]> {
    return this.http.get<SubscriptionPackage[]>(`${this.API_URL}/packages`);
  }

  createPackage(data: SubscriptionPackageCreate): Observable<SubscriptionPackage> {
    return this.http.post<SubscriptionPackage>(`${this.API_URL}/packages`, data);
  }

  updatePackage(id: number, data: SubscriptionPackageUpdate): Observable<SubscriptionPackage> {
    return this.http.put<SubscriptionPackage>(`${this.API_URL}/packages/\${id}`, data);
  }

  deletePackage(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/packages/\${id}`);
  }

  // ============ Public Pricing ============

  getPricing(): Observable<PricingResponse> {
    return this.http.get<PricingResponse>(`${this.API_URL}/pricing`);
  }

  // ============ Module Access Control ============

  /**
   * Get all module access information for the current user's organization.
   * Results are cached in moduleAccess$ BehaviorSubject.
   */
  getMyModuleAccess(): Observable<ModuleAccessResponse> {
    return this.http.get<ModuleAccessResponse>(`${this.API_URL}/my-access`).pipe(
      tap(response => this.moduleAccessSubject.next(response))
    );
  }

  /**
   * Check if the current user has access to a specific module.
   */
  checkModuleAccess(moduleCode: string): Observable<ModuleAccessCheck> {
    return this.http.get<ModuleAccessCheck>(`${this.API_URL}/check-access/\${moduleCode}`);
  }

  /**
   * Quick synchronous check using cached data.
   * Returns true if module is accessible, false otherwise.
   * Falls back to false if cache is empty.
   */
  hasModuleAccess(moduleCode: string): boolean {
    const access = this.moduleAccessSubject.value;
    if (!access) return false;
    const module = access.modules.find(m => m.code === moduleCode);
    return module?.has_access ?? false;
  }

  /**
   * Get cached module info by code.
   */
  getModuleInfo(moduleCode: string): ModuleAccessInfo | undefined {
    const access = this.moduleAccessSubject.value;
    if (!access) return undefined;
    return access.modules.find(m => m.code === moduleCode);
  }

  /**
   * Clear the cached module access (call on logout).
   */
  clearModuleAccessCache(): void {
    this.moduleAccessSubject.next(null);
  }
}
