import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-cookie-consent',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cookie-consent.component.html',
  styleUrls: ['./cookie-consent.component.scss']
})
export class CookieConsentComponent implements OnInit {
  showBanner = false;

  ngOnInit(): void {
    // Check if user has already consented
    const consent = localStorage.getItem('cookieConsent');
    if (!consent) {
      this.showBanner = true;
    }
  }

  acceptAll(): void {
    localStorage.setItem('cookieConsent', 'all');
    this.showBanner = false;

    // Update Google Consent Mode v2 - grant all consent types
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('consent', 'update', {
        'analytics_storage': 'granted',
        'ad_storage': 'granted',
        'ad_user_data': 'granted',
        'ad_personalization': 'granted',
        'functionality_storage': 'granted',
        'personalization_storage': 'granted'
      });
    }
  }

  acceptNecessary(): void {
    localStorage.setItem('cookieConsent', 'necessary');
    this.showBanner = false;

    // Update Google Consent Mode v2 - deny all non-essential
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('consent', 'update', {
        'analytics_storage': 'denied',
        'ad_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied',
        'functionality_storage': 'denied',
        'personalization_storage': 'denied'
      });
    }
  }

  openPrivacyPolicy(): void {
    window.open('/privacy', '_blank');
  }
}
