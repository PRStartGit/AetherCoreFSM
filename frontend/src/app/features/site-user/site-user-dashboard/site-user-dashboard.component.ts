import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { ChecklistService } from '../../../core/services/checklist.service';
import { CategoryService } from '../../../core/services/category.service';
import { DefectService } from '../../../core/services/defect.service';
import { User } from '../../../core/models/user.model';
import { Checklist, ChecklistStatus, Category, Defect, DefectStatus, ChecklistItem } from '../../../core/models/monitoring.model';

interface ChecklistCard {
  id: number;
  categoryName: string;
  totalItems: number;
  completedItems: number;
  completionPercentage: number;
  status: ChecklistStatus;
  dueDate: string;
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
  openingLaterTasks: ChecklistCard[] = [];

  // Defects
  myOpenDefects: Defect[] = [];

  // Categories map
  categoriesMap: Map<number, Category> = new Map();

  // Expandable checklist state
  expandedChecklists: Set<number> = new Set();
  checklistItems: Map<number, ChecklistItem[]> = new Map();
  loadingItems: Set<number> = new Set();

  constructor(
    private authService: AuthService,
    private checklistService: ChecklistService,
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
    const today = new Date().toISOString().split('T')[0];

    // Load checklists for today for this site
    this.checklistService.getAll(siteId, undefined, undefined, today, today).subscribe({
      next: (checklists) => {
        console.log('Loaded checklists for today:', checklists);
        this.processChecklists(checklists);
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading checklists:', err);
        this.error = 'Failed to load checklists';
        this.loading = false;
      }
    });
  }

  processChecklists(checklists: Checklist[]): void {
    this.openTasks = [];
    this.missedTasks = [];
    this.completedTasks = [];
    this.openingLaterTasks = [];

    checklists.forEach(checklist => {
      const category = this.categoriesMap.get(checklist.category_id);

      if (!category) {
        console.log(`Checklist ${checklist.id} has no category, skipping`);
        return;
      }

      const card: ChecklistCard = {
        id: checklist.id,
        categoryName: category.name,
        totalItems: checklist.total_items || 0,
        completedItems: checklist.completed_items || 0,
        completionPercentage: checklist.completion_percentage || 0,
        status: checklist.status,
        dueDate: checklist.checklist_date
      };

      switch (checklist.status) {
        case ChecklistStatus.PENDING:
        case ChecklistStatus.IN_PROGRESS:
          this.openTasks.push(card);
          break;
        case ChecklistStatus.COMPLETED:
          this.completedTasks.push(card);
          break;
        case ChecklistStatus.OVERDUE:
          this.missedTasks.push(card);
          break;
      }
    });

    console.log('Checklist categorization complete:');
    console.log('- Open (pending/in-progress):', this.openTasks.length);
    console.log('- Missed (overdue):', this.missedTasks.length);
    console.log('- Completed:', this.completedTasks.length);
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
        this.checklistItems.set(checklistId, checklist.items || []);
        this.loadingItems.delete(checklistId);
      },
      error: (err) => {
        console.error('Error loading checklist items:', err);
        this.loadingItems.delete(checklistId);
      }
    });
  }

  toggleItem(checklistId: number, item: ChecklistItem): void {
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
}
