import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TicketService, Ticket, TicketMessage, TicketStatus, TicketPriority } from '../../../core/services/ticket.service';
import { AuthService } from '../../../core/auth/auth.service';
import { UserRole } from '../../../core/models';
import { formatDateTime } from '../../../shared/utils/date-utils';

@Component({
  selector: 'app-ticket-detail',
  templateUrl: './ticket-detail.component.html',
  styleUrls: ['./ticket-detail.component.css']
})
export class TicketDetailComponent implements OnInit {
  ticket: Ticket | null = null;
  loading = true;
  newMessage = '';
  isInternalNote = false;
  sendingMessage = false;
  updatingStatus = false;

  TicketStatus = TicketStatus;
  TicketPriority = TicketPriority;

  constructor(
    public ticketService: TicketService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    const ticketId = this.route.snapshot.paramMap.get('id');
    if (ticketId) {
      this.loadTicket(parseInt(ticketId));
    }
  }

  loadTicket(id: number): void {
    this.loading = true;
    this.ticketService.getTicket(id).subscribe({
      next: (ticket) => {
        this.ticket = ticket;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading ticket:', err);
        this.loading = false;
        this.router.navigate(['/support/tickets']);
      }
    });
  }

  sendMessage(): void {
    if (!this.newMessage.trim() || !this.ticket) return;

    this.sendingMessage = true;
    this.ticketService.addMessage(this.ticket.id, {
      message: this.newMessage,
      is_internal_note: this.isInternalNote
    }).subscribe({
      next: (message) => {
        this.ticket!.messages = [...(this.ticket!.messages || []), message];
        this.ticket!.message_count++;
        this.newMessage = '';
        this.isInternalNote = false;
        this.sendingMessage = false;
      },
      error: (err) => {
        console.error('Error sending message:', err);
        this.sendingMessage = false;
      }
    });
  }

  updateStatus(status: TicketStatus): void {
    if (!this.ticket) return;

    this.updatingStatus = true;
    this.ticketService.updateTicket(this.ticket.id, { status }).subscribe({
      next: (ticket) => {
        this.ticket = { ...this.ticket!, ...ticket };
        this.updatingStatus = false;
      },
      error: (err) => {
        console.error('Error updating status:', err);
        this.updatingStatus = false;
      }
    });
  }

  updatePriority(priority: TicketPriority): void {
    if (!this.ticket) return;

    this.ticketService.updateTicket(this.ticket.id, { priority }).subscribe({
      next: (ticket) => {
        this.ticket = { ...this.ticket!, ...ticket };
      }
    });
  }

  closeTicket(): void {
    if (!this.ticket) return;

    this.ticketService.closeTicket(this.ticket.id).subscribe({
      next: (ticket) => {
        this.ticket = { ...this.ticket!, ...ticket };
      }
    });
  }

  reopenTicket(): void {
    if (!this.ticket) return;

    this.ticketService.reopenTicket(this.ticket.id).subscribe({
      next: (ticket) => {
        this.ticket = { ...this.ticket!, ...ticket };
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/support/tickets']);
  }

  isSuperAdmin(): boolean {
    return this.authService.getUser()?.role === UserRole.SUPER_ADMIN;
  }

  isTicketOwner(): boolean {
    const user = this.authService.getUser();
    return user?.id === this.ticket?.created_by_user_id;
  }

  canCloseTicket(): boolean {
    return this.isTicketOwner() || this.isSuperAdmin();
  }

  formatDate(dateStr: string): string {
    return formatDateTime(dateStr);
  }

  getMessageClass(message: TicketMessage): string {
    const user = this.authService.getUser();
    if (message.is_internal_note) {
      return 'bg-yellow-50 border-yellow-200';
    }
    if (message.user_id === user?.id) {
      return 'bg-cyan-50 border-cyan-200';
    }
    return 'bg-gray-50 border-gray-200';
  }
}
