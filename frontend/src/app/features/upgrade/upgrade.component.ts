import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { SubscriptionService, ModuleAccessInfo, ModuleAccessResponse } from '../../core/services/subscription.service';
import { UpgradePromptComponent } from '../../shared/components/upgrade-prompt/upgrade-prompt.component';

@Component({
  selector: 'app-upgrade',
  standalone: true,
  imports: [CommonModule, UpgradePromptComponent],
  templateUrl: './upgrade.component.html',
  styleUrls: ['./upgrade.component.scss']
})
export class UpgradeComponent implements OnInit {
  moduleCode: string | null = null;
  moduleInfo: ModuleAccessInfo | null = null;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private subscriptionService: SubscriptionService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.moduleCode = params['module'] || sessionStorage.getItem('upgrade_requested_module');
      if (this.moduleCode) {
        this.loadModuleInfo();
      } else {
        this.loading = false;
      }
    });
  }

  loadModuleInfo(): void {
    this.subscriptionService.getMyModuleAccess().subscribe({
      next: (response: ModuleAccessResponse) => {
        if (this.moduleCode) {
          this.moduleInfo = response.modules.find(m => m.code === this.moduleCode) || null;
        }
        this.loading = false;
      },
      error: () => {
        this.loading = false;
        // Create a basic module info from session storage
        const moduleName = sessionStorage.getItem('upgrade_module_name');
        if (moduleName && this.moduleCode) {
          this.moduleInfo = {
            code: this.moduleCode,
            name: moduleName,
            description: null,
            icon: null,
            has_access: false,
            access_type: null,
            addon_price_per_site: null,
            addon_price_per_org: null
          };
        }
      }
    });
  }

  goBack(): void {
    // Clear session storage
    sessionStorage.removeItem('upgrade_requested_module');
    sessionStorage.removeItem('upgrade_module_name');
    
    // Navigate back to dashboard based on role or home
    this.router.navigate(['/']);
  }
}
