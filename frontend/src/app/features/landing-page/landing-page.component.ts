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
    free: {
      name: 'Free',
      description: 'Try Zynthio at no cost',
      monthlyPrice: 0,
      annualPrice: 0,
      siteRange: '1 site only',
      features: [
        'Mobile-friendly web access',
        'Digital checklists',
        'Temperature monitoring',
        'Photo upload',
        'Email reports',
        'Unlimited users',
        'Basic support'
      ],
      limitations: [
        'No Training module access',
        'No Recipes module access'
      ]
    },
    starter: {
      name: 'Starter',
      description: 'Perfect for 1-3 sites',
      monthlyPrice: 12,
      annualPrice: 10,
      siteRange: '1-3 sites',
      features: [
        'Everything in Free, plus:',
        'Multiple sites (up to 3)',
        'Training module access',
        'Recipes module access',
        'Defects tracking',
        'Advanced reporting',
        'Priority support'
      ]
    },
    professional: {
      name: 'Professional',
      description: 'Best for 4-10 sites',
      monthlyPrice: 10,
      annualPrice: 8.30,
      siteRange: '4-10 sites',
      popular: true,
      features: [
        'Everything in Starter, plus:',
        'Multiple sites (up to 10)',
        'Documents module',
        'Custom branding',
        'Advanced analytics',
        'Multi-site dashboard',
        'API access',
        'Priority email support'
      ]
    },
    enterprise: {
      name: 'Enterprise',
      description: 'For 11+ sites',
      monthlyPrice: 8,
      annualPrice: 6.70,
      siteRange: '11+ sites',
      features: [
        'Everything in Pro, plus:',
        'Unlimited sites',
        'Dedicated account manager',
        'Custom integrations',
        'SLA guarantee',
        'Onboarding assistance',
        'White-label options',
        '24/7 phone support'
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
  getPrice(plan: 'free' | 'starter' | 'professional' | 'enterprise'): number {
    return this.isAnnual
      ? this.pricingPlans[plan].annualPrice
      : this.pricingPlans[plan].monthlyPrice;
  }

  /**
   * Calculate savings percentage
   */
  getSavings(plan: 'free' | 'starter' | 'professional' | 'enterprise'): number {
    const monthly = this.pricingPlans[plan].monthlyPrice;
    const annual = this.pricingPlans[plan].annualPrice;
    if (monthly === 0) return 0;
    return Math.round(((monthly - annual) / monthly) * 100);
  }

  /**
   * Calculate annual savings in currency
   */
  getAnnualSavings(plan: 'free' | 'starter' | 'professional' | 'enterprise'): number {
    const monthly = this.pricingPlans[plan].monthlyPrice;
    const annual = this.pricingPlans[plan].annualPrice;
    return Math.round((monthly - annual) * 12 * 100) / 100;
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
