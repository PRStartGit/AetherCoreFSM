import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { TaskService } from '../../../core/services/task.service';
import { CategoryService } from '../../../core/services/category.service';
import { DefectService } from '../../../core/services/defect.service';
import { User } from '../../../core/models/user.model';
import { Task, Category, Defect, DefectStatus } from '../../../core/models/monitoring.model';

interface TaskCard {
  id: number;
  taskName: string;
  categoryName: string;
  closesAt: string;
  timeInfo: string;
  status: 'open' | 'missed' | 'opening-later';
}

@Component({
  selector: 'app-site-user-dashboard',
  templateUrl: './site-user-dashboard.component.html',
  styleUrls: ['./site-user-dashboard.component.css']
})
export class SiteUserDashboardComponent implements OnInit {
  currentUser: User | null = null;
  loading = false;
  error: string | null = null;

  // Task arrays
  openTasks: TaskCard[] = [];
  missedTasks: TaskCard[] = [];
  openingLaterTasks: TaskCard[] = [];

  // Defects
  myOpenDefects: Defect[] = [];

  // UI state
  showOpeningLater = false;

  // Categories map
  categoriesMap: Map<number, Category> = new Map();

  constructor(
    private authService: AuthService,
    private taskService: TaskService,
    private categoryService: CategoryService,
    private defectService: DefectService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.authState$.subscribe(state => {
      this.currentUser = state.user;
      if (this.currentUser) {
        this.loadCategories();
      }
    });
  }

  loadCategories(): void {
    this.categoryService.getAll().subscribe({
      next: (categories) => {
        // Build a map of category_id -> category for quick lookup
        categories.forEach(cat => {
          this.categoriesMap.set(cat.id, cat);
        });
        this.loadTasks();
        this.loadMyDefects();
      },
      error: (err) => {
        console.error('Error loading categories:', err);
        this.error = 'Failed to load categories';
      }
    });
  }

  loadTasks(): void {
    this.loading = true;
    this.error = null;

    const siteId = this.currentUser?.site_ids?.[0];

    if (!siteId) {
      this.error = 'No site assigned to user';
      this.loading = false;
      return;
    }

    // Load all tasks assigned to this site
    this.taskService.getAll().subscribe({
      next: (tasks) => {
        console.log('Loaded tasks:', tasks);
        this.processTasks(tasks, siteId);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading tasks:', err);
        this.error = 'Failed to load tasks';
        this.loading = false;
      }
    });
  }

  processTasks(tasks: Task[], siteId: number): void {
    this.openTasks = [];
    this.missedTasks = [];
    this.openingLaterTasks = [];

    const now = new Date();
    const currentTime = now.getHours() * 60 + now.getMinutes();

    console.log('Current time (minutes):', currentTime);

    // Filter tasks assigned to this site
    const siteTasks = tasks.filter(t => {
      const isAssigned = t.site_ids?.includes(siteId) || t.assigned_sites?.includes(siteId);
      console.log(`Task ${t.id} (${t.name}) assigned to site ${siteId}:`, isAssigned);
      return isAssigned;
    });

    console.log(`Found ${siteTasks.length} tasks for site ${siteId}`);

    siteTasks.forEach(task => {
      // Get category from map
      const category = this.categoriesMap.get(task.category_id);

      if (!category || !category.closes_at) {
        console.log(`Task ${task.id} has no category or closes_at time, skipping`);
        return;
      }

      const closesAt = category.closes_at;
      const timeParts = closesAt.split(':');
      const hours = parseInt(timeParts[0], 10);
      const minutes = parseInt(timeParts[1], 10);
      const closeTimeMinutes = hours * 60 + minutes;

      console.log(`Task ${task.id}: closes at ${closesAt} (${closeTimeMinutes} minutes), current: ${currentTime} minutes`);

      const taskCard: TaskCard = {
        id: task.id!,
        taskName: task.name,
        categoryName: category.name,
        closesAt: this.formatClosesAt(closesAt),
        timeInfo: '',
        status: 'open'
      };

      if (currentTime > closeTimeMinutes) {
        const minutesSince = currentTime - closeTimeMinutes;
        taskCard.timeInfo = this.calculateTimeSince(minutesSince);
        taskCard.status = 'missed';
        this.missedTasks.push(taskCard);
        console.log(`Task ${task.id} is MISSED (${minutesSince} minutes past close time)`);
      } else {
        const minutesUntil = closeTimeMinutes - currentTime;
        taskCard.timeInfo = this.calculateTimeUntil(minutesUntil);
        taskCard.status = 'open';
        this.openTasks.push(taskCard);
        console.log(`Task ${task.id} is OPEN (${minutesUntil} minutes until close time)`);
      }
    });

    console.log('Task categorization complete:');
    console.log('- Open tasks:', this.openTasks.length);
    console.log('- Missed tasks:', this.missedTasks.length);
  }

  calculateTimeUntil(minutes: number): string {
    if (minutes < 60) {
      return `Closes in ${minutes} minute${minutes !== 1 ? 's' : ''}`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (mins === 0) {
      return `Closes in ${hours} hour${hours !== 1 ? 's' : ''}`;
    }
    return `Closes in ${hours}h ${mins}m`;
  }

  calculateTimeSince(minutes: number): string {
    if (minutes < 60) {
      return `Missed by ${minutes} minute${minutes !== 1 ? 's' : ''}`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    if (mins === 0) {
      return `Missed by ${hours} hour${hours !== 1 ? 's' : ''}`;
    }
    return `Missed by ${hours}h ${mins}m`;
  }

  formatClosesAt(time: string): string {
    const parts = time.split(':');
    let hours = parseInt(parts[0], 10);
    const minutes = parts[1];
    const ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12 || 12;
    return `${hours}:${minutes} ${ampm}`;
  }

  loadMyDefects(): void {
    if (!this.currentUser?.id) return;

    this.defectService.getAll().subscribe({
      next: (defects) => {
        this.myOpenDefects = defects.filter(d =>
          d.reported_by === this.currentUser!.id &&
          d.status === DefectStatus.OPEN
        );
      },
      error: (err) => {
        console.error('Error loading defects:', err);
      }
    });
  }

  viewTask(taskId: number): void {
    this.router.navigate(['/site-user/tasks', taskId]);
  }

  viewDefect(defectId: number): void {
    this.router.navigate(['/site-user/defects', defectId]);
  }

  getSeverityColor(severity: string): string {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return 'bg-red-600 text-white';
      case 'high':
        return 'bg-orange-600 text-white';
      case 'medium':
        return 'bg-yellow-600 text-white';
      case 'low':
        return 'bg-blue-600 text-white';
      default:
        return 'bg-gray-600 text-white';
    }
  }

  getDefectStatusColor(status: string): string {
    switch (status?.toLowerCase()) {
      case 'open':
        return 'bg-red-100 text-red-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'closed':
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }
}
