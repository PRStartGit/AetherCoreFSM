export interface JobRole {
  id: number;
  name: string;
  is_system_role: boolean;
  created_at: string;
}

export interface UserModuleAccess {
  id: number;
  user_id: number;
  module_name: string;
  granted_at: string;
  granted_by_user_id: number | null;
}

export interface CourseCategory {
  id: number;
  name: string;
  description?: string;
  created_at: string;
  updated_at?: string;
}

export interface CourseModule {
  id: number;
  course_id: number;
  title: string;
  description?: string;
  video_url?: string;
  pdf_url?: string;
  text_content?: string;
  order_index: number;
  duration_minutes?: number;
  created_at: string;
  updated_at?: string;
}

export interface Course {
  id: number;
  title: string;
  description?: string;
  thumbnail_url?: string;
  category_id?: number;
  is_published: boolean;
  created_by_user_id: number;
  created_at: string;
  updated_at?: string;
  category?: CourseCategory;
  modules?: CourseModule[];
}

export interface CourseCreate {
  title: string;
  description?: string;
  thumbnail_url?: string;
  category_id?: number;
  is_published: boolean;
}

export interface CourseUpdate {
  title?: string;
  description?: string;
  thumbnail_url?: string;
  category_id?: number;
  is_published?: boolean;
}

export interface CourseModuleCreate {
  course_id: number;
  title: string;
  description?: string;
  video_url?: string;
  pdf_url?: string;
  text_content?: string;
  order_index: number;
  duration_minutes?: number;
}

export interface CourseModuleUpdate {
  title?: string;
  description?: string;
  video_url?: string;
  pdf_url?: string;
  text_content?: string;
  order_index?: number;
  duration_minutes?: number;
}

export enum EnrollmentStatus {
  NOT_STARTED = 'not_started',
  IN_PROGRESS = 'in_progress',
  COMPLETED = 'completed'
}

export interface CourseEnrollment {
  id: number;
  user_id: number;
  course_id: number;
  assigned_by_user_id?: number;
  enrolled_at: string;
  status: EnrollmentStatus;
  progress_percentage: number;
  started_at?: string;
  completed_at?: string;
  last_accessed_at?: string;
}

export interface CourseEnrollmentWithCourse extends CourseEnrollment {
  course_title: string;
  course_description?: string;
  course_thumbnail_url?: string;
  course_category_name?: string;
}

export interface AssignCoursesRequest {
  user_ids: number[];
  course_ids: number[];
}

export interface ModuleProgress {
  id: number;
  enrollment_id: number;
  module_id: number;
  is_completed: boolean;
  completed_at?: string;
  time_spent_seconds: number;
  last_position_seconds: number;
  created_at: string;
  updated_at?: string;
}
