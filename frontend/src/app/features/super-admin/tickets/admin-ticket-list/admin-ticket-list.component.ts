import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TicketService, Ticket, TicketStatus, TicketType, TicketPriority, TicketStats } from '../../../../core/services/ticket.service';
import { formatDate } from '../../../../shared/utils/date-utils';

@Component({
  selector: 'app-admin-ticket-list',
  templateUrl: './admin-ticket-list.component.html',
  styleUrls: ['./admin-ticket-list.component.css']
})
export class AdminTicketListComponent implements OnInit {
  tickets: Ticket[] = [];
  filteredTickets: Ticket[] = [];
  stats: TicketStats = { total: 0, open: 0, in_progress: 0, resolved: 0, closed: 0 };
  loading = true;

  // Filters
  statusFilter: TicketStatus | '' = '';
  typeFilter: TicketType | '' = '';
  priorityFilter: TicketPriority | '' = '';
  searchQuery = '';

  // Tab selection
  activeTab: 'active' | 'closed' = 'active';

  TicketStatus = TicketStatus;
  TicketType = TicketType;
  TicketPriority = TicketPriority;

  constructor(
    public ticketService: TicketService,
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
      // Tab filter
      if (this.activeTab === 'active' && ticket.status === TicketStatus.CLOSED) return false;
      if (this.activeTab === 'closed' && ticket.status !== TicketStatus.CLOSED) return false;

      // Status filter
      if (this.statusFilter && ticket.status !== this.statusFilter) return false;
      if (this.typeFilter && ticket.ticket_type !== this.typeFilter) return false;
      if (this.priorityFilter && ticket.priority !== this.priorityFilter) return false;

      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        if (!ticket.ticket_number.toLowerCase().includes(query) &&
            !ticket.subject.toLowerCase().includes(query) &&
            !ticket.created_by_user_name.toLowerCase().includes(query) &&
            !(ticket.organization_name?.toLowerCase().includes(query))) {
          return false;
        }
      }

      return true;
    });
  }

  onFilterChange(): void {
    this.applyFilters();
  }

  setActiveTab(tab: 'active' | 'closed'): void {
    this.activeTab = tab;
    this.statusFilter = '';
    this.applyFilters();
  }

  clearFilters(): void {
    this.statusFilter = '';
    this.typeFilter = '';
    this.priorityFilter = '';
    this.searchQuery = '';
    this.applyFilters();
  }

  viewTicket(ticket: Ticket): void {
    this.router.navigate(['/super-admin/tickets', ticket.id]);
  }

  quickUpdateStatus(ticket: Ticket, status: TicketStatus, event: Event): void {
    event.stopPropagation();
    this.ticketService.updateTicket(ticket.id, { status }).subscribe({
      next: (updated) => {
        const idx = this.tickets.findIndex(t => t.id === ticket.id);
        if (idx >= 0) {
          this.tickets[idx] = { ...this.tickets[idx], ...updated };
          this.applyFilters();
          this.loadStats();
        }
      }
    });
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

  getActiveCount(): number {
    return this.tickets.filter(t => t.status !== TicketStatus.CLOSED).length;
  }

  getClosedCount(): number {
    return this.tickets.filter(t => t.status === TicketStatus.CLOSED).length;
  }
}
