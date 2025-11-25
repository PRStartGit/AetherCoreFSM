import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject, interval } from 'rxjs';
import { tap } from 'rxjs/operators';

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  notification_type: string;
  related_id: number | null;
  related_url: string | null;
  is_read: boolean;
  read_at: string | null;
  created_at: string;
}

export interface UnreadCountResponse {
  count: number;
}

export interface MarkReadRequest {
  notification_ids: number[];
}

@Injectable({
  providedIn: 'root'
})
export class NotificationService {
  private apiUrl = '/api/v1/notifications';
  private unreadCountSubject = new BehaviorSubject<number>(0);
  public unreadCount$ = this.unreadCountSubject.asObservable();

  constructor(private http: HttpClient) {
    // Poll for unread count every 30 seconds
    interval(30000).subscribe(() => this.refreshUnreadCount());
  }

  /**
   * Get all notifications for the current user
   */
  getNotifications(unreadOnly: boolean = false, limit: number = 50): Observable<Notification[]> {
    const params: any = { limit };
    if (unreadOnly) {
      params.unread_only = 'true';
    }
    return this.http.get<Notification[]>(this.apiUrl, { params });
  }

  /**
   * Get count of unread notifications
   */
  getUnreadCount(): Observable<UnreadCountResponse> {
    return this.http.get<UnreadCountResponse>(`${this.apiUrl}/unread-count`).pipe(
      tap(response => this.unreadCountSubject.next(response.count))
    );
  }

  /**
   * Refresh the unread count (call this periodically)
   */
  refreshUnreadCount(): void {
    this.getUnreadCount().subscribe();
  }

  /**
   * Mark specific notifications as read
   */
  markAsRead(notificationIds: number[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/mark-read`, { notification_ids: notificationIds }).pipe(
      tap(() => this.refreshUnreadCount())
    );
  }

  /**
   * Mark all notifications as read
   */
  markAllAsRead(): Observable<any> {
    return this.http.post(`${this.apiUrl}/mark-all-read`, {}).pipe(
      tap(() => this.refreshUnreadCount())
    );
  }

  /**
   * Delete a notification
   */
  deleteNotification(notificationId: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${notificationId}`).pipe(
      tap(() => this.refreshUnreadCount())
    );
  }

  /**
   * Get the current unread count value
   */
  getCurrentUnreadCount(): number {
    return this.unreadCountSubject.value;
  }
}
