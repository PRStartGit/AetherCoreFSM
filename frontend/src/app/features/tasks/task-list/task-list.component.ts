import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TaskService } from '../../../core/services/task.service';
import { CategoryService } from '../../../core/services/category.service';
import { SiteService } from '../../../core/services/site.service';
import { AuthService } from '../../../core/auth/auth.service';
import { Task, Category } from '../../../core/models/monitoring.model';
import { Site } from '../../../core/models';
import { TaskFormComponent } from '../task-form/task-form.component';

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
  styleUrls: ['./task-list.component.scss']
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];
  categories: Category[] = [];
  sites: Site[] = [];
  loading = false;
  displayedColumns: string[] = ['name', 'category', 'sites', 'status', 'actions'];

  // Filter properties
  searchTerm: string = '';
  selectedFrequency: string = 'all';

  // Available frequencies
  frequencies = ['daily', 'weekly', 'monthly', 'six_monthly', 'yearly'];

  constructor(
    private taskService: TaskService,
    private categoryService: CategoryService,
    private siteService: SiteService,
    private authService: AuthService,
    private dialog: MatDialog,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadTasks();
    this.loadCategories();
    this.loadSites();
  }

  loadTasks(): void {
    this.loading = true;
    this.taskService.getAll().subscribe({
      next: (tasks: any[]) => {
        this.tasks = tasks;
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading tasks:', error);
        this.snackBar.open('Failed to load tasks', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  loadCategories(): void {
    const user = this.authService.getUser();
    const isSuperAdmin = user?.role === 'super_admin';
    this.categoryService.getAll(isSuperAdmin ? undefined : false).subscribe({
      next: (categories: any[]) => {
        this.categories = categories.filter((c: any) => c.is_active);
      },
      error: (error: any) => {
        console.error('Error loading categories:', error);
      }
    });
  }

  loadSites(): void {
    this.siteService.getAll().subscribe({
      next: (sites: any[]) => {
        this.sites = sites;
      },
      error: (error: any) => {
        console.error('Error loading sites:', error);
      }
    });
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(TaskFormComponent, {
      width: '700px',
      data: {
        task: null,
        categories: this.categories,
        sites: this.sites
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadTasks();
      }
    });
  }

  openEditDialog(task: Task): void {
    const dialogRef = this.dialog.open(TaskFormComponent, {
      width: '700px',
      data: {
        task: task,
        categories: this.categories,
        sites: this.sites
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.loadTasks();
      }
    });
  }

  deleteTask(task: Task): void {
    if (confirm(`Are you sure you want to delete task "${task.name}"?`)) {
      this.taskService.delete(task.id).subscribe({
        next: () => {
          this.snackBar.open('Task deleted successfully', 'Close', { duration: 3000 });
          this.loadTasks();
        },
        error: (error: any) => {
          console.error('Error deleting task:', error);
          this.snackBar.open('Failed to delete task', 'Close', { duration: 3000 });
        }
      });
    }
  }

  getCategoryName(categoryId: number): string {
    const category = this.categories.find(c => c.id === categoryId);
    return category?.name || 'Unknown';
  }

  getCategoryFrequency(categoryId: number): string {
    const category = this.categories.find(c => c.id === categoryId);
    return category?.frequency || '';
  }

  getSiteNames(siteIds: number[]): string {
    if (!siteIds || siteIds.length === 0) {
      return 'All Sites';
    }
    const names = siteIds
      .map(id => this.sites.find(s => s.id === id)?.name)
      .filter(name => name);
    return names.length > 0 ? names.join(', ') : 'All Sites';
  }

  get filteredTasks(): Task[] {
    return this.tasks.filter(task => {
      // Filter by search term
      const matchesSearch = !this.searchTerm ||
        task.name.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
        task.description?.toLowerCase().includes(this.searchTerm.toLowerCase());

      // Filter by frequency
      const category = this.categories.find(c => c.id === task.category_id);
      const matchesFrequency = this.selectedFrequency === 'all' ||
        category?.frequency === this.selectedFrequency;

      return matchesSearch && matchesFrequency;
    });
  }
}
