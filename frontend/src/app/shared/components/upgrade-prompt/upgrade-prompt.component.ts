import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ModuleAccessInfo } from '../../../core/services/subscription.service';

@Component({
  selector: 'app-upgrade-prompt',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './upgrade-prompt.component.html',
  styleUrls: ['./upgrade-prompt.component.scss']
})
export class UpgradePromptComponent {
  @Input() moduleInfo: ModuleAccessInfo | null = null;
  @Input() showAsModal: boolean = false;
  @Output() closeModal = new EventEmitter<void>();
  @Output() upgradeRequested = new EventEmitter<string>();

  constructor(private router: Router) {}

  get moduleName(): string {
    return this.moduleInfo?.name ?? 'this module';
  }

  get hasAddonPricing(): boolean {
    return !!(this.moduleInfo?.addon_price_per_site || this.moduleInfo?.addon_price_per_org);
  }

  get addonPriceDisplay(): string {
    if (this.moduleInfo?.addon_price_per_site) {
      return '£' + this.moduleInfo.addon_price_per_site + '/site/month';
    }
    if (this.moduleInfo?.addon_price_per_org) {
      return '£' + this.moduleInfo.addon_price_per_org + '/month';
    }
    return '';
  }

  onClose(): void {
    this.closeModal.emit();
  }

  onUpgradeClick(): void {
    if (this.moduleInfo?.code) {
      this.upgradeRequested.emit(this.moduleInfo.code);
    }
    this.router.navigate(['/subscription/upgrade']);
  }

  onViewPlans(): void {
    this.router.navigate(['/pricing']);
  }
}
