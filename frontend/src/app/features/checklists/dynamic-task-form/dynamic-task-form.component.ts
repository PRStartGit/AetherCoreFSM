import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { TaskFieldService } from '../../../core/services/task-field.service';
import { TaskField, TaskFieldType } from '../../../core/models/monitoring.model';

@Component({
  selector: 'app-dynamic-task-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    MatSlideToggleModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatSnackBarModule
  ],
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

  // Track repeating group instances
  repeatingGroups: Map<number, any[]> = new Map();

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
      // Skip repeating group fields - they don't have a single control
      // Their instance controls are created by updateRepeatingGroups()
      if (field.field_type === TaskFieldType.REPEATING_GROUP) {
        return;
      }

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

    // Store scroll position before submit to prevent jump on mobile
    const scrollY = window.scrollY;

    this.submitting = true;

    // Build responses array
    const responses = this.taskFields.map(field => {
      const response: any = {
        checklist_item_id: this.checklistItemId,
        task_field_id: field.id
      };

      // Handle repeating groups specially
      if (field.field_type === TaskFieldType.REPEATING_GROUP) {
        const instances = this.getRepeatingInstances(field.id);
        const groupData: any[] = [];

        instances.forEach((instance, idx) => {
          const instanceData: any = {};
          if (field.validation_rules?.repeat_template) {
            field.validation_rules.repeat_template.forEach((template: any) => {
              const controlName = `field_${field.id}_${idx}_${template.type}`;
              const value = this.dynamicForm.get(controlName)?.value;

              // Store based on template type
              if (template.type === 'temperature' || template.type === 'number') {
                instanceData[template.type] = parseFloat(value) || null;
              } else if (template.type === 'photo') {
                instanceData[template.type] = value || null;
              } else {
                instanceData[template.type] = value || null;
              }
            });
          }
          groupData.push(instanceData);
        });

        response.json_value = groupData;
      } else {
        // Handle regular fields
        const value = this.dynamicForm.get(`field_${field.id}`)?.value;

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
          default:
            response.text_value = value;
        }
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
        // Restore scroll position after DOM update to prevent mobile jump
        setTimeout(() => window.scrollTo(0, scrollY), 50);
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

  onPhotoSelected(event: any, field: TaskField): void {
    const file = event.target?.files?.[0];
    if (file) {
      // For now, just store the filename. In production, you'd upload to cloud storage
      const filename = `photo_${Date.now()}_${file.name}`;
      this.dynamicForm.get(`field_${field.id}`)?.setValue(filename);

      // TODO: Implement actual file upload to cloud storage (S3, etc.)
      console.log('Photo selected:', file.name);
    }
  }

  onPhotoSelectedRepeating(event: any, fieldId: number, index: number, subFieldType: string): void {
    const file = event.target?.files?.[0];
    if (file) {
      const filename = `photo_${Date.now()}_${file.name}`;
      const controlName = `field_${fieldId}_${index}_${subFieldType}`;
      this.dynamicForm.get(controlName)?.setValue(filename);
      console.log('Photo selected for repeating field:', file.name);
    }
  }

  updateRepeatingGroups(countFieldId: number, count: number): void {
    // Find all repeating group fields that depend on this count field
    const repeatingFields = this.taskFields.filter(f =>
      f.field_type === TaskFieldType.REPEATING_GROUP &&
      f.validation_rules?.repeat_count_field_id === countFieldId
    );

    repeatingFields.forEach(field => {
      // Generate instances based on count
      const instances = [];
      for (let i = 0; i < count; i++) {
        instances.push({ index: i, label: `${field.validation_rules.repeat_label || 'Item'} ${i + 1}` });
      }
      this.repeatingGroups.set(field.id, instances);

      // Create form controls for each instance
      if (field.validation_rules?.repeat_template) {
        field.validation_rules.repeat_template.forEach((template: any) => {
          for (let i = 0; i < count; i++) {
            const controlName = `field_${field.id}_${i}_${template.type}`;
            // Remove old control if exists
            if (this.dynamicForm.contains(controlName)) {
              this.dynamicForm.removeControl(controlName);
            }

            // Add new control with appropriate validators
            // Temperature/number fields are required, photos are optional
            const validators = [];
            if (template.type === 'temperature' || template.type === 'number') {
              // Temperature fields are always required in repeating groups
              validators.push(Validators.required);
            }
            // Photo fields are always optional (no validators)

            this.dynamicForm.addControl(controlName, this.fb.control('', validators));
            console.log(`Created control ${controlName} with validators:`, validators.length > 0 ? 'required' : 'optional');
          }
        });
      }
    });
  }

  onCountChange(field: TaskField): void {
    const count = parseInt(this.dynamicForm.get(`field_${field.id}`)?.value) || 0;
    this.updateRepeatingGroups(field.id, count);
  }

  getRepeatingInstances(fieldId: number): any[] {
    return this.repeatingGroups.get(fieldId) || [];
  }
}
