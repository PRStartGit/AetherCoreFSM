import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { forkJoin } from 'rxjs';
import { ChecklistService } from '../../../core/services/checklist.service';
import { TaskService } from '../../../core/services/task.service';
import { TaskFieldService } from '../../../core/services/task-field.service';
import { Checklist, ChecklistItem, Task, ChecklistStatus, TaskField, TaskFieldResponse } from '../../../core/models';

interface ChecklistItemWithTask extends ChecklistItem {
  task?: Task;
}

interface ChecklistItemResponses {
  responses: TaskFieldResponse[];
  fields: TaskField[];
}

@Component({
  selector: 'app-checklist-completion',
  templateUrl: './checklist-completion.component.html',
  styleUrls: ['./checklist-completion.component.scss']
})
export class ChecklistCompletionComponent implements OnInit {
  checklist: Checklist | null = null;
  items: ChecklistItemWithTask[] = [];
  loading = true;
  error: string | null = null;
  checklistId: number = 0;
  itemResponses: Map<number, ChecklistItemResponses> = new Map();

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private checklistService: ChecklistService,
    private taskService: TaskService,
    private taskFieldService: TaskFieldService
  ) {}

  ngOnInit(): void {
    this.checklistId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadChecklist();
  }

  loadChecklist(): void {
    this.loading = true;
    this.error = null;

    this.checklistService.getById(this.checklistId).subscribe({
      next: (checklist) => {
        this.checklist = checklist;

        // Load task details for each item
        if (checklist.items && checklist.items.length > 0) {
          const taskRequests = checklist.items.map(item =>
            this.taskService.getById(item.task_id)
          );

          forkJoin(taskRequests).subscribe({
            next: (tasks) => {
              this.items = checklist.items!.map((item, index) => ({
                ...item,
                task: tasks[index]
              }));
              // Load responses for completed items with dynamic forms
              this.loadCompletedResponses();
            },
            error: (err) => {
              console.error('Error loading tasks:', err);
              this.error = 'Failed to load task details';
              this.loading = false;
            }
          });
        } else {
          this.items = [];
          this.loading = false;
        }
      },
      error: (err) => {
        console.error('Error loading checklist:', err);
        this.error = 'Failed to load checklist';
        this.loading = false;
      }
    });
  }

  onItemCompleted(item: ChecklistItemWithTask): void {
    // Update the item's completed status
    this.checklistService.updateItem(this.checklistId, item.id, {
      is_completed: true
    }).subscribe({
      next: () => {
        item.is_completed = true;
        this.checkForCompletion();
      },
      error: (err) => {
        console.error('Error updating item:', err);
        this.error = 'Failed to update item';
      }
    });
  }

  checkForCompletion(): void {
    const allCompleted = this.items.every(item => item.is_completed);
    if (allCompleted && this.checklist) {
      this.checklist.status = ChecklistStatus.COMPLETED;
      // Navigate back to checklist list
      setTimeout(() => {
        this.router.navigate(['/checklists']);
      }, 500);
    }
  }

  goBack(): void {
    this.router.navigate(['/checklists']);
  }

  getProgressPercentage(): number {
    if (this.items.length === 0) return 0;
    const completed = this.getCompletedCount();
    return Math.round((completed / this.items.length) * 100);
  }

  getCompletedCount(): number {
    return this.items.filter(item => item.is_completed).length;
  }

  loadCompletedResponses(): void {
    const completedDynamicItems = this.items.filter(
      item => item.is_completed && item.task?.has_dynamic_form
    );

    if (completedDynamicItems.length === 0) {
      this.loading = false;
      return;
    }

    const responseRequests = completedDynamicItems.map(item => {
      return forkJoin({
        responses: this.taskFieldService.getResponses(item.id),
        fields: this.taskFieldService.getAllFields(item.task_id)
      });
    });

    forkJoin(responseRequests).subscribe({
      next: (results) => {
        completedDynamicItems.forEach((item, index) => {
          this.itemResponses.set(item.id, results[index]);
        });
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading responses:', err);
        this.loading = false;
      }
    });
  }

  getResponseValue(response: TaskFieldResponse, field: TaskField): string {
    // Return the appropriate value based on field type
    if (response.boolean_value !== null && response.boolean_value !== undefined) {
      return response.boolean_value ? 'Yes' : 'No';
    }
    if (response.number_value !== null && response.number_value !== undefined) {
      return response.number_value.toString();
    }
    if (response.text_value) {
      return response.text_value;
    }
    if (response.file_url) {
      return 'Photo uploaded';
    }
    if (response.json_value) {
      return JSON.stringify(response.json_value);
    }
    return 'N/A';
  }

  getFieldForResponse(itemId: number, response: TaskFieldResponse): TaskField | undefined {
    const itemData = this.itemResponses.get(itemId);
    if (!itemData) return undefined;
    return itemData.fields.find(f => f.id === response.task_field_id);
  }
}
