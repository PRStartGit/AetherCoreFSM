import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../core/auth/auth.service';
import { UserRole } from '../../core/models';
import { SubscriptionService, PricingResponse, SubscriptionPackage } from '../../core/services/subscription.service';

interface PricingPlan {
  name: string;
  description: string;
  monthlyPrice: number;
  annualPrice: number;
  siteRange: string;
  features: string[];
  limitations?: string[];
  popular?: boolean;
}

@Component({
  selector: 'app-landing-page',
  templateUrl: './landing-page.component.html',
  styleUrls: ['./landing-page.component.scss']
})
export class LandingPageComponent implements OnInit {
  isAnnual: boolean = false;
  isLoggedIn: boolean = false;
  isMobileMenuOpen: boolean = false;
  openFaqIndex: number | null = null;
  pricingLoading: boolean = true;

  pricingPlans: { [key: string]: PricingPlan } = {
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
      description: 'Perfect for 2-3 sites',
      monthlyPrice: 29,
      annualPrice: 24,
      siteRange: '2-3 sites',
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
      monthlyPrice: 79,
      annualPrice: 66,
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
      monthlyPrice: 149,
      annualPrice: 124,
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
    private authService: AuthService,
    private subscriptionService: SubscriptionService
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.isLoggedIn = state.isAuthenticated;
    });
    this.loadPricingData();
  }

  loadPricingData(): void {
    this.pricingLoading = true;
    this.subscriptionService.getPricing().subscribe({
      next: (response: PricingResponse) => {
        this.mapPricingResponse(response);
        this.pricingLoading = false;
      },
      error: (error) => {
        console.error('Failed to load pricing data:', error);
        this.pricingLoading = false;
      }
    });
  }

  private mapPricingResponse(response: PricingResponse): void {
    response.tiers.forEach((tier) => {
      const code = tier.code.toLowerCase();

      this.pricingPlans[code] = {
        name: tier.name,
        description: tier.description || this.pricingPlans[code]?.description || '',
        monthlyPrice: tier.monthly_price,
        annualPrice: tier.annual_price || Math.round(tier.monthly_price * 0.83 * 100) / 100,
        siteRange: tier.site_range,
        features: tier.features.length > 0 ? tier.features : (this.pricingPlans[code]?.features || []),
        limitations: this.pricingPlans[code]?.limitations || [],
        popular: tier.is_popular
      };
    });
  }

  toggleBilling(): void {
    this.isAnnual = !this.isAnnual;
  }

  getPrice(plan: string): number {
    const planData = this.pricingPlans[plan];
    if (!planData) return 0;
    return this.isAnnual ? planData.annualPrice : planData.monthlyPrice;
  }

  getSavings(plan: string): number {
    const planData = this.pricingPlans[plan];
    if (!planData) return 0;
    const monthly = planData.monthlyPrice;
    const annual = planData.annualPrice;
    if (monthly === 0) return 0;
    return Math.round(((monthly - annual) / monthly) * 100);
  }

  getAnnualSavings(plan: string): number {
    const planData = this.pricingPlans[plan];
    if (!planData) return 0;
    const monthly = planData.monthlyPrice;
    const annual = planData.annualPrice;
    return Math.round((monthly - annual) * 12 * 100) / 100;
  }

  claimFifeTrial(): void {
    this.startTrial('professional', true);
  }

  startTrial(plan: string, isFifeTrial: boolean = false): void {
    const trialDuration = isFifeTrial ? '6 months' : 'Standard trial period';
    alert('Starting ' + plan + ' plan trial! Duration: ' + trialDuration);
  }

  contactSales(): void {
    alert('Contact Sales - Our sales team will contact you within 24 hours.');
  }

  navigateToLogin(): void {
    this.router.navigate(['/login']);
  }

  navigateToRegister(): void {
    this.router.navigate(['/register']);
  }

  navigateToDashboard(): void {
    const user = this.authService.getUser();
    if (!user) {
      this.router.navigate(['/login']);
      return;
    }
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

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }

  closeMobileMenu(): void {
    this.isMobileMenuOpen = false;
  }

  toggleFaq(index: number): void {
    this.openFaqIndex = this.openFaqIndex === index ? null : index;
  }
}
