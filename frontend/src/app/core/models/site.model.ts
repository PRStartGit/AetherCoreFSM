export interface Site {
  id: number;
  name: string;
  site_code: string;
  organization_id: number;
  organization_name?: string;
  address: string;
  city: string;
  postcode: string;
  country: string;
  is_active: boolean;
  daily_report_enabled?: boolean;
  daily_report_time?: string;
  weekly_report_enabled?: boolean;
  weekly_report_day?: number;
  weekly_report_time?: string;
  report_recipients?: string;
  created_at: string;
  updated_at: string;
}

export interface SiteCreate {
  name: string;
  site_code: string;
  organization_id: number;
  address: string;
  city: string;
  postcode: string;
  country?: string;
  daily_report_enabled?: boolean;
  daily_report_time?: string;
  weekly_report_enabled?: boolean;
  weekly_report_day?: number;
  weekly_report_time?: string;
  report_recipients?: string;
}

export interface SiteUpdate {
  name?: string;
  site_code?: string;
  organization_id?: number;
  address?: string;
  city?: string;
  postcode?: string;
  country?: string;
  is_active?: boolean;
  daily_report_enabled?: boolean;
  daily_report_time?: string;
  weekly_report_enabled?: boolean;
  weekly_report_day?: number;
  weekly_report_time?: string;
  report_recipients?: string;
}
