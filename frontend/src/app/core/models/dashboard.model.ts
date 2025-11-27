export interface SuperAdminMetrics {
  total_organizations: number;
  total_sites: number;
  total_users: number;
  active_subscriptions: number;
  total_checklists_today?: number;
  checklists_today?: number;
  total_open_defects: number;
  total_active_checklists?: number;
  recent_activity: ActivityItem[];
  rag_summary: {
    green: number;
    amber: number;
    red: number;
  };
  org_performance: Array<{
    org_id: number;
    org_name: string;
    rag_status: string;
    completion_rate: number;
    open_defects: number;
    total_sites: number;
  }>;
  growth_data: Array<{
    month: string;
    organizations: number;
    sites: number;
    users: number;
  }>;
  subscription_summary: {
    [key: string]: number;
  };
  // New enhanced metrics
  revenue_metrics?: RevenueMetrics;
  user_engagement?: UserEngagement;
  module_adoption?: ModuleAdoption[];
  defect_trends?: DefectTrend[];
  top_sites?: SiteRanking[];
  bottom_sites?: SiteRanking[];
  alerts?: Alert[];
}

export interface RevenueMetrics {
  mrr: number;
  arr: number;
  avg_revenue_per_org: number;
  tier_breakdown: {
    [key: string]: {
      count: number;
      revenue: number;
    };
  };
}

export interface UserEngagement {
  active_today: number;
  active_this_week: number;
  new_users_this_week: number;
  total_users: number;
  engagement_rate: number;
}

export interface ModuleAdoption {
  module: string;
  display_name: string;
  organizations: number;
  adoption_rate: number;
}

export interface DefectTrend {
  date: string;
  full_date: string;
  created: number;
  resolved: number;
}

export interface SiteRanking {
  site_id: number;
  site_name: string;
  organization: string;
  completion_rate: number;
  rag_status: string;
  open_defects: number;
}

export interface Alert {
  type: 'warning' | 'error' | 'info';
  category: string;
  title: string;
  message: string;
  org_id?: number;
  site_id?: number;
  priority: 'high' | 'medium' | 'low';
}

export interface RecentActivityResponse {
  items: ActivityItem[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface OrgAdminMetrics {
  organization_name: string;
  total_sites: number;
  sites_by_rag: {
    red: number;
    amber: number;
    green: number;
  };
  total_checklists_today: number;
  completion_rate: number;
  total_open_defects: number;
  site_details: SiteDetail[];
}

export interface SiteUserMetrics {
  site_name: string;
  pending_checklists: ChecklistSummary[];
  overdue_checklists: number;
  open_defects: number;
  completion_rate_this_week: number;
}

export interface ActivityItem {
  id: number;
  type: string;
  description: string;
  timestamp: string;
}

export interface SiteDetail {
  site_id: number;
  site_name: string;
  rag_status: string;
  completion_rate: number;
  open_defects: number;
}

export interface ChecklistSummary {
  id: number;
  category_name: string;
  scheduled_date: string;
  status: string;
  total_tasks: number;
  completed_tasks: number;
}
