import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { TaskFieldService } from '../../../core/services/task-field.service';
import { TaskField, TaskFieldType } from '../../../core/models/monitoring.model';
import { CdkDragDrop, moveItemInArray, DragDropModule } from '@angular/cdk/drag-drop';

@Component({
  selector: 'app-task-field-builder',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, DragDropModule],
  templateUrl: './task-field-builder.component.html',
  styleUrl: './task-field-builder.component.scss'
})
export class TaskFieldBuilderComponent implements OnInit {
  @Input() taskId!: number;
  @Output() fieldsSaved = new EventEmitter<TaskField[]>();

  fieldsForm: FormGroup;
  existingFields: TaskField[] = [];
  loading = false;
  saving = false;

  fieldTypes = [
    { value: TaskFieldType.NUMBER, label: 'Number', icon: '🔢' },
    { value: TaskFieldType.TEXT, label: 'Text', icon: '📝' },
    { value: TaskFieldType.TEMPERATURE, label: 'Temperature', icon: '🌡️' },
    { value: TaskFieldType.YES_NO, label: 'Yes/No', icon: '✓✗' },
    { value: TaskFieldType.DROPDOWN, label: 'Dropdown', icon: '📋' },
    { value: TaskFieldType.PHOTO, label: 'Photo', icon: '📷' },
    { value: TaskFieldType.REPEATING_GROUP, label: 'Repeating Group', icon: '🔁' }
  ];

  constructor(
    private fb: FormBuilder,
    private taskFieldService: TaskFieldService,
    private snackBar: MatSnackBar
  ) {
    this.fieldsForm = this.fb.group({
      fields: this.fb.array([])
    });
  }

  ngOnInit(): void {
    if (this.taskId) {
      this.loadExistingFields();
    }
  }

  get fields(): FormArray {
    return this.fieldsForm.get('fields') as FormArray;
  }

  loadExistingFields(): void {
    this.loading = true;
    this.taskFieldService.getAllFields(this.taskId).subscribe({
      next: (fields) => {
        this.existingFields = fields.sort((a, b) => a.field_order - b.field_order);
        this.fields.clear();
        fields.forEach(field => {
          this.fields.push(this.createFieldFormGroup(field));
        });
        this.loading = false;
      },
      error: (error) => {
        console.error('Error loading fields:', error);
        this.snackBar.open('Failed to load fields', 'Close', { duration: 3000 });
        this.loading = false;
      }
    });
  }

  createFieldFormGroup(field?: TaskField): FormGroup {
    return this.fb.group({
      id: [field?.id || null],
      field_type: [field?.field_type || TaskFieldType.TEXT, Validators.required],
      field_label: [field?.field_label || '', Validators.required],
      field_order: [field?.field_order || this.fields.length],
      is_required: [field?.is_required ?? true],
      validation_rules: [field?.validation_rules || {}],
      options: [field?.options || null],
      show_if: [field?.show_if || null]
    });
  }

  addField(): void {
    const newField = this.createFieldFormGroup();
    newField.patchValue({ field_order: this.fields.length });
    this.fields.push(newField);
  }

  removeField(index: number): void {
    const field = this.fields.at(index);
    const fieldId = field.get('id')?.value;

    if (fieldId) {
      // Delete from backend
      this.taskFieldService.deleteField(fieldId).subscribe({
        next: () => {
          this.fields.removeAt(index);
          this.updateFieldOrders();
          this.snackBar.open('Field deleted successfully', 'Close', { duration: 3000 });
        },
        error: (error) => {
          console.error('Error deleting field:', error);
          this.snackBar.open('Failed to delete field', 'Close', { duration: 3000 });
        }
      });
    } else {
      // Just remove from form if not saved yet
      this.fields.removeAt(index);
      this.updateFieldOrders();
    }
  }

  onDrop(event: CdkDragDrop<any[]>): void {
    moveItemInArray(this.fields.controls, event.previousIndex, event.currentIndex);
    this.updateFieldOrders();
  }

  updateFieldOrders(): void {
    this.fields.controls.forEach((control, index) => {
      control.patchValue({ field_order: index });
    });
  }

  getFieldTypeIcon(type: string): string {
    return this.fieldTypes.find(t => t.value === type)?.icon || '📝';
  }

  needsOptions(fieldType: string): boolean {
    return fieldType === TaskFieldType.DROPDOWN;
  }

  saveFields(): void {
    if (this.fieldsForm.invalid) {
      this.snackBar.open('Please fill in all required fields', 'Close', { duration: 3000 });
      return;
    }

    this.saving = true;
    const fieldsData = this.fields.value.map((field: any) => ({
      task_id: this.taskId,
      field_type: field.field_type,
      field_label: field.field_label,
      field_order: field.field_order,
      is_required: field.is_required,
      validation_rules: field.validation_rules,
      options: field.options,
      show_if: field.show_if
    }));

    // For now, we'll delete all and recreate (simpler approach)
    // In production, you'd want to update individual fields
    const bulkData = {
      task_id: this.taskId,
      fields: fieldsData.map((f: any) => ({
        field_type: f.field_type,
        field_label: f.field_label,
        field_order: f.field_order,
        is_required: f.is_required,
        validation_rules: f.validation_rules,
        options: f.options,
        show_if: f.show_if
      }))
    };

    // Delete existing fields first
    const deletePromises = this.existingFields.map(field =>
      this.taskFieldService.deleteField(field.id).toPromise()
    );

    Promise.all(deletePromises).then(() => {
      // Then create new ones
      this.taskFieldService.createFieldsBulk(bulkData).subscribe({
        next: (createdFields) => {
          this.snackBar.open('Fields saved successfully!', 'Close', { duration: 3000 });
          this.saving = false;
          this.loadExistingFields();
          this.fieldsSaved.emit(createdFields);
        },
        error: (error) => {
          console.error('Error saving fields:', error);
          this.snackBar.open('Failed to save fields', 'Close', { duration: 3000 });
          this.saving = false;
        }
      });
    }).catch(error => {
      console.error('Error deleting old fields:', error);
      this.snackBar.open('Failed to update fields', 'Close', { duration: 3000 });
      this.saving = false;
    });
  }

  parseOptions(optionsString: string): string[] {
    return optionsString.split(',').map(o => o.trim()).filter(o => o);
  }

  formatOptions(options: string[] | null): string {
    return options ? options.join(', ') : '';
  }
}
