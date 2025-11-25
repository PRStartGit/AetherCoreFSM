import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export enum TicketStatus {
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  RESOLVED = 'resolved',
  CLOSED = 'closed'
}

export enum TicketPriority {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  URGENT = 'urgent'
}

export enum TicketType {
  TECHNICAL = 'technical',
  BILLING = 'billing',
  GENERAL = 'general',
  FEATURE_REQUEST = 'feature_request'
}

export interface TicketMessage {
  id: number;
  ticket_id: number;
  user_id: number;
  user_name: string;
  user_role: string;
  message: string;
  is_internal_note: boolean;
  created_at: string;
}

export interface Ticket {
  id: number;
  ticket_number: string;
  subject: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  ticket_type: TicketType;
  created_by_user_id: number;
  created_by_user_name: string;
  organization_id: number | null;
  organization_name: string | null;
  assigned_to_user_id: number | null;
  assigned_to_user_name: string | null;
  created_at: string;
  updated_at: string | null;
  resolved_at: string | null;
  closed_at: string | null;
  message_count: number;
  messages?: TicketMessage[];
}

export interface TicketStats {
  total: number;
  open: number;
  in_progress: number;
  resolved: number;
  closed: number;
}

export interface CreateTicketRequest {
  subject: string;
  description: string;
  ticket_type: TicketType;
  priority: TicketPriority;
}

export interface UpdateTicketRequest {
  status?: TicketStatus;
  priority?: TicketPriority;
  assigned_to_user_id?: number;
}

export interface CreateMessageRequest {
  message: string;
  is_internal_note?: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class TicketService {
  private apiUrl = '/api/v1/tickets';

  constructor(private http: HttpClient) {}

  createTicket(ticket: CreateTicketRequest): Observable<Ticket> {
    return this.http.post<Ticket>(this.apiUrl, ticket);
  }

  getTickets(filters?: {
    status?: TicketStatus;
    ticket_type?: TicketType;
    priority?: TicketPriority;
  }): Observable<Ticket[]> {
    let params = new HttpParams();
    if (filters?.status) {
      params = params.set('status', filters.status);
    }
    if (filters?.ticket_type) {
      params = params.set('ticket_type', filters.ticket_type);
    }
    if (filters?.priority) {
      params = params.set('priority', filters.priority);
    }
    return this.http.get<Ticket[]>(this.apiUrl, { params });
  }

  getTicket(id: number): Observable<Ticket> {
    return this.http.get<Ticket>(`${this.apiUrl}/${id}`);
  }

  getStats(): Observable<TicketStats> {
    return this.http.get<TicketStats>(`${this.apiUrl}/stats`);
  }

  updateTicket(id: number, update: UpdateTicketRequest): Observable<Ticket> {
    return this.http.patch<Ticket>(`${this.apiUrl}/${id}`, update);
  }

  addMessage(ticketId: number, message: CreateMessageRequest): Observable<TicketMessage> {
    return this.http.post<TicketMessage>(`${this.apiUrl}/${ticketId}/messages`, message);
  }

  closeTicket(id: number): Observable<Ticket> {
    return this.http.post<Ticket>(`${this.apiUrl}/${id}/close`, {});
  }

  reopenTicket(id: number): Observable<Ticket> {
    return this.http.post<Ticket>(`${this.apiUrl}/${id}/reopen`, {});
  }

  // Helper methods for display
  getStatusLabel(status: TicketStatus): string {
    const labels: Record<TicketStatus, string> = {
      [TicketStatus.OPEN]: 'Open',
      [TicketStatus.IN_PROGRESS]: 'In Progress',
      [TicketStatus.RESOLVED]: 'Resolved',
      [TicketStatus.CLOSED]: 'Closed'
    };
    return labels[status] || status;
  }

  getStatusColor(status: TicketStatus): string {
    const colors: Record<TicketStatus, string> = {
      [TicketStatus.OPEN]: 'bg-blue-100 text-blue-800',
      [TicketStatus.IN_PROGRESS]: 'bg-yellow-100 text-yellow-800',
      [TicketStatus.RESOLVED]: 'bg-green-100 text-green-800',
      [TicketStatus.CLOSED]: 'bg-gray-100 text-gray-800'
    };
    return colors[status] || 'bg-gray-100 text-gray-800';
  }

  getPriorityLabel(priority: TicketPriority): string {
    const labels: Record<TicketPriority, string> = {
      [TicketPriority.LOW]: 'Low',
      [TicketPriority.MEDIUM]: 'Medium',
      [TicketPriority.HIGH]: 'High',
      [TicketPriority.URGENT]: 'Urgent'
    };
    return labels[priority] || priority;
  }

  getPriorityColor(priority: TicketPriority): string {
    const colors: Record<TicketPriority, string> = {
      [TicketPriority.LOW]: 'bg-gray-100 text-gray-800',
      [TicketPriority.MEDIUM]: 'bg-blue-100 text-blue-800',
      [TicketPriority.HIGH]: 'bg-orange-100 text-orange-800',
      [TicketPriority.URGENT]: 'bg-red-100 text-red-800'
    };
    return colors[priority] || 'bg-gray-100 text-gray-800';
  }

  getTypeLabel(type: TicketType): string {
    const labels: Record<TicketType, string> = {
      [TicketType.TECHNICAL]: 'Technical',
      [TicketType.BILLING]: 'Billing',
      [TicketType.GENERAL]: 'General',
      [TicketType.FEATURE_REQUEST]: 'Feature Request'
    };
    return labels[type] || type;
  }
}
