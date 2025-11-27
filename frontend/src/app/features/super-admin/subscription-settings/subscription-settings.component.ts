import { Component, OnInit } from '@angular/core';
import { SubscriptionService, Module, SubscriptionPackage, ModuleCreate, ModuleUpdate, SubscriptionPackageCreate, SubscriptionPackageUpdate } from '../../../core/services/subscription.service';

@Component({
  selector: 'app-subscription-settings',
  templateUrl: './subscription-settings.component.html',
  styleUrls: ['./subscription-settings.component.scss']
})
export class SubscriptionSettingsComponent implements OnInit {
  activeTab: 'packages' | 'modules' = 'packages';

  // Data
  packages: SubscriptionPackage[] = [];
  modules: Module[] = [];

  // Loading states
  loadingPackages = true;
  loadingModules = true;
  error: string | null = null;

  // Package form
  showPackageForm = false;
  editingPackage: SubscriptionPackage | null = null;
  packageFormData: any = {};
  selectedModuleIds: number[] = [];

  // Module form
  showModuleForm = false;
  editingModule: Module | null = null;
  moduleFormData: any = {};

  constructor(private subscriptionService: SubscriptionService) {}

  ngOnInit(): void {
    this.loadPackages();
    this.loadModules();
  }

  // ============ Data Loading ============

  loadPackages(): void {
    this.loadingPackages = true;
    this.subscriptionService.getPackages().subscribe({
      next: (packages) => {
        this.packages = packages;
        this.loadingPackages = false;
      },
      error: (err) => {
        this.error = 'Failed to load packages';
        this.loadingPackages = false;
        console.error(err);
      }
    });
  }

  loadModules(): void {
    this.loadingModules = true;
    this.subscriptionService.getModules().subscribe({
      next: (modules) => {
        this.modules = modules;
        this.loadingModules = false;
      },
      error: (err) => {
        this.error = 'Failed to load modules';
        this.loadingModules = false;
        console.error(err);
      }
    });
  }

  // ============ Package Form ============

  openPackageCreate(): void {
    this.editingPackage = null;
    this.packageFormData = {
      name: '',
      code: '',
      description: '',
      min_sites: 1,
      max_sites: null,
      monthly_price: 0,
      annual_price: null,
      features_json: '[]',
      is_active: true,
      is_popular: false,
      display_order: this.packages.length + 1
    };
    this.selectedModuleIds = this.modules.filter(m => m.is_core).map(m => m.id);
    this.showPackageForm = true;
  }

  openPackageEdit(pkg: SubscriptionPackage): void {
    this.editingPackage = pkg;
    this.packageFormData = {
      name: pkg.name,
      code: pkg.code,
      description: pkg.description || '',
      min_sites: pkg.min_sites,
      max_sites: pkg.max_sites,
      monthly_price: pkg.monthly_price,
      annual_price: pkg.annual_price,
      features_json: pkg.features_json || '[]',
      is_active: pkg.is_active,
      is_popular: pkg.is_popular,
      display_order: pkg.display_order,
      stripe_monthly_price_id: pkg.stripe_monthly_price_id || '',
      stripe_annual_price_id: pkg.stripe_annual_price_id || ''
    };
    this.selectedModuleIds = pkg.included_modules.map(m => m.module_id);
    this.showPackageForm = true;
  }

  closePackageForm(): void {
    this.showPackageForm = false;
    this.editingPackage = null;
  }

  submitPackageForm(): void {
    const data: any = {
      ...this.packageFormData,
      included_module_ids: this.selectedModuleIds
    };

    // Clean up empty strings
    if (!data.max_sites) data.max_sites = null;
    if (!data.annual_price) data.annual_price = null;

    if (this.editingPackage) {
      this.subscriptionService.updatePackage(this.editingPackage.id, data).subscribe({
        next: () => {
          this.closePackageForm();
          this.loadPackages();
        },
        error: (err) => alert(err.error?.detail || 'Failed to update package')
      });
    } else {
      this.subscriptionService.createPackage(data).subscribe({
        next: () => {
          this.closePackageForm();
          this.loadPackages();
        },
        error: (err) => alert(err.error?.detail || 'Failed to create package')
      });
    }
  }

  deletePackage(pkg: SubscriptionPackage): void {
    if (confirm(`Delete package "${pkg.name}"? This cannot be undone.`)) {
      this.subscriptionService.deletePackage(pkg.id).subscribe({
        next: () => this.loadPackages(),
        error: (err) => alert(err.error?.detail || 'Failed to delete package')
      });
    }
  }

  toggleModuleInPackage(moduleId: number): void {
    const module = this.modules.find(m => m.id === moduleId);
    if (module?.is_core) return; // Can't toggle core modules

    const index = this.selectedModuleIds.indexOf(moduleId);
    if (index > -1) {
      this.selectedModuleIds.splice(index, 1);
    } else {
      this.selectedModuleIds.push(moduleId);
    }
  }

  isModuleSelected(moduleId: number): boolean {
    return this.selectedModuleIds.includes(moduleId);
  }

  // ============ Module Form ============

  openModuleCreate(): void {
    this.editingModule = null;
    this.moduleFormData = {
      name: '',
      code: '',
      description: '',
      icon: '',
      is_core: false,
      addon_price_per_site: null,
      addon_price_per_org: null,
      is_active: true,
      display_order: this.modules.length + 1
    };
    this.showModuleForm = true;
  }

  openModuleEdit(module: Module): void {
    this.editingModule = module;
    this.moduleFormData = {
      name: module.name,
      code: module.code,
      description: module.description || '',
      icon: module.icon || '',
      is_core: module.is_core,
      addon_price_per_site: module.addon_price_per_site,
      addon_price_per_org: module.addon_price_per_org,
      stripe_addon_price_id: module.stripe_addon_price_id || '',
      is_active: module.is_active,
      display_order: module.display_order
    };
    this.showModuleForm = true;
  }

  closeModuleForm(): void {
    this.showModuleForm = false;
    this.editingModule = null;
  }

  submitModuleForm(): void {
    const data: any = { ...this.moduleFormData };

    // Clean up empty values
    if (!data.addon_price_per_site) data.addon_price_per_site = null;
    if (!data.addon_price_per_org) data.addon_price_per_org = null;

    if (this.editingModule) {
      this.subscriptionService.updateModule(this.editingModule.id, data).subscribe({
        next: () => {
          this.closeModuleForm();
          this.loadModules();
        },
        error: (err) => alert(err.error?.detail || 'Failed to update module')
      });
    } else {
      this.subscriptionService.createModule(data).subscribe({
        next: () => {
          this.closeModuleForm();
          this.loadModules();
        },
        error: (err) => alert(err.error?.detail || 'Failed to create module')
      });
    }
  }

  deleteModule(module: Module): void {
    if (module.is_core) {
      alert('Cannot delete core modules');
      return;
    }
    if (confirm(`Delete module "${module.name}"? This cannot be undone.`)) {
      this.subscriptionService.deleteModule(module.id).subscribe({
        next: () => this.loadModules(),
        error: (err) => alert(err.error?.detail || 'Failed to delete module')
      });
    }
  }

  // ============ Helpers ============

  getSiteRange(pkg: SubscriptionPackage): string {
    if (pkg.max_sites === null) {
      return `${pkg.min_sites}+ sites`;
    } else if (pkg.min_sites === pkg.max_sites) {
      return pkg.min_sites === 1 ? '1 site' : `${pkg.min_sites} sites`;
    }
    return `${pkg.min_sites}-${pkg.max_sites} sites`;
  }

  getFeatures(pkg: SubscriptionPackage): string[] {
    try {
      return JSON.parse(pkg.features_json || '[]');
    } catch {
      return [];
    }
  }

  formatPrice(price: number): string {
    return price === 0 ? 'Free' : `£${price.toFixed(2)}`;
  }

  getPricingType(module: Module): string {
    if (module.is_core) return 'Core (included)';
    if (module.addon_price_per_site) return `£${module.addon_price_per_site}/site`;
    if (module.addon_price_per_org) return `£${module.addon_price_per_org}/org`;
    return 'No add-on pricing';
  }
}
