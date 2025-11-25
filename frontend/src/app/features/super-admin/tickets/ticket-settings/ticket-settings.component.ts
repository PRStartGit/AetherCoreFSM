import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar } from '@angular/material/snack-bar';

interface TicketCategory {
  id: number;
  name: string;
  description: string | null;
  is_active: boolean;
  sort_order: number;
  created_at: string;
}

interface TicketSettings {
  ticketing_enabled: boolean;
  auto_assign_enabled: boolean;
  email_notifications_enabled: boolean;
  default_priority: string;
  sla_response_hours: number;
}

@Component({
  selector: 'app-ticket-settings',
  templateUrl: './ticket-settings.component.html',
  styleUrls: ['./ticket-settings.component.css']
})
export class TicketSettingsComponent implements OnInit {
  categories: TicketCategory[] = [];
  settings: TicketSettings = {
    ticketing_enabled: true,
    auto_assign_enabled: false,
    email_notifications_enabled: true,
    default_priority: 'medium',
    sla_response_hours: 24
  };

  loading = true;
  savingSettings = false;

  // New category form
  showCategoryForm = false;
  editingCategory: TicketCategory | null = null;
  categoryForm = {
    name: '',
    description: '',
    is_active: true,
    sort_order: 0
  };
  savingCategory = false;

  priorities = [
    { value: 'low', label: 'Low' },
    { value: 'medium', label: 'Medium' },
    { value: 'high', label: 'High' },
    { value: 'urgent', label: 'Urgent' }
  ];

  constructor(
    private http: HttpClient,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;

    // Load settings
    this.http.get<TicketSettings>('/api/v1/ticket-settings/settings').subscribe({
      next: (settings) => {
        this.settings = settings;
      },
      error: (err) => {
        console.error('Error loading settings:', err);
      }
    });

    // Load categories
    this.http.get<TicketCategory[]>('/api/v1/ticket-settings/categories?include_inactive=true').subscribe({
      next: (categories) => {
        this.categories = categories;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading categories:', err);
        this.loading = false;
      }
    });
  }

  saveSettings(): void {
    this.savingSettings = true;
    this.http.patch<TicketSettings>('/api/v1/ticket-settings/settings', this.settings).subscribe({
      next: (settings) => {
        this.settings = settings;
        this.savingSettings = false;
        this.snackBar.open('Settings saved successfully', 'Close', { duration: 3000 });
      },
      error: (err) => {
        console.error('Error saving settings:', err);
        this.savingSettings = false;
        this.snackBar.open('Error saving settings', 'Close', { duration: 3000 });
      }
    });
  }

  openCategoryForm(category?: TicketCategory): void {
    if (category) {
      this.editingCategory = category;
      this.categoryForm = {
        name: category.name,
        description: category.description || '',
        is_active: category.is_active,
        sort_order: category.sort_order
      };
    } else {
      this.editingCategory = null;
      this.categoryForm = {
        name: '',
        description: '',
        is_active: true,
        sort_order: this.categories.length
      };
    }
    this.showCategoryForm = true;
  }

  closeCategoryForm(): void {
    this.showCategoryForm = false;
    this.editingCategory = null;
  }

  saveCategory(): void {
    if (!this.categoryForm.name) return;

    this.savingCategory = true;

    if (this.editingCategory) {
      // Update existing
      this.http.patch<TicketCategory>(`/api/v1/ticket-settings/categories/${this.editingCategory.id}`, this.categoryForm).subscribe({
        next: (category) => {
          const idx = this.categories.findIndex(c => c.id === category.id);
          if (idx >= 0) this.categories[idx] = category;
          this.savingCategory = false;
          this.closeCategoryForm();
          this.snackBar.open('Category updated', 'Close', { duration: 3000 });
        },
        error: (err) => {
          console.error('Error updating category:', err);
          this.savingCategory = false;
        }
      });
    } else {
      // Create new
      this.http.post<TicketCategory>('/api/v1/ticket-settings/categories', this.categoryForm).subscribe({
        next: (category) => {
          this.categories.push(category);
          this.savingCategory = false;
          this.closeCategoryForm();
          this.snackBar.open('Category created', 'Close', { duration: 3000 });
        },
        error: (err) => {
          console.error('Error creating category:', err);
          this.savingCategory = false;
        }
      });
    }
  }

  toggleCategoryActive(category: TicketCategory): void {
    this.http.patch<TicketCategory>(`/api/v1/ticket-settings/categories/${category.id}`, {
      is_active: !category.is_active
    }).subscribe({
      next: (updated) => {
        const idx = this.categories.findIndex(c => c.id === updated.id);
        if (idx >= 0) this.categories[idx] = updated;
      }
    });
  }

  deleteCategory(category: TicketCategory): void {
    if (!confirm(`Are you sure you want to deactivate "${category.name}"?`)) return;

    this.http.delete(`/api/v1/ticket-settings/categories/${category.id}`).subscribe({
      next: () => {
        category.is_active = false;
        this.snackBar.open('Category deactivated', 'Close', { duration: 3000 });
      }
    });
  }
}
