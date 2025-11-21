import { Component, OnInit } from '@angular/core';
import { CommonModule, DatePipe } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivityLogService, ActivityLog, LogsResponse } from '../../../core/services/activity-log.service';

type TabType = 'tasks' | 'logins' | 'registrations' | 'errors';

@Component({
  selector: 'app-logs',
  standalone: true,
  imports: [CommonModule, DatePipe, FormsModule],
  templateUrl: './logs.component.html',
  styleUrls: ['./logs.component.scss']
})
export class LogsComponent implements OnInit {
  activeTab: TabType = 'tasks';
  logs: ActivityLog[] = [];
  total = 0;
  loading = false;
  error: string | null = null;
  days = 30;

  tabs: { id: TabType; label: string; icon: string }[] = [
    { id: 'tasks', label: 'Task Completions', icon: 'fa-solid fa-clipboard-check' },
    { id: 'logins', label: 'User Logins', icon: 'fa-solid fa-right-to-bracket' },
    { id: 'registrations', label: 'Registrations', icon: 'fa-solid fa-user-plus' },
    { id: 'errors', label: 'Errors', icon: 'fa-solid fa-triangle-exclamation' }
  ];

  constructor(private activityLogService: ActivityLogService) {}

  ngOnInit(): void {
    this.loadLogs();
  }

  setTab(tab: TabType): void {
    this.activeTab = tab;
    this.loadLogs();
  }

  loadLogs(): void {
    this.loading = true;
    this.error = null;

    let request$;
    switch (this.activeTab) {
      case 'tasks':
        request$ = this.activityLogService.getTaskCompletions(this.days);
        break;
      case 'logins':
        request$ = this.activityLogService.getLogins(this.days);
        break;
      case 'registrations':
        request$ = this.activityLogService.getRegistrations(this.days);
        break;
      case 'errors':
        request$ = this.activityLogService.getErrors(this.days);
        break;
    }

    request$.subscribe({
      next: (response: LogsResponse) => {
        this.logs = response.logs;
        this.total = response.total;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load logs';
        this.loading = false;
        console.error('Error loading logs:', err);
      }
    });
  }

  getLogTypeIcon(logType: string): string {
    switch (logType) {
      case 'login': return 'fa-solid fa-right-to-bracket text-green-500';
      case 'logout': return 'fa-solid fa-right-from-bracket text-gray-500';
      case 'registration': return 'fa-solid fa-user-plus text-blue-500';
      case 'org_registration': return 'fa-solid fa-building text-purple-500';
      case 'task_completed':
      case 'checklist_completed': return 'fa-solid fa-check-circle text-green-500';
      case 'error': return 'fa-solid fa-exclamation-circle text-red-500';
      case 'defect_created': return 'fa-solid fa-bug text-orange-500';
      case 'defect_resolved': return 'fa-solid fa-bug-slash text-green-500';
      default: return 'fa-solid fa-circle-info text-gray-500';
    }
  }

  setDays(days: number): void {
    this.days = days;
    this.loadLogs();
  }
}
