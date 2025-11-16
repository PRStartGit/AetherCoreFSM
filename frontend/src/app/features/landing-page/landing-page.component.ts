import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {

  constructor(private router: Router) {}

  ngOnInit(): void {
    // Component initialization
  }

  /**
   * Handle Fife trial claim button click
   */
  claimFifeTrial(): void {
    // TODO: Implement Fife-specific trial signup flow
    // For now, redirect to standard trial signup with Fife flag
    console.log('Claiming Fife free trial (6 months)');
    this.startTrial('professional', true);
  }

  /**
   * Handle trial start for specific plan
   * @param plan - starter, professional, or enterprise
   * @param isFifeTrial - whether this is a Fife 6-month trial
   */
  startTrial(plan: string, isFifeTrial: boolean = false): void {
    console.log(`Starting trial for plan: ${plan}${isFifeTrial ? ' (Fife 6-month trial)' : ''}`);

    // TODO: Implement trial signup modal/page
    // For now, show alert with plan details
    const trialDuration = isFifeTrial ? '6 months' : 'Standard trial period';
    alert(`Starting ${plan} plan trial!\n\nDuration: ${trialDuration}\n\nThis will redirect to the signup form.`);

    // Future implementation:
    // - Open modal with signup form
    // - Collect: Name, Email, Company Name, Number of Sites, Phone (optional)
    // - Submit to backend API
    // - Redirect to confirmation page
    // this.router.navigate(['/signup'], { queryParams: { plan, fifeTrial: isFifeTrial } });
  }

  /**
   * Handle contact sales button click for Enterprise plan
   */
  contactSales(): void {
    console.log('Contact Sales clicked');

    // TODO: Implement contact sales modal/page
    // For now, show alert
    alert('Contact Sales\n\nThis will open a contact form where you can:\n- Provide your details\n- Specify number of sites\n- Describe your requirements\n\nOur sales team will contact you within 24 hours.');

    // Future implementation:
    // - Open modal with contact form
    // - Collect: Name, Email, Company Name, Number of Sites, Phone, Message
    // - Submit to backend API
    // - Redirect to thank you page
    // this.router.navigate(['/contact-sales']);
  }

  /**
   * Navigate to login page
   */
  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }

  /**
   * Navigate to dashboard (will redirect to appropriate dashboard based on user role)
   */
  navigateToDashboard(): void {
    // If user is already logged in, AuthGuard will handle routing to the correct dashboard
    // Otherwise, will redirect to login page
    this.router.navigate(['/login']);
  }

}
