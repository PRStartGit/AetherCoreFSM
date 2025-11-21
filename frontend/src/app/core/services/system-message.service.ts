import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface SystemMessage {
  id: number;
  message_content: string;
  created_by_user_id: number;
  created_by_name: string | null;
  organization_id: number | null;
  organization_name: string | null;
  visibility_scope: string;
  expiry_date: string;
  is_active: boolean;
  created_at: string;
  is_super_admin_message: boolean;
}

export interface SystemMessageCreate {
  message_content: string;
  expiry_date: string;
  visibility_scope: 'org_admins_only' | 'site_users_only' | 'both';
}

@Injectable({
  providedIn: 'root'
})
export class SystemMessageService {
  private apiUrl = '/api/v1/system-messages';
  private messagesSubject = new BehaviorSubject<SystemMessage[]>([]);
  public messages$ = this.messagesSubject.asObservable();

  constructor(private http: HttpClient) {}

  loadMessages(): void {
    this.getActiveMessages().subscribe(messages => {
      this.messagesSubject.next(messages);
    });
  }

  getMessages(includeDismissed: boolean = false): Observable<SystemMessage[]> {
    return this.http.get<SystemMessage[]>(`${this.apiUrl}?include_dismissed=${includeDismissed}`);
  }

  getActiveMessages(): Observable<SystemMessage[]> {
    return this.http.get<SystemMessage[]>(`${this.apiUrl}/active`);
  }

  createMessage(message: SystemMessageCreate): Observable<SystemMessage> {
    return this.http.post<SystemMessage>(this.apiUrl, message).pipe(
      tap(() => this.loadMessages())
    );
  }

  dismissMessage(messageId: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/${messageId}/dismiss`, {}).pipe(
      tap(() => {
        const current = this.messagesSubject.value;
        this.messagesSubject.next(current.filter(m => m.id !== messageId));
      })
    );
  }

  deleteMessage(messageId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${messageId}`).pipe(
      tap(() => {
        const current = this.messagesSubject.value;
        this.messagesSubject.next(current.filter(m => m.id !== messageId));
      })
    );
  }
}
