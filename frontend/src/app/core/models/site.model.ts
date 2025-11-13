export interface Site {
  id: number;
  name: string;
  organization_id: number;
  address: string;
  postcode: string;
  site_type: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface SiteCreate {
  name: string;
  organization_id: number;
  address: string;
  postcode: string;
  site_type: string;
}

export interface SiteUpdate {
  name?: string;
  address?: string;
  postcode?: string;
  site_type?: string;
  is_active?: boolean;
}
