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
  }

  acceptNecessary(): void {
    localStorage.setItem('cookieConsent', 'necessary');
    this.showBanner = false;
    // Disable Google Analytics if only necessary cookies are accepted
    if (typeof window !== 'undefined' && (window as any).gtag) {
      (window as any).gtag('consent', 'update', {
        'analytics_storage': 'denied'
      });
    }
  }

  openPrivacyPolicy(): void {
    window.open('/privacy', '_blank');
  }
}
