export interface SuperAdminMetrics {
  total_organizations: number;
  total_sites: number;
  total_users: number;
  active_subscriptions: number;
  total_checklists_today: number;
  total_open_defects: number;
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
