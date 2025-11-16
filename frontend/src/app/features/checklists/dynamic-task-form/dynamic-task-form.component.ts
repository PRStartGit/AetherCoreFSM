import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TaskFieldService } from '../../../core/services/task-field.service';
import { TaskField, TaskFieldType } from '../../../core/models/monitoring.model';

@Component({
  selector: 'app-dynamic-task-form',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './dynamic-task-form.component.html',
  styleUrl: './dynamic-task-form.component.scss'
})
export class DynamicTaskFormComponent implements OnInit {
  @Input() taskId!: number;
  @Input() checklistItemId!: number;
  @Output() formSubmitted = new EventEmitter<any>();

  dynamicForm: FormGroup;
  taskFields: TaskField[] = [];
  loading = false;
  submitting = false;

  TaskFieldType = TaskFieldType;

  constructor(
    private fb: FormBuilder,
    private taskFieldService: TaskFieldService,
    private snackBar: MatSnackBar
  ) {
    this.dynamicForm = this.fb.group({});
  }

  ngOnInit(): void {
    if (this.taskId) {
      this.loadTaskFields();
    }
  }

  loadTaskFields(): void {
    this.loading = true;
    this.taskFieldService.getAllFields(this.taskId).subscribe({
      next: (fields) => {
        this.taskFields = fields.sort((a, b) => a.field_order - b.field_order);
        this.buildForm();
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading task fields:', error);
        this.snackBar.open('Failed to load form fields', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  buildForm(): void {
    this.taskFields.forEach(field => {
      const validators = field.is_required ? [Validators.required] : [];

      // Add additional validators based on field type
      if (field.field_type === TaskFieldType.NUMBER || field.field_type === TaskFieldType.TEMPERATURE) {
        const rules = field.validation_rules;
        if (rules?.min !== undefined) {
          validators.push(Validators.min(rules.min));
        }
        if (rules?.max !== undefined) {
          validators.push(Validators.max(rules.max));
        }
      }

      this.dynamicForm.addControl(
        `field_${field.id}`,
        this.fb.control('', validators)
      );
    });
  }

  getFieldIcon(fieldType: string): string {
    const icons: { [key: string]: string } = {
      [TaskFieldType.NUMBER]: '🔢',
      [TaskFieldType.TEXT]: '📝',
      [TaskFieldType.TEMPERATURE]: '🌡️',
      [TaskFieldType.YES_NO]: '✓✗',
      [TaskFieldType.DROPDOWN]: '📋',
      [TaskFieldType.PHOTO]: '📷',
      [TaskFieldType.REPEATING_GROUP]: '🔁'
    };
    return icons[fieldType] || '📝';
  }

  onSubmit(): void {
    if (this.dynamicForm.invalid) {
      this.snackBar.open('Please fill in all required fields', 'Close', { duration: 3000 });
      return;
    }

    this.submitting = true;

    // Build responses array
    const responses = this.taskFields.map(field => {
      const value = this.dynamicForm.get(`field_${field.id}`)?.value;
      const response: any = {
        task_field_id: field.id
      };

      // Set the appropriate value field based on field type
      switch (field.field_type) {
        case TaskFieldType.NUMBER:
        case TaskFieldType.TEMPERATURE:
          response.number_value = parseFloat(value);
          break;
        case TaskFieldType.YES_NO:
          response.boolean_value = value === 'true' || value === true;
          break;
        case TaskFieldType.DROPDOWN:
        case TaskFieldType.TEXT:
          response.text_value = value;
          break;
        case TaskFieldType.PHOTO:
          response.file_url = value;
          break;
        case TaskFieldType.REPEATING_GROUP:
          response.json_value = value;
          break;
        default:
          response.text_value = value;
      }

      return response;
    });

    const submission = {
      checklist_item_id: this.checklistItemId,
      responses: responses
    };

    this.taskFieldService.submitResponses(submission).subscribe({
      next: (result) => {
        this.snackBar.open('Form submitted successfully!', 'Close', { duration: 3000 });
        this.submitting = false;
        this.formSubmitted.emit(result);
      },
      error: (error) => {
        console.error('Error submitting form:', error);
        this.snackBar.open('Failed to submit form', 'Close', { duration: 3000 });
        this.submitting = false;
      }
    });
  }

  isOutOfRange(field: TaskField): boolean {
    const value = this.dynamicForm.get(`field_${field.id}`)?.value;
    if (!value || !field.validation_rules) return false;

    const numValue = parseFloat(value);
    if (isNaN(numValue)) return false;

    const rules = field.validation_rules;
    return (rules.min !== undefined && numValue < rules.min) ||
           (rules.max !== undefined && numValue > rules.max);
  }

  getValidationMessage(field: TaskField): string {
    const rules = field.validation_rules;
    if (!rules) return '';

    if (rules.min !== undefined && rules.max !== undefined) {
      return `Expected range: ${rules.min} - ${rules.max}`;
    } else if (rules.min !== undefined) {
      return `Minimum: ${rules.min}`;
    } else if (rules.max !== undefined) {
      return `Maximum: ${rules.max}`;
    }
    return '';
  }
}
