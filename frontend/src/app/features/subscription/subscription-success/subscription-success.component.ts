import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { BillingService } from '../../../core/services/billing.service';
import { SubscriptionService } from '../../../core/services/subscription.service';

@Component({
  selector: 'app-subscription-success',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="success-container">
      <div class="success-card" *ngIf="!loading && !error">
        <div class="success-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12zm13.36-1.814a.75.75 0 10-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 00-1.06 1.06l2.25 2.25a.75.75 0 001.14-.094l3.75-5.25z" clip-rule="evenodd" />
          </svg>
        </div>
        <h1>Subscription Activated!</h1>
        <p class="message">Your subscription has been successfully set up.</p>

        <div class="details" *ngIf="subscriptionDetails">
          <div class="detail-row">
            <span class="label">Package:</span>
            <span class="value">{{ subscriptionDetails.package }}</span>
          </div>
          <div class="detail-row">
            <span class="label">Amount:</span>
            <span class="value">£{{ subscriptionDetails.amount }}/{{ subscriptionDetails.interval }}</span>
          </div>
        </div>

        <p class="next-steps">Your first payment will be collected automatically via Direct Debit.</p>

        <button class="btn-primary" (click)="goToDashboard()">Go to Dashboard</button>
      </div>

      <div class="loading-card" *ngIf="loading">
        <div class="spinner"></div>
        <p>Setting up your subscription...</p>
      </div>

      <div class="error-card" *ngIf="error">
        <div class="error-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-1.72 6.97a.75.75 0 10-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 101.06 1.06L12 13.06l1.72 1.72a.75.75 0 101.06-1.06L13.06 12l1.72-1.72a.75.75 0 10-1.06-1.06L12 10.94l-1.72-1.72z" clip-rule="evenodd" />
          </svg>
        </div>
        <h1>Something went wrong</h1>
        <p class="message">{{ errorMessage }}</p>
        <button class="btn-secondary" (click)="retry()">Try Again</button>
        <button class="btn-link" (click)="goToDashboard()">Return to Dashboard</button>
      </div>
    </div>
  `,
  styles: [`
    .success-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      padding: 20px;
    }

    .success-card, .loading-card, .error-card {
      background: white;
      border-radius: 16px;
      padding: 48px;
      text-align: center;
      max-width: 480px;
      width: 100%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    .success-icon {
      width: 80px;
      height: 80px;
      margin: 0 auto 24px;
      color: #10b981;
    }

    .success-icon svg {
      width: 100%;
      height: 100%;
    }

    .error-icon {
      width: 80px;
      height: 80px;
      margin: 0 auto 24px;
      color: #ef4444;
    }

    .error-icon svg {
      width: 100%;
      height: 100%;
    }

    h1 {
      font-size: 28px;
      font-weight: 700;
      color: #1f2937;
      margin: 0 0 12px;
    }

    .message {
      color: #6b7280;
      font-size: 16px;
      margin: 0 0 24px;
    }

    .details {
      background: #f9fafb;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 24px;
    }

    .detail-row {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
    }

    .detail-row:not(:last-child) {
      border-bottom: 1px solid #e5e7eb;
    }

    .label {
      color: #6b7280;
    }

    .value {
      font-weight: 600;
      color: #1f2937;
    }

    .next-steps {
      color: #6b7280;
      font-size: 14px;
      margin-bottom: 24px;
    }

    .btn-primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 14px 32px;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .btn-primary:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    .btn-secondary {
      background: #f3f4f6;
      color: #374151;
      border: none;
      padding: 14px 32px;
      border-radius: 8px;
      font-size: 16px;
      font-weight: 600;
      cursor: pointer;
      margin-right: 12px;
    }

    .btn-link {
      background: none;
      border: none;
      color: #6b7280;
      font-size: 14px;
      cursor: pointer;
      text-decoration: underline;
    }

    .spinner {
      width: 48px;
      height: 48px;
      border: 4px solid #e5e7eb;
      border-top-color: #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 0 auto 24px;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  `]
})
export class SubscriptionSuccessComponent implements OnInit {
  loading = true;
  error = false;
  errorMessage = '';
  subscriptionDetails: any = null;

  private redirectFlowId: string | null = null;
  private sessionToken: string | null = null;
  private packageId: number | null = null;
  private billingCycle: string = 'monthly';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private billingService: BillingService,
    private subscriptionService: SubscriptionService
  ) {}

  ngOnInit(): void {
    // Get query params from GoCardless redirect
    this.route.queryParams.subscribe(params => {
      this.redirectFlowId = params['redirect_flow_id'];

      // Get stored session data
      const sessionData = sessionStorage.getItem('checkout_session');
      if (sessionData) {
        const data = JSON.parse(sessionData);
        this.sessionToken = data.session_token;
        this.packageId = data.package_id;
        this.billingCycle = data.billing_cycle || 'monthly';
      }

      if (this.redirectFlowId && this.sessionToken && this.packageId) {
        this.completeCheckout();
      } else {
        this.loading = false;
        this.error = true;
        this.errorMessage = 'Missing checkout information. Please try again.';
      }
    });
  }

  completeCheckout(): void {
    this.billingService.completeCheckout(
      this.redirectFlowId!,
      this.sessionToken!,
      this.packageId!,
      this.billingCycle
    ).subscribe({
      next: (result) => {
        this.loading = false;
        this.subscriptionDetails = result;
        // Clear session storage
        sessionStorage.removeItem('checkout_session');
        // Refresh module access
        this.subscriptionService.clearModuleAccessCache();
      },
      error: (err) => {
        this.loading = false;
        this.error = true;
        this.errorMessage = err.error?.detail || 'Failed to complete subscription setup.';
      }
    });
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }

  retry(): void {
    this.router.navigate(['/subscription/upgrade']);
  }
}
