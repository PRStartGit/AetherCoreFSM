import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-subscription-cancelled',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="cancelled-container">
      <div class="cancelled-card">
        <div class="cancelled-icon">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
            <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25zm-1.72 6.97a.75.75 0 10-1.06 1.06L10.94 12l-1.72 1.72a.75.75 0 101.06 1.06L12 13.06l1.72 1.72a.75.75 0 101.06-1.06L13.06 12l1.72-1.72a.75.75 0 10-1.06-1.06L12 10.94l-1.72-1.72z" clip-rule="evenodd" />
          </svg>
        </div>
        <h1>Checkout Cancelled</h1>
        <p class="message">You've cancelled the checkout process. No payment has been taken.</p>

        <p class="help-text">
          If you experienced any issues or have questions about our plans,
          please don't hesitate to contact our support team.
        </p>

        <div class="actions">
          <button class="btn-primary" (click)="tryAgain()">Try Again</button>
          <button class="btn-secondary" (click)="goToDashboard()">Return to Dashboard</button>
        </div>

        <a class="contact-link" href="mailto:support@zynthio.com">Contact Support</a>
      </div>
    </div>
  `,
  styles: [`
    .cancelled-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #6b7280 0%, #374151 100%);
      padding: 20px;
    }

    .cancelled-card {
      background: white;
      border-radius: 16px;
      padding: 48px;
      text-align: center;
      max-width: 480px;
      width: 100%;
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }

    .cancelled-icon {
      width: 80px;
      height: 80px;
      margin: 0 auto 24px;
      color: #9ca3af;
    }

    .cancelled-icon svg {
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
      margin: 0 0 16px;
    }

    .help-text {
      color: #9ca3af;
      font-size: 14px;
      margin-bottom: 32px;
    }

    .actions {
      display: flex;
      gap: 12px;
      justify-content: center;
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
      transition: background 0.2s;
    }

    .btn-secondary:hover {
      background: #e5e7eb;
    }

    .contact-link {
      color: #667eea;
      font-size: 14px;
      text-decoration: none;
    }

    .contact-link:hover {
      text-decoration: underline;
    }
  `]
})
export class SubscriptionCancelledComponent {
  constructor(private router: Router) {}

  tryAgain(): void {
    this.router.navigate(['/subscription/upgrade']);
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }
}
