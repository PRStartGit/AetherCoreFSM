export interface Organization {
  id: number;
  name: string;
  slug: string;
  contact_email: string;
  subscription_tier: string;
  subscription_status: string;
  max_sites: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface OrganizationCreate {
  name: string;
  slug: string;
  contact_email: string;
  subscription_tier?: string;
  max_sites?: number;
}

export interface OrganizationUpdate {
  name?: string;
  contact_email?: string;
  subscription_tier?: string;
  subscription_status?: string;
  max_sites?: number;
  is_active?: boolean;
}
