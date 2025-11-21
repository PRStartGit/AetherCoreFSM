export interface Organization {
  id: number;
  name: string;
  org_id: string;
  contact_person?: string;
  contact_email: string;
  contact_phone?: string;
  address?: string;
  subscription_tier: string;
  subscription_status: string;
  subscription_end_date?: string;
  custom_price_per_site?: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface OrganizationCreate {
  name: string;
  org_id: string;
  contact_person?: string;
  contact_email: string;
  contact_phone?: string;
  address?: string;
  subscription_tier?: string;
  custom_price_per_site?: number;
}

export interface OrganizationUpdate {
  name?: string;
  contact_person?: string;
  contact_email?: string;
  contact_phone?: string;
  address?: string;
  subscription_tier?: string;
  subscription_status?: string;
  subscription_end_date?: string;
  custom_price_per_site?: number;
  is_active?: boolean;
}
