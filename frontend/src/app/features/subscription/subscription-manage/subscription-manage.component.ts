import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { BillingService, SubscriptionStatus } from '../../../core/services/billing.service';
import { SubscriptionService } from '../../../core/services/subscription.service';

@Component({
  selector: 'app-subscription-manage',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="manage-container">
      <div class="manage-header">
        <h1>Subscription Management</h1>
        <p>Manage your Zynthio subscription and billing</p>
      </div>

      <div class="content" *ngIf="!loading">
        <!-- Current Plan -->
        <div class="card current-plan">
          <h2>Current Plan</h2>

          <div class="plan-details" *ngIf="status">
            <div class="plan-badge" [class.trial]="status.is_trial">
              {{ status.is_trial ? 'Trial' : 'Active' }}
            </div>

            <div class="plan-name">
              {{ status.package?.name || 'Free Plan' }}
            </div>

            <div class="plan-price" *ngIf="status.package">
              £{{ status.package.monthly_price }}/month
            </div>

            <div class="plan-info">
              <div class="info-row">
                <span class="label">Organization:</span>
                <span class="value">{{ status.organization_name }}</span>
              </div>
              <div class="info-row">
                <span class="label">Direct Debit:</span>
                <span class="value" [class.active]="status.has_mandate">
                  {{ status.has_mandate ? 'Active' : 'Not Set Up' }}
                </span>
              </div>
              <div class="info-row">
                <span class="label">Subscription:</span>
                <span class="value" [class.active]="status.has_subscription">
                  {{ status.has_subscription ? 'Active' : 'Inactive' }}
                </span>
              </div>
            </div>
          </div>

          <div class="plan-actions">
            <button class="btn-primary" *ngIf="!status?.has_subscription" (click)="upgrade()">
              Upgrade Plan
            </button>
            <button class="btn-secondary" *ngIf="status?.has_subscription" (click)="upgrade()">
              Change Plan
            </button>
          </div>
        </div>

        <!-- Billing History placeholder -->
        <div class="card billing-history">
          <h2>Billing</h2>
          <p class="placeholder-text">
            Your payments are managed securely through GoCardless Direct Debit.
            Payment receipts will be sent to your registered email address.
          </p>
        </div>

        <!-- Cancel Subscription -->
        <div class="card danger-zone" *ngIf="status?.has_subscription">
          <h2>Cancel Subscription</h2>
          <p>
            If you cancel your subscription, you'll lose access to premium features
            at the end of your current billing period.
          </p>
          <button class="btn-danger" (click)="confirmCancel()" [disabled]="cancelling">
            {{ cancelling ? 'Cancelling...' : 'Cancel Subscription' }}
          </button>
        </div>
      </div>

      <div class="loading" *ngIf="loading">
        <div class="spinner"></div>
        <p>Loading subscription details...</p>
      </div>

      <!-- Cancel Confirmation Modal -->
      <div class="modal-overlay" *ngIf="showCancelModal" (click)="showCancelModal = false">
        <div class="modal" (click)="$event.stopPropagation()">
          <h3>Cancel Subscription?</h3>
          <p>Are you sure you want to cancel your subscription? You'll lose access to:</p>
          <ul>
            <li>Premium modules and features</li>
            <li>Priority support</li>
            <li>Advanced reporting</li>
          </ul>
          <div class="modal-actions">
            <button class="btn-secondary" (click)="showCancelModal = false">Keep Subscription</button>
            <button class="btn-danger" (click)="cancelSubscription()">Yes, Cancel</button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .manage-container {
      max-width: 800px;
      margin: 0 auto;
      padding: 32px 24px;
    }

    .manage-header {
      margin-bottom: 32px;
    }

    .manage-header h1 {
      font-size: 28px;
      font-weight: 700;
      color: #1f2937;
      margin: 0 0 8px;
    }

    .manage-header p {
      color: #6b7280;
      margin: 0;
    }

    .card {
      background: white;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .card h2 {
      font-size: 18px;
      font-weight: 600;
      color: #1f2937;
      margin: 0 0 16px;
    }

    .plan-details {
      margin-bottom: 24px;
    }

    .plan-badge {
      display: inline-block;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      text-transform: uppercase;
      background: #10b981;
      color: white;
      margin-bottom: 12px;
    }

    .plan-badge.trial {
      background: #f59e0b;
    }

    .plan-name {
      font-size: 24px;
      font-weight: 700;
      color: #1f2937;
      margin-bottom: 4px;
    }

    .plan-price {
      font-size: 18px;
      color: #6b7280;
      margin-bottom: 20px;
    }

    .plan-info {
      background: #f9fafb;
      border-radius: 8px;
      padding: 16px;
    }

    .info-row {
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
    }

    .info-row:not(:last-child) {
      border-bottom: 1px solid #e5e7eb;
    }

    .info-row .label {
      color: #6b7280;
    }

    .info-row .value {
      font-weight: 500;
      color: #1f2937;
    }

    .info-row .value.active {
      color: #10b981;
    }

    .plan-actions {
      display: flex;
      gap: 12px;
    }

    .btn-primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
    }

    .btn-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }

    .btn-secondary {
      background: #f3f4f6;
      color: #374151;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
    }

    .btn-secondary:hover {
      background: #e5e7eb;
    }

    .danger-zone {
      border: 1px solid #fecaca;
    }

    .danger-zone h2 {
      color: #dc2626;
    }

    .danger-zone p {
      color: #6b7280;
      margin-bottom: 16px;
    }

    .btn-danger {
      background: #dc2626;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
    }

    .btn-danger:hover:not(:disabled) {
      background: #b91c1c;
    }

    .btn-danger:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }

    .placeholder-text {
      color: #6b7280;
    }

    .loading {
      text-align: center;
      padding: 60px 20px;
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

    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }

    .modal {
      background: white;
      border-radius: 12px;
      padding: 24px;
      max-width: 400px;
      width: 90%;
    }

    .modal h3 {
      font-size: 18px;
      font-weight: 600;
      color: #1f2937;
      margin: 0 0 12px;
    }

    .modal p {
      color: #6b7280;
      margin-bottom: 12px;
    }

    .modal ul {
      color: #6b7280;
      margin: 0 0 20px;
      padding-left: 20px;
    }

    .modal-actions {
      display: flex;
      gap: 12px;
      justify-content: flex-end;
    }
  `]
})
export class SubscriptionManageComponent implements OnInit {
  loading = true;
  status: SubscriptionStatus | null = null;
  cancelling = false;
  showCancelModal = false;

  constructor(
    private router: Router,
    private billingService: BillingService,
    private subscriptionService: SubscriptionService
  ) {}

  ngOnInit(): void {
    this.loadStatus();
  }

  loadStatus(): void {
    this.billingService.getSubscriptionStatus().subscribe({
      next: (status) => {
        this.status = status;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      }
    });
  }

  upgrade(): void {
    this.router.navigate(['/subscription/upgrade']);
  }

  confirmCancel(): void {
    this.showCancelModal = true;
  }

  cancelSubscription(): void {
    this.showCancelModal = false;
    this.cancelling = true;

    this.billingService.cancelSubscription().subscribe({
      next: () => {
        this.cancelling = false;
        this.subscriptionService.clearModuleAccessCache();
        this.loadStatus();
      },
      error: () => {
        this.cancelling = false;
      }
    });
  }
}
