import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { AuthService } from '../../../core/auth/auth.service';
import { ChecklistService } from '../../../core/services/checklist.service';
import { CategoryService } from '../../../core/services/category.service';
import { DefectService } from '../../../core/services/defect.service';
import { TaskService } from '../../../core/services/task.service';
import { User } from '../../../core/models/user.model';
import { Checklist, ChecklistStatus, Category, Defect, DefectStatus, ChecklistItem, Task } from '../../../core/models/monitoring.model';

interface ChecklistItemWithTask extends ChecklistItem {
  task?: Task;
}

interface ChecklistCard {
  id: number;
  categoryName: string;
  totalItems: number;
  completedItems: number;
  completionPercentage: number;
  status: ChecklistStatus;
  dueDate: string;
  isActive?: boolean;  // Whether the checklist is open for editing based on time
  opensAt?: string | null;
  closesAt?: string | null;
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

  // Checklist arrays
  openTasks: ChecklistCard[] = [];
  missedTasks: ChecklistCard[] = [];
  completedTasks: ChecklistCard[] = [];
  futureTasks: ChecklistCard[] = [];
  openingLaterTasks: ChecklistCard[] = [];

  // Defects
  myOpenDefects: Defect[] = [];

  // Categories map
  categoriesMap: Map<number, Category> = new Map();

  // Expandable checklist state
  expandedChecklists: Set<number> = new Set();
  checklistItems: Map<number, ChecklistItemWithTask[]> = new Map();
  loadingItems: Set<number> = new Set();

  constructor(
    private authService: AuthService,
    private checklistService: ChecklistService,
    private categoryService: CategoryService,
    private defectService: DefectService,
    private taskService: TaskService,
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
        this.loadChecklists();
        this.loadMyDefects();
      },
      error: (err) => {
        console.error('Error loading categories:', err);
        this.error = 'Failed to load categories';
      }
    });
  }

  loadChecklists(): void {
    this.loading = true;
    this.error = null;

    const siteId = this.currentUser?.site_ids?.[0];

    if (!siteId) {
      this.error = 'No site assigned to user';
      this.loading = false;
      return;
    }

    // Get today's date in YYYY-MM-DD format
    const today = new Date();
    const todayStr = today.toISOString().split('T')[0];

    // Get end of current month
    const futureDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    const futureDateStr = futureDate.toISOString().split('T')[0];

    // Load checklists from today to end of current month
    console.log('Loading checklists from', todayStr, 'to', futureDateStr);
    this.checklistService.getAll(siteId, undefined, undefined, todayStr, futureDateStr).subscribe({
      next: (checklists) => {
        console.log('Loaded checklists:', checklists);
        console.log('Number of checklists loaded:', checklists.length);
        this.processChecklists(checklists, todayStr);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading checklists:', err);
        this.error = 'Failed to load checklists';
        this.loading = false;
      }
    });
  }

  processChecklists(checklists: Checklist[], todayStr: string): void {
    this.openTasks = [];
    this.missedTasks = [];
    this.completedTasks = [];
    this.futureTasks = [];
    this.openingLaterTasks = [];

    const today = new Date(todayStr);
    today.setHours(0, 0, 0, 0);
    console.log('Today (for comparison):', today.toISOString(), '(timestamp:', today.getTime(), ')');

    checklists.forEach(checklist => {
      const category = this.categoriesMap.get(checklist.category_id);

      if (!category) {
        console.log(`Checklist ${checklist.id} has no category, skipping`);
        return;
      }

      // Check if checklist is currently active based on time window
      const isActive = this.isChecklistActive(category);

      const card: ChecklistCard = {
        id: checklist.id,
        categoryName: category.name,
        totalItems: checklist.total_items || 0,
        completedItems: checklist.completed_items || 0,
        completionPercentage: checklist.completion_percentage || 0,
        status: checklist.status,
        dueDate: checklist.checklist_date,
        isActive: isActive,
        opensAt: category.opens_at,
        closesAt: category.closes_at
      };

      const checklistDate = new Date(checklist.checklist_date);
      checklistDate.setHours(0, 0, 0, 0);

      console.log(`Checklist ${checklist.id} (${category.name}):`,
                  'Date:', checklist.checklist_date,
                  'Parsed:', checklistDate.toISOString(),
                  'Timestamp:', checklistDate.getTime(),
                  'Status:', checklist.status,
                  'Frequency:', category.frequency,
                  'Is future?', checklistDate > today,
                  'Is active?', isActive);

      switch (checklist.status) {
        case ChecklistStatus.PENDING:
        case ChecklistStatus.IN_PROGRESS:
          // Check if the due date is in the future (not today)
          if (checklistDate > today) {
            // Exclude daily tasks from future tasks (based on category name)
            const dailyCategories = ['opening checks', 'closing checks', 'food safety', 'cleaning', 'morning checks', 'afternoon checks', 'evening checks'];
            const isDailyTask = dailyCategories.some(dc => category.name.toLowerCase().includes(dc));

            if (isDailyTask) {
              console.log(`  -> Skipping FUTURE tasks (daily category: ${category.name})`);
              // Don't add daily tasks to future section
            } else {
              console.log(`  -> Adding to FUTURE tasks`);
              this.futureTasks.push(card);
            }
          } else {
            console.log(`  -> Adding to OPEN tasks`);
            this.openTasks.push(card);
          }
          break;
        case ChecklistStatus.COMPLETED:
          console.log(`  -> Adding to COMPLETED tasks`);
          this.completedTasks.push(card);
          break;
        case ChecklistStatus.OVERDUE:
          console.log(`  -> Adding to MISSED tasks`);
          this.missedTasks.push(card);
          break;
      }
    });

    console.log('Checklist categorization complete:');
    console.log('- Open (pending/in-progress - due today):', this.openTasks.length);
    console.log('- Future (pending/in-progress - due later):', this.futureTasks.length);
    console.log('- Missed (overdue):', this.missedTasks.length);
    console.log('- Completed:', this.completedTasks.length);
  }

  isChecklistActive(category: Category): boolean {
    // If no time restrictions, it's always active
    if (!category.opens_at && !category.closes_at) {
      return true;
    }

    const now = new Date();
    const currentTime = now.getHours() * 60 + now.getMinutes(); // Current time in minutes since midnight

    // Parse opens_at time (format: "HH:MM:SS")
    let opensAtMinutes = 0;
    if (category.opens_at) {
      const [hours, minutes] = category.opens_at.split(':').map(Number);
      opensAtMinutes = hours * 60 + minutes;
    }

    // Parse closes_at time (format: "HH:MM:SS")
    let closesAtMinutes = 24 * 60; // Default to end of day
    if (category.closes_at) {
      const [hours, minutes] = category.closes_at.split(':').map(Number);
      closesAtMinutes = hours * 60 + minutes;
    }

    // Check if current time is within the window
    return currentTime >= opensAtMinutes && currentTime <= closesAtMinutes;
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

  viewTask(checklistId: number): void {
    this.router.navigate(['/checklists', checklistId, 'complete']);
  }

  viewDefect(defectId: number): void {
    this.router.navigate(['/defects', defectId, 'edit']);
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

  formatDate(dateString: string): string {
    if (!dateString) return '';
    const date = new Date(dateString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  }

  formatDueDate(dueDate: string): string {
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const due = new Date(dueDate);
    due.setHours(0, 0, 0, 0);

    const diffTime = due.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) {
      return 'Today';
    } else if (diffDays === 1) {
      return 'Tomorrow';
    } else if (diffDays > 0 && diffDays <= 7) {
      return `Due in ${diffDays} days`;
    } else if (diffDays > 7 && diffDays <= 30) {
      return 'Due this month';
    } else if (diffDays < 0 && diffDays >= -7) {
      return `Overdue by ${Math.abs(diffDays)} days`;
    } else if (diffDays < -7) {
      return 'Overdue';
    }

    return this.formatDate(dueDate);
  }

  toggleChecklist(checklistId: number): void {
    if (this.expandedChecklists.has(checklistId)) {
      // Collapse the checklist
      this.expandedChecklists.delete(checklistId);
    } else {
      // Expand the checklist
      this.expandedChecklists.add(checklistId);

      // Load items if not already loaded
      if (!this.checklistItems.has(checklistId)) {
        this.loadChecklistItems(checklistId);
      }
    }
  }

  loadChecklistItems(checklistId: number): void {
    this.loadingItems.add(checklistId);

    this.checklistService.getById(checklistId).subscribe({
      next: (checklist) => {
        // Load task details for each item to get has_dynamic_form flag
        if (checklist.items && checklist.items.length > 0) {
          const taskRequests = checklist.items.map(item =>
            this.taskService.getById(item.task_id)
          );

          forkJoin(taskRequests).subscribe({
            next: (tasks) => {
              const itemsWithTasks: ChecklistItemWithTask[] = checklist.items!.map((item, index) => ({
                ...item,
                task: tasks[index]
              }));
              this.checklistItems.set(checklistId, itemsWithTasks);
              this.loadingItems.delete(checklistId);
            },
            error: (err) => {
              console.error('Error loading tasks:', err);
              this.checklistItems.set(checklistId, checklist.items || []);
              this.loadingItems.delete(checklistId);
            }
          });
        } else {
          this.checklistItems.set(checklistId, []);
          this.loadingItems.delete(checklistId);
        }
      },
      error: (err) => {
        console.error('Error loading checklist items:', err);
        this.loadingItems.delete(checklistId);
      }
    });
  }

  toggleItem(checklistId: number, item: ChecklistItemWithTask): void {
    const newCompletedState = !item.is_completed;

    this.checklistService.updateItem(checklistId, item.id, {
      is_completed: newCompletedState
    }).subscribe({
      next: () => {
        // Update the item in the local state
        item.is_completed = newCompletedState;

        // Reload the checklist to update progress
        this.loadChecklists();
      },
      error: (err) => {
        console.error('Error updating checklist item:', err);
      }
    });
  }

  onDynamicFormSubmitted(checklistId: number, item: ChecklistItemWithTask): void {
    // Mark item as completed and reload
    item.is_completed = true;
    this.loadChecklists();
  }

  getOverallCompletionPercentage(): number {
    const allTasks = [...this.openTasks, ...this.missedTasks, ...this.completedTasks];
    if (allTasks.length === 0) return 0;

    const totalItems = allTasks.reduce((sum, task) => sum + task.totalItems, 0);
    const completedItems = allTasks.reduce((sum, task) => sum + task.completedItems, 0);

    return totalItems > 0 ? Math.round((completedItems / totalItems) * 100) : 0;
  }

  getProgressDashOffset(): number {
    const percentage = this.getOverallCompletionPercentage();
    const circumference = 2 * Math.PI * 45; // 45 is the radius
    return circumference - (percentage / 100) * circumference;
  }

  getTimeRangeDisplay(opensAt: string | null | undefined, closesAt: string | null | undefined): string {
    if (!opensAt && !closesAt) return '';

    const formatTime = (timeStr: string | null | undefined): string => {
      if (!timeStr) return '';
      const [hours, minutes] = timeStr.split(':').map(Number);
      return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;
    };

    if (opensAt && closesAt) {
      return `${formatTime(opensAt)} - ${formatTime(closesAt)}`;
    } else if (opensAt) {
      return `Opens at ${formatTime(opensAt)}`;
    } else if (closesAt) {
      return `Closes at ${formatTime(closesAt)}`;
    }
    return '';
  }
}
