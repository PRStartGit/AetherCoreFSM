from pydantic import BaseModel
from typing import List, Dict, Any


class SuperAdminDashboard(BaseModel):
    """Super admin dashboard data."""
    total_organizations: int
    total_sites: int
    sites_by_rag: Dict[str, int] = {}
    total_checklists_today: int
    total_users: int
    total_active_checklists: int
    total_open_defects: int
    recent_activity: List[Dict[str, Any]] = []
    subscription_summary: Dict[str, Any] = {}
    rag_summary: Dict[str, int] = {}
    org_performance: List[Dict[str, Any]] = []
    growth_data: List[Dict[str, Any]] = []


class OrgAdminDashboard(BaseModel):
    """Organization admin dashboard data."""
    organization_name: str
    total_sites: int
    sites_by_rag: Dict[str, int] = {}
    total_checklists_today: int
    total_users: int
    overall_rag_status: str
    completion_rate: float
    total_open_defects: int
    overdue_checklists: int
    site_details: List[Dict[str, Any]] = []
    recent_activity: List[Dict[str, Any]] = []


class SiteUserDashboard(BaseModel):
    """Site user dashboard data."""
    assigned_sites: List[Dict[str, Any]] = []
    todays_checklists: List[Dict[str, Any]] = []
    assigned_checklists: List[Dict[str, Any]] = []
    open_defects: List[Dict[str, Any]] = []
    recent_completed: List[Dict[str, Any]] = []


class RAGStatus(BaseModel):
    """RAG status for a site."""
    site_id: int
    site_name: str
    rag_status: str  # 'red', 'amber', 'green'
    completion_rate: float
    open_defects: int
    overdue_defects: int
    last_30_days_completion: float
