import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription } from 'rxjs';
import { SystemMessageService, SystemMessage } from '../../../core/services/system-message.service';

@Component({
  selector: 'app-system-message-banner',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="system-messages-container" *ngIf="messages.length > 0">
      <div *ngFor="let message of messages"
           class="system-message-banner"
           [class.super-admin]="message.is_super_admin_message"
           [class.org-admin]="!message.is_super_admin_message">
        <div class="message-content">
          <i class="fa-solid" [class.fa-bullhorn]="message.is_super_admin_message"
             [class.fa-building]="!message.is_super_admin_message"></i>
          <span class="message-text">{{ message.message_content }}</span>
          <span class="message-meta">
            — {{ message.created_by_name || 'System' }}
            <span *ngIf="!message.is_super_admin_message && message.organization_name">
              ({{ message.organization_name }})
            </span>
          </span>
        </div>
        <button class="dismiss-btn" (click)="dismissMessage(message.id)" title="Dismiss">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>
    </div>
  `,
  styles: [`
    .system-messages-container {
      position: fixed;
      top: 64px;
      left: 0;
      right: 0;
      z-index: 100;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    @media (min-width: 768px) {
      .system-messages-container {
        left: 240px;
      }
    }

    .system-message-banner {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 6px 12px;
      font-size: 13px;
      animation: slideDown 0.3s ease-out;
    }

    @keyframes slideDown {
      from {
        transform: translateY(-100%);
        opacity: 0;
      }
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }

    .system-message-banner.super-admin {
      background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
      color: white;
    }

    .system-message-banner.org-admin {
      background: linear-gradient(135deg, #047857 0%, #10b981 100%);
      color: white;
    }

    .message-content {
      display: flex;
      align-items: center;
      gap: 8px;
      flex: 1;
      min-width: 0;
    }

    .message-content i {
      font-size: 13px;
      flex-shrink: 0;
    }

    .message-text {
      font-weight: 500;
    }

    .message-meta {
      font-size: 12px;
      opacity: 0.85;
      flex-shrink: 0;
    }

    .dismiss-btn {
      background: rgba(255, 255, 255, 0.2);
      border: none;
      color: white;
      width: 22px;
      height: 22px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
      flex-shrink: 0;
      font-size: 11px;
    }

    .dismiss-btn:hover {
      background: rgba(255, 255, 255, 0.3);
    }

    @media (max-width: 640px) {
      .message-meta {
        display: none;
      }
    }
  `]
})
export class SystemMessageBannerComponent implements OnInit, OnDestroy {
  messages: SystemMessage[] = [];
  private subscription?: Subscription;

  constructor(private systemMessageService: SystemMessageService) {}

  ngOnInit(): void {
    this.systemMessageService.loadMessages();
    this.subscription = this.systemMessageService.messages$.subscribe(messages => {
      this.messages = messages;
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  dismissMessage(id: number): void {
    this.systemMessageService.dismissMessage(id).subscribe();
  }
}
