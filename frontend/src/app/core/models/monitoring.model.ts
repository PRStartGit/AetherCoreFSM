// Category Models
export enum ChecklistFrequency {
  DAILY = 'daily',
  WEEKLY = 'weekly',
  MONTHLY = 'monthly',
  SIX_MONTHLY = 'six_monthly',
  YEARLY = 'yearly'
}

export interface Category {
  id: number;
  name: string;
  description: string;
  frequency: string;
  closes_at: string | null;
  is_global: boolean;
  organization_id: number | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface CategoryCreate {
  name: string;
  description: string;
  frequency: string;
  closes_at?: string | null;
  is_global?: boolean;
  organization_id?: number;
}

// Task Models
export interface Task {
  id: number;
  category_id: number;
  name: string;
  description: string;
  order_index: number;
  form_config: any;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  assigned_sites?: number[];
  site_ids?: number[];  // For compatibility with form
}

export interface TaskCreate {
  category_id: number;
  name: string;
  description: string;
  order_index?: number;
  form_config?: any;
}

export interface TaskAssignment {
  task_id: number;
  site_ids: number[];
}

// Checklist Models
export enum ChecklistStatus {
  PENDING = 'pending',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed',
  OVERDUE = 'overdue'
}

export interface ChecklistItem {
  id: number;
  checklist_id: number;
  task_id: number;
  item_name: string;  // Backend uses item_name, not task_name
  form_data: any;
  is_completed: boolean;
  completed_at: string | null;
  completed_by: number | null;
}

export interface Checklist {
  id: number;
  site_id: number;
  category_id: number;
  checklist_date: string;  // Backend uses checklist_date, not scheduled_date
  status: ChecklistStatus;
  completed_at: string | null;
  created_at: string;
  updated_at: string;
  items?: ChecklistItem[];
  category?: Category;
  total_items?: number;
  completed_items?: number;
  completion_percentage?: number;
  completed_by_id?: number | null;
}

export interface ChecklistCreate {
  site_id: number;
  category_id: number;
  scheduled_date: string;
}

export interface ChecklistItemUpdate {
  form_data?: any;
  is_completed?: boolean;
}

// Defect Models
export enum DefectSeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

export enum DefectStatus {
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved',
  CLOSED = 'closed'
}

export interface Defect {
  id: number;
  site_id: number;
  checklist_item_id: number | null;
  title: string;
  description: string;
  severity: DefectSeverity;
  status: DefectStatus;
  photo_url: string | null;
  reported_by: number;
  assigned_to: number | null;
  due_date: string | null;
  resolved_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface DefectCreate {
  site_id: number;
  checklist_item_id?: number;
  title: string;
  description: string;
  severity: DefectSeverity;
  photo_url?: string;
  assigned_to?: number;
  due_date?: string;
}

export interface DefectUpdate {
  title?: string;
  description?: string;
  severity?: DefectSeverity;
  status?: DefectStatus;
  assigned_to?: number;
  due_date?: string;
}

// RAG Status
export enum RAGStatus {
  RED = 'red',
  AMBER = 'amber',
  GREEN = 'green'
}

export interface SiteRAGStatus {
  site_id: number;
  site_name: string;
  rag_status: RAGStatus;
  completion_rate: number;
  overdue_checklists: number;
  open_defects: number;
  critical_defects: number;
}
