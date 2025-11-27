import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { SubscriptionService, SubscriptionPackage } from '../../../core/services/subscription.service';
import { BillingService } from '../../../core/services/billing.service';

@Component({
  selector: 'app-subscription-upgrade',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="upgrade-container">
      <div class="upgrade-header">
        <button class="back-btn" (click)="goBack()">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          Back
        </button>
        <h1>Choose Your Plan</h1>
        <p>Select the plan that best fits your organization's needs</p>

        <div class="billing-toggle">
          <button
            [class.active]="billingCycle === 'monthly'"
            (click)="billingCycle = 'monthly'"
          >
            Monthly
          </button>
          <button
            [class.active]="billingCycle === 'annual'"
            (click)="billingCycle = 'annual'"
          >
            Annual
            <span class="save-badge">Save 17%</span>
          </button>
        </div>
      </div>

      <div class="packages-grid" *ngIf="!loading">
        <div
          class="package-card"
          *ngFor="let pkg of packages"
          [class.popular]="pkg.code === 'professional'"
          [class.current]="pkg.id === currentPackageId"
        >
          <div class="popular-badge" *ngIf="pkg.code === 'professional'">Most Popular</div>
          <div class="current-badge" *ngIf="pkg.id === currentPackageId">Current Plan</div>

          <h2>{{ pkg.name }}</h2>
          <p class="description">{{ pkg.description }}</p>

          <div class="price">
            <span class="amount">
              £{{ billingCycle === 'annual' && pkg.annual_price ? pkg.annual_price : pkg.monthly_price }}
            </span>
            <span class="period">/{{ billingCycle === 'annual' ? 'year' : 'month' }}</span>
          </div>

          <div class="limits">
            <div class="limit">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              {{ pkg.max_sites === -1 ? 'Unlimited' : pkg.max_sites }} Users
            </div>
            <div class="limit">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
                <polyline points="9 22 9 12 15 12 15 22"/>
              </svg>
              {{ pkg.max_sites === -1 ? 'Unlimited' : pkg.max_sites }} Sites
            </div>
          </div>

          <ul class="features">
            <li *ngFor="let feature of getFeatures(pkg.code)">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              {{ feature }}
            </li>
          </ul>

          <button
            class="select-btn"
            [class.primary]="pkg.code === 'professional'"
            [disabled]="pkg.id === currentPackageId || pkg.monthly_price === 0 || processing"
            (click)="selectPackage(pkg)"
          >
            <span *ngIf="pkg.id === currentPackageId">Current Plan</span>
            <span *ngIf="pkg.id !== currentPackageId && pkg.monthly_price === 0">Free</span>
            <span *ngIf="pkg.id !== currentPackageId && pkg.monthly_price > 0 && !processing">
              Get Started
            </span>
            <span *ngIf="processing && selectedPackageId === pkg.id">Processing...</span>
          </button>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        <div class="spinner"></div>
        <p>Loading plans...</p>
      </div>

      <div class="footer-note">
        <p>All plans include a 14-day money-back guarantee. Payments are processed securely via Direct Debit.</p>
      </div>
    </div>
  `,
  styles: [`
    .upgrade-container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 32px 24px;
    }

    .back-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: none;
      border: none;
      color: #6b7280;
      font-size: 14px;
      cursor: pointer;
      margin-bottom: 16px;
      padding: 0;
    }

    .back-btn:hover {
      color: #374151;
    }

    .upgrade-header {
      text-align: center;
      margin-bottom: 48px;
    }

    .upgrade-header h1 {
      font-size: 36px;
      font-weight: 700;
      color: #1f2937;
      margin: 0 0 12px;
    }

    .upgrade-header p {
      color: #6b7280;
      font-size: 18px;
      margin: 0 0 32px;
    }

    .billing-toggle {
      display: inline-flex;
      background: #f3f4f6;
      border-radius: 8px;
      padding: 4px;
    }

    .billing-toggle button {
      background: none;
      border: none;
      padding: 10px 24px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 500;
      color: #6b7280;
      cursor: pointer;
      transition: all 0.2s;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .billing-toggle button.active {
      background: white;
      color: #1f2937;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .save-badge {
      background: #10b981;
      color: white;
      font-size: 11px;
      padding: 2px 6px;
      border-radius: 4px;
    }

    .packages-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
      margin-bottom: 48px;
    }

    .package-card {
      background: white;
      border-radius: 16px;
      padding: 32px;
      position: relative;
      border: 2px solid #e5e7eb;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .package-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }

    .package-card.popular {
      border-color: #667eea;
    }

    .package-card.current {
      border-color: #10b981;
    }

    .popular-badge {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 4px 16px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
    }

    .current-badge {
      position: absolute;
      top: -12px;
      right: 16px;
      background: #10b981;
      color: white;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
    }

    .package-card h2 {
      font-size: 24px;
      font-weight: 700;
      color: #1f2937;
      margin: 0 0 8px;
    }

    .description {
      color: #6b7280;
      font-size: 14px;
      margin: 0 0 24px;
    }

    .price {
      margin-bottom: 24px;
    }

    .price .amount {
      font-size: 48px;
      font-weight: 700;
      color: #1f2937;
    }

    .price .period {
      color: #6b7280;
      font-size: 16px;
    }

    .limits {
      display: flex;
      gap: 16px;
      margin-bottom: 24px;
      padding-bottom: 24px;
      border-bottom: 1px solid #e5e7eb;
    }

    .limit {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #6b7280;
      font-size: 14px;
    }

    .limit svg {
      color: #9ca3af;
    }

    .features {
      list-style: none;
      padding: 0;
      margin: 0 0 24px;
    }

    .features li {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 8px 0;
      color: #374151;
      font-size: 14px;
    }

    .features li svg {
      color: #10b981;
      flex-shrink: 0;
    }

    .select-btn {
      width: 100%;
      padding: 14px;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
      background: #f3f4f6;
      color: #374151;
      border: none;
    }

    .select-btn.primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }

    .select-btn:hover:not(:disabled) {
      transform: translateY(-1px);
    }

    .select-btn.primary:hover:not(:disabled) {
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    .select-btn:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .loading {
      text-align: center;
      padding: 60px;
    }

    .spinner {
      width: 40px;
      height: 40px;
      border: 3px solid #e5e7eb;
      border-top-color: #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 16px;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .footer-note {
      text-align: center;
    }

    .footer-note p {
      color: #9ca3af;
      font-size: 14px;
    }
  `]
})
export class SubscriptionUpgradeComponent implements OnInit {
  packages: SubscriptionPackage[] = [];
  loading = true;
  processing = false;
  billingCycle: 'monthly' | 'annual' = 'monthly';
  currentPackageId: number | null = null;
  selectedPackageId: number | null = null;

  private featuresByPlan: { [key: string]: string[] } = {
    'free': [
      'Basic task management',
      'Single site',
      'Email support'
    ],
    'starter': [
      'All Free features',
      'Multiple sites',
      'Checklist management',
      'Basic reporting',
      'Email & chat support'
    ],
    'professional': [
      'All Starter features',
      'Advanced reporting',
      'Recipe management',
      'Training module',
      'Priority support',
      'API access'
    ],
    'enterprise': [
      'All Professional features',
      'Unlimited everything',
      'Custom integrations',
      'Dedicated account manager',
      'SLA guarantee',
      'On-premise option'
    ]
  };

  constructor(
    private router: Router,
    private subscriptionService: SubscriptionService,
    private billingService: BillingService
  ) {}

  ngOnInit(): void {
    this.loadPackages();
    this.loadCurrentPlan();
  }

  loadPackages(): void {
    this.subscriptionService.getPackages().subscribe({
      next: (packages) => {
        this.packages = packages.filter(p => p.is_active).sort((a, b) => a.display_order - b.display_order);
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  loadCurrentPlan(): void {
    this.billingService.getSubscriptionStatus().subscribe({
      next: (status) => {
        this.currentPackageId = status.package?.id || null;
      }
    });
  }

  getFeatures(code: string): string[] {
    return this.featuresByPlan[code] || [];
  }

  goBack(): void {
    this.router.navigate(['/subscription/manage']);
  }

  selectPackage(pkg: SubscriptionPackage): void {
    if (pkg.monthly_price === 0) return;

    this.processing = true;
    this.selectedPackageId = pkg.id;

    this.billingService.startCheckout(pkg.id, this.billingCycle).subscribe({
      next: (response) => {
        // Store session data for completion
        sessionStorage.setItem('checkout_session', JSON.stringify({
          session_token: response.session_token,
          package_id: pkg.id,
          billing_cycle: this.billingCycle
        }));

        // Redirect to GoCardless
        window.location.href = response.redirect_url;
      },
      error: () => {
        this.processing = false;
        this.selectedPackageId = null;
      }
    });
  }
}
