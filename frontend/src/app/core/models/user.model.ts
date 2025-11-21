export enum UserRole {
  SUPER_ADMIN = 'super_admin',
  ORG_ADMIN = 'org_admin',
  SITE_USER = 'site_user'
}

export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  role: UserRole;
  organization_id: number | null;
  is_active: boolean;
  must_change_password?: boolean;
  created_at: string;
  updated_at: string;
  site_ids?: number[];
}

export interface LoginRequest {
  organization_id: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  must_change_password?: boolean;
  user?: User;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
}
