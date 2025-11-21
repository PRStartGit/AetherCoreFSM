import { Component, EventEmitter, Input, Output, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SystemMessageService, SystemMessageCreate } from '../../../core/services/system-message.service';
import { UserRole } from '../../../core/models';

@Component({
  selector: 'app-broadcast-modal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="modal-backdrop" (click)="close.emit()">
      <div class="modal-content" (click)="$event.stopPropagation()">
        <div class="modal-header">
          <h2><i class="fa-solid fa-bullhorn"></i> Send Broadcast Message</h2>
          <button class="close-btn" (click)="close.emit()">
            <i class="fa-solid fa-xmark"></i>
          </button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label for="message">Message <span class="required">*</span></label>
            <textarea
              id="message"
              [(ngModel)]="messageContent"
              rows="4"
              placeholder="Enter your broadcast message..."
              class="form-textarea"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="expiry">Expiry Date <span class="required">*</span></label>
            <input
              type="datetime-local"
              id="expiry"
              [(ngModel)]="expiryDate"
              class="form-input"
              [min]="minDate"
            >
          </div>

          <div class="form-group" *ngIf="userRole === 'super_admin'">
            <label>Visibility</label>
            <div class="radio-group">
              <label class="radio-option">
                <input type="radio" name="visibility" value="both" [(ngModel)]="visibilityScope">
                <span>All Users (Org Admins & Site Users)</span>
              </label>
              <label class="radio-option">
                <input type="radio" name="visibility" value="org_admins_only" [(ngModel)]="visibilityScope">
                <span>Org Admins Only</span>
              </label>
              <label class="radio-option">
                <input type="radio" name="visibility" value="site_users_only" [(ngModel)]="visibilityScope">
                <span>Site Users Only</span>
              </label>
            </div>
          </div>

          <div class="info-box" *ngIf="userRole !== 'super_admin'">
            <i class="fa-solid fa-info-circle"></i>
            <span>This message will be sent to all users in your organization.</span>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-secondary" (click)="close.emit()">Cancel</button>
          <button
            class="btn-primary"
            (click)="sendMessage()"
            [disabled]="!isValid() || sending"
          >
            <i class="fa-solid fa-paper-plane" *ngIf="!sending"></i>
            <i class="fa-solid fa-spinner fa-spin" *ngIf="sending"></i>
            {{ sending ? 'Sending...' : 'Send Message' }}
          </button>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 1rem;
    }

    .modal-content {
      background: white;
      border-radius: 12px;
      width: 100%;
      max-width: 500px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    }

    .modal-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #e5e7eb;
    }

    .modal-header h2 {
      font-size: 1.25rem;
      font-weight: 600;
      color: #1f2937;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    .modal-header h2 i {
      color: #0891b2;
    }

    .close-btn {
      background: none;
      border: none;
      color: #6b7280;
      cursor: pointer;
      padding: 0.5rem;
      border-radius: 6px;
      transition: all 0.2s;
    }

    .close-btn:hover {
      background: #f3f4f6;
      color: #1f2937;
    }

    .modal-body {
      padding: 1.5rem;
    }

    .form-group {
      margin-bottom: 1.25rem;
    }

    .form-group label {
      display: block;
      font-size: 0.875rem;
      font-weight: 600;
      color: #374151;
      margin-bottom: 0.5rem;
    }

    .required {
      color: #ef4444;
    }

    .form-textarea,
    .form-input {
      width: 100%;
      padding: 0.75rem;
      border: 1px solid #d1d5db;
      border-radius: 8px;
      font-size: 0.95rem;
      transition: border-color 0.2s, box-shadow 0.2s;
    }

    .form-textarea:focus,
    .form-input:focus {
      outline: none;
      border-color: #0891b2;
      box-shadow: 0 0 0 3px rgba(8, 145, 178, 0.1);
    }

    .form-textarea {
      resize: vertical;
      min-height: 100px;
    }

    .radio-group {
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .radio-option {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      cursor: pointer;
      font-size: 0.9rem;
      color: #4b5563;
    }

    .radio-option input {
      width: 18px;
      height: 18px;
      accent-color: #0891b2;
    }

    .info-box {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      padding: 0.875rem;
      background: #f0f9ff;
      border-radius: 8px;
      color: #0369a1;
      font-size: 0.875rem;
    }

    .modal-footer {
      display: flex;
      justify-content: flex-end;
      gap: 0.75rem;
      padding: 1rem 1.5rem;
      border-top: 1px solid #e5e7eb;
    }

    .btn-secondary,
    .btn-primary {
      padding: 0.625rem 1.25rem;
      border-radius: 8px;
      font-weight: 600;
      font-size: 0.9rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: all 0.2s;
    }

    .btn-secondary {
      background: #f3f4f6;
      border: 1px solid #d1d5db;
      color: #374151;
    }

    .btn-secondary:hover {
      background: #e5e7eb;
    }

    .btn-primary {
      background: linear-gradient(135deg, #0891b2, #06b6d4);
      border: none;
      color: white;
    }

    .btn-primary:hover:not(:disabled) {
      background: linear-gradient(135deg, #0e7490, #0891b2);
    }

    .btn-primary:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  `]
})
export class BroadcastModalComponent implements OnInit {
  @Input() userRole: string = '';
  @Output() close = new EventEmitter<void>();
  @Output() messageSent = new EventEmitter<void>();

  messageContent: string = '';
  expiryDate: string = '';
  visibilityScope: 'both' | 'org_admins_only' | 'site_users_only' = 'both';
  sending: boolean = false;
  minDate: string = '';

  constructor(private systemMessageService: SystemMessageService) {}

  ngOnInit(): void {
    // Set minimum date to now
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    this.minDate = now.toISOString().slice(0, 16);

    // Set default expiry to 7 days from now
    const defaultExpiry = new Date();
    defaultExpiry.setDate(defaultExpiry.getDate() + 7);
    defaultExpiry.setMinutes(defaultExpiry.getMinutes() - defaultExpiry.getTimezoneOffset());
    this.expiryDate = defaultExpiry.toISOString().slice(0, 16);
  }

  isValid(): boolean {
    return this.messageContent.trim().length > 0 && this.expiryDate.length > 0;
  }

  sendMessage(): void {
    if (!this.isValid()) return;

    this.sending = true;

    const message: SystemMessageCreate = {
      message_content: this.messageContent.trim(),
      expiry_date: new Date(this.expiryDate).toISOString(),
      visibility_scope: this.visibilityScope
    };

    this.systemMessageService.createMessage(message).subscribe({
      next: () => {
        this.sending = false;
        this.messageSent.emit();
        this.close.emit();
      },
      error: (err) => {
        this.sending = false;
        console.error('Error sending message:', err);
      }
    });
  }
}
