import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TicketService, Ticket, TicketStatus, TicketType, TicketPriority, TicketStats } from '../../../core/services/ticket.service';
import { AuthService } from '../../../core/auth/auth.service';
import { UserRole } from '../../../core/models';
import { formatDate } from '../../../shared/utils/date-utils';

@Component({
  selector: 'app-ticket-list',
  templateUrl: './ticket-list.component.html',
  styleUrls: ['./ticket-list.component.css']
})
export class TicketListComponent implements OnInit {
  tickets: Ticket[] = [];
  filteredTickets: Ticket[] = [];
  stats: TicketStats = { total: 0, open: 0, in_progress: 0, resolved: 0, closed: 0 };
  loading = true;
  showNewTicketForm = false;

  // Filters
  statusFilter: TicketStatus | '' = '';
  typeFilter: TicketType | '' = '';
  priorityFilter: TicketPriority | '' = '';

  // New ticket form
  newTicket = {
    subject: '',
    description: '',
    ticket_type: TicketType.GENERAL,
    priority: TicketPriority.MEDIUM
  };
  submitting = false;

  // Enums for template
  TicketStatus = TicketStatus;
  TicketType = TicketType;
  TicketPriority = TicketPriority;

  constructor(
    public ticketService: TicketService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadTickets();
    this.loadStats();
  }

  loadTickets(): void {
    this.loading = true;
    this.ticketService.getTickets().subscribe({
      next: (tickets) => {
        this.tickets = tickets;
        this.applyFilters();
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading tickets:', err);
        this.loading = false;
      }
    });
  }

  loadStats(): void {
    this.ticketService.getStats().subscribe({
      next: (stats) => {
        this.stats = stats;
      }
    });
  }

  applyFilters(): void {
    this.filteredTickets = this.tickets.filter(ticket => {
      if (this.statusFilter && ticket.status !== this.statusFilter) return false;
      if (this.typeFilter && ticket.ticket_type !== this.typeFilter) return false;
      if (this.priorityFilter && ticket.priority !== this.priorityFilter) return false;
      return true;
    });
  }

  onFilterChange(): void {
    this.applyFilters();
  }

  clearFilters(): void {
    this.statusFilter = '';
    this.typeFilter = '';
    this.priorityFilter = '';
    this.applyFilters();
  }

  openNewTicketForm(): void {
    this.showNewTicketForm = true;
    this.newTicket = {
      subject: '',
      description: '',
      ticket_type: TicketType.GENERAL,
      priority: TicketPriority.MEDIUM
    };
  }

  closeNewTicketForm(): void {
    this.showNewTicketForm = false;
  }

  submitNewTicket(): void {
    if (!this.newTicket.subject || !this.newTicket.description) return;

    this.submitting = true;
    this.ticketService.createTicket(this.newTicket).subscribe({
      next: (ticket) => {
        this.submitting = false;
        this.showNewTicketForm = false;
        this.loadTickets();
        this.loadStats();
        // Navigate to the new ticket
        this.router.navigate(['/support/tickets', ticket.id]);
      },
      error: (err) => {
        console.error('Error creating ticket:', err);
        this.submitting = false;
      }
    });
  }

  viewTicket(ticket: Ticket): void {
    this.router.navigate(['/support/tickets', ticket.id]);
  }

  isSuperAdmin(): boolean {
    return this.authService.getUser()?.role === UserRole.SUPER_ADMIN;
  }

  getRelativeTime(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return formatDate(date);
  }
}
