import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { UserRole } from '../../core/models';

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {
  // Subscription toggle state
  isAnnual: boolean = false;

  // Authentication state
  isLoggedIn: boolean = false;

  // Mobile menu state
  isMobileMenuOpen: boolean = false;

  // FAQ state - tracks which FAQ item is open (null = all closed)
  openFaqIndex: number | null = null;

  // Pricing data
  pricingPlans = {
    starter: {
      name: 'Starter',
      description: 'Perfect for independent venues',
      monthlyPrice: 12,
      annualPrice: 10.20,
      siteRange: '1-3 sites',
      features: [
        'Mobile app access',
        'Digital safety checklists',
        'Photo upload & evidence',
        'Email reports',
        'Basic support',
        'Unlimited users',
        'Cloud storage',
        'EHO inspection ready'
      ]
    },
    professional: {
      name: 'Professional',
      description: 'For growing restaurant groups',
      monthlyPrice: 10,
      annualPrice: 8.50,
      siteRange: '4-10 sites',
      popular: true,
      features: [
        'Everything in Starter, plus:',
        'Documents module',
        'Priority support',
        'Custom branding',
        'Advanced analytics',
        'Multi-site dashboard',
        'Staff training tracking'
      ]
    },
    enterprise: {
      name: 'Enterprise',
      description: 'For large hospitality groups',
      monthlyPrice: 8,
      annualPrice: 6.80,
      siteRange: '11+ sites',
      features: [
        'Everything in Pro, plus:',
        'E-learning module',
        'Dedicated account manager',
        'API access',
        'Custom integrations',
        'Advanced permissions',
        'SLA guarantee',
        'Onboarding assistance'
      ]
    }
  };

  constructor(
    private router: Router,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // Subscribe to authentication state changes
    this.authService.authState$.subscribe(state => {
      this.isLoggedIn = state.isAuthenticated;
    });
  }

  /**
   * Toggle between monthly and annual billing
   */
  toggleBilling(): void {
    this.isAnnual = !this.isAnnual;
  }

  /**
   * Get price for a plan based on billing period
   */
  getPrice(plan: 'starter' | 'professional' | 'enterprise'): number {
    return this.isAnnual
      ? this.pricingPlans[plan].annualPrice
      : this.pricingPlans[plan].monthlyPrice;
  }

  /**
   * Calculate savings percentage
   */
  getSavings(plan: 'starter' | 'professional' | 'enterprise'): number {
    const monthly = this.pricingPlans[plan].monthlyPrice;
    const annual = this.pricingPlans[plan].annualPrice;
    return Math.round(((monthly - annual) / monthly) * 100);
  }

  /**
   * Handle Fife trial claim button click
   */
  claimFifeTrial(): void {
    console.log('Claiming Fife free trial (6 months)');
    this.startTrial('professional', true);
  }

  /**
   * Handle trial start for specific plan
   */
  startTrial(plan: string, isFifeTrial: boolean = false): void {
    console.log(`Starting trial for plan: ${plan}${isFifeTrial ? ' (Fife 6-month trial)' : ''}`);
    const trialDuration = isFifeTrial ? '6 months' : 'Standard trial period';
    alert(`Starting ${plan} plan trial!\n\nDuration: ${trialDuration}\n\nThis will redirect to the signup form.`);
  }

  /**
   * Handle contact sales button click for Enterprise plan
   */
  contactSales(): void {
    console.log('Contact Sales clicked');
    alert('Contact Sales\n\nThis will open a contact form where you can:\n- Provide your details\n- Specify number of sites\n- Describe your requirements\n\nOur sales team will contact you within 24 hours.');
  }

  /**
   * Navigate to login page
   */
  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }

  /**
   * Navigate to register page
   */
  navigateToRegister(): void {
    this.router.navigate(['/register']);
  }

  /**
   * Navigate to dashboard based on user role
   */
  navigateToDashboard(): void {
    const user = this.authService.getUser();
    if (!user) {
      this.router.navigate(['/login']);
      return;
    }

    // Navigate to appropriate dashboard based on user role
    switch (user.role) {
      case UserRole.SUPER_ADMIN:
        this.router.navigate(['/super-admin']);
        break;
      case UserRole.ORG_ADMIN:
        this.router.navigate(['/org-admin']);
        break;
      case UserRole.SITE_USER:
        this.router.navigate(['/site-user']);
        break;
      default:
        this.router.navigate(['/login']);
    }
  }

  /**
   * Toggle mobile menu open/closed
   */
  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  /**
   * Close mobile menu
   */
  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }

  /**
   * Toggle FAQ item open/closed
   * If clicking the same item, close it. If clicking a different item, open that one.
   */
  toggleFaq(index: number): void {
    this.openFaqIndex = this.openFaqIndex === index ? null : index;
  }

}
