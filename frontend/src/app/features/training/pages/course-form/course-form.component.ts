import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { TrainingService } from '../../services/training.service';
import { Course, CourseCategory, CourseModule, CourseModuleCreate } from '../../models/training.models';

@Component({
  selector: 'app-course-form',
  templateUrl: './course-form.component.html',
  styleUrls: ['./course-form.component.css']
})
export class CourseFormComponent implements OnInit {
  courseForm: FormGroup;
  moduleForm: FormGroup;
  isEditMode = false;
  courseId?: number;
  loading = false;
  error: string | null = null;

  categories: CourseCategory[] = [];
  modules: CourseModule[] = [];
  showModuleForm = false;
  editingModuleId?: number;

  constructor(
    private fb: FormBuilder,
    private trainingService: TrainingService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.courseForm = this.fb.group({
      title: ['', [Validators.required, Validators.maxLength(200)]],
      description: [''],
      thumbnail_url: [''],
      category_id: [null],
      is_published: [false]
    });

    this.moduleForm = this.fb.group({
      title: ['', [Validators.required, Validators.maxLength(200)]],
      description: [''],
      video_url: [''],
      pdf_url: [''],
      text_content: [''],
      duration_minutes: [null]
    });
  }

  ngOnInit(): void {
    this.loadCategories();

    const id = this.route.snapshot.paramMap.get('id');
    if (id && id !== 'new') {
      this.isEditMode = true;
      this.courseId = +id;
      this.loadCourse();
      this.loadModules();
    }
  }

  loadCategories(): void {
    this.trainingService.getCourseCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
      },
      error: (err) => {
        console.error('Error loading categories:', err);
      }
    });
  }

  loadCourse(): void {
    if (!this.courseId) return;

    this.loading = true;
    this.trainingService.getCourseById(this.courseId).subscribe({
      next: (course) => {
        this.courseForm.patchValue({
          title: course.title,
          description: course.description,
          thumbnail_url: course.thumbnail_url,
          category_id: course.category_id,
          is_published: course.is_published
        });
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load course';
        this.loading = false;
        console.error('Error loading course:', err);
      }
    });
  }

  loadModules(): void {
    if (!this.courseId) return;

    this.trainingService.getCourseModules(this.courseId).subscribe({
      next: (modules) => {
        this.modules = modules.sort((a, b) => a.order_index - b.order_index);
      },
      error: (err) => {
        console.error('Error loading modules:', err);
      }
    });
  }

  onSubmitCourse(): void {
    if (this.courseForm.invalid) {
      this.courseForm.markAllAsTouched();
      return;
    }

    this.loading = true;
    this.error = null;

    const formValue = this.courseForm.value;

    if (this.isEditMode && this.courseId) {
      this.trainingService.updateCourse(this.courseId, formValue).subscribe({
        next: () => {
          this.router.navigate(['/training/courses']);
        },
        error: (err) => {
          this.error = 'Failed to update course';
          this.loading = false;
          console.error('Error updating course:', err);
        }
      });
    } else {
      this.trainingService.createCourse(formValue).subscribe({
        next: (course) => {
          this.router.navigate(['/training/courses', course.id]);
        },
        error: (err) => {
          this.error = 'Failed to create course';
          this.loading = false;
          console.error('Error creating course:', err);
        }
      });
    }
  }

  openModuleForm(): void {
    this.showModuleForm = true;
    this.editingModuleId = undefined;
    this.moduleForm.reset();
  }

  editModule(module: CourseModule): void {
    this.showModuleForm = true;
    this.editingModuleId = module.id;
    this.moduleForm.patchValue({
      title: module.title,
      description: module.description,
      video_url: module.video_url,
      pdf_url: module.pdf_url,
      text_content: module.text_content,
      duration_minutes: module.duration_minutes
    });
  }

  closeModuleForm(): void {
    this.showModuleForm = false;
    this.editingModuleId = undefined;
    this.moduleForm.reset();
  }

  onSubmitModule(): void {
    if (this.moduleForm.invalid || !this.courseId) {
      this.moduleForm.markAllAsTouched();
      return;
    }

    const formValue = this.moduleForm.value;

    if (this.editingModuleId) {
      // Update existing module
      this.trainingService.updateCourseModule(this.editingModuleId, formValue).subscribe({
        next: () => {
          this.loadModules();
          this.closeModuleForm();
        },
        error: (err) => {
          alert('Failed to update module');
          console.error('Error updating module:', err);
        }
      });
    } else {
      // Create new module
      const moduleData: CourseModuleCreate = {
        ...formValue,
        course_id: this.courseId,
        order_index: this.modules.length
      };

      this.trainingService.createCourseModule(this.courseId, moduleData).subscribe({
        next: () => {
          this.loadModules();
          this.closeModuleForm();
        },
        error: (err) => {
          alert('Failed to create module');
          console.error('Error creating module:', err);
        }
      });
    }
  }

  deleteModule(module: CourseModule): void {
    if (confirm(`Are you sure you want to delete "${module.title}"?`)) {
      this.trainingService.deleteCourseModule(module.id).subscribe({
        next: () => {
          this.loadModules();
        },
        error: (err) => {
          alert('Failed to delete module');
          console.error('Error deleting module:', err);
        }
      });
    }
  }

  moveModuleUp(index: number): void {
    if (index === 0 || !this.courseId) return;

    const moduleOrders: {[key: number]: number} = {};
    moduleOrders[this.modules[index].id] = index - 1;
    moduleOrders[this.modules[index - 1].id] = index;

    this.trainingService.reorderCourseModules(this.courseId, moduleOrders).subscribe({
      next: () => {
        this.loadModules();
      },
      error: (err) => {
        console.error('Error reordering modules:', err);
      }
    });
  }

  moveModuleDown(index: number): void {
    if (index === this.modules.length - 1 || !this.courseId) return;

    const moduleOrders: {[key: number]: number} = {};
    moduleOrders[this.modules[index].id] = index + 1;
    moduleOrders[this.modules[index + 1].id] = index;

    this.trainingService.reorderCourseModules(this.courseId, moduleOrders).subscribe({
      next: () => {
        this.loadModules();
      },
      error: (err) => {
        console.error('Error reordering modules:', err);
      }
    });
  }

  cancel(): void {
    this.router.navigate(['/training/courses']);
  }

  isFieldInvalid(formGroup: FormGroup, fieldName: string): boolean {
    const field = formGroup.get(fieldName);
    return !!(field && field.invalid && field.touched);
  }

  getFieldError(formGroup: FormGroup, fieldName: string): string {
    const field = formGroup.get(fieldName);
    if (field?.hasError('required')) return `${fieldName} is required`;
    if (field?.hasError('maxlength')) return `${fieldName} is too long`;
    return '';
  }
}
