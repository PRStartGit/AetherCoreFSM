import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


export interface CheckoutResponse {
  redirect_url: string;
  session_token: string;
}

export interface SubscriptionStatus {
  organization_id: number;
  organization_name: string;
  is_trial: boolean;
  has_mandate: boolean;
  has_subscription: boolean;
  package: {
    id: number;
    name: string;
    code: string;
    monthly_price: number;
    annual_price: number | null;
  } | null;
}

export interface CompleteCheckoutResponse {
  success: boolean;
  subscription_id: string;
  package: string;
  amount: number;
  interval: string;
}

@Injectable({
  providedIn: 'root'
})
export class BillingService {
  private readonly API_URL = '/api/v1/billing';

  constructor(private http: HttpClient) {}

  startCheckout(packageId: number, billingCycle: string = 'monthly'): Observable<CheckoutResponse> {
    return this.http.post<CheckoutResponse>(`${this.API_URL}/checkout`, {
      package_id: packageId,
      billing_cycle: billingCycle
    });
  }

  completeCheckout(
    redirectFlowId: string,
    sessionToken: string,
    packageId: number,
    billingCycle: string = 'monthly'
  ): Observable<CompleteCheckoutResponse> {
    return this.http.post<CompleteCheckoutResponse>(
      `${this.API_URL}/checkout/complete?package_id=${packageId}&billing_cycle=${billingCycle}`,
      {
        redirect_flow_id: redirectFlowId,
        session_token: sessionToken
      }
    );
  }

  getSubscriptionStatus(): Observable<SubscriptionStatus> {
    return this.http.get<SubscriptionStatus>(`${this.API_URL}/subscription`);
  }

  cancelSubscription(): Observable<{ success: boolean; message: string }> {
    return this.http.post<{ success: boolean; message: string }>(
      `${this.API_URL}/subscription/cancel`,
      {}
    );
  }
}
