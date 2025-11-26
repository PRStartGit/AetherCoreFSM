import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TrainingService } from '../../services/training.service';
import { AuthService } from '../../../../core/auth/auth.service';
import { Course, CourseCategory } from '../../models/training.models';
import { UserRole } from '../../../../core/models';

@Component({
  selector: 'app-course-list',
  templateUrl: './course-list.component.html',
  styleUrls: ['./course-list.component.css']
})
export class CourseListComponent implements OnInit {
  courses: Course[] = [];
  categories: CourseCategory[] = [];
  loading = true;
  error: string | null = null;
  filterCategoryId: number | null = null;
  filterPublishedOnly = false;
  UserRole = UserRole;

  constructor(
    private trainingService: TrainingService,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadCategories();
    this.loadCourses();
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

  loadCourses(): void {
    this.loading = true;
    this.error = null;

    this.trainingService.getCourses(this.filterPublishedOnly, this.filterCategoryId || undefined).subscribe({
      next: (courses) => {
        this.courses = courses;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load courses';
        this.loading = false;
        console.error('Error loading courses:', err);
      }
    });
  }

  onFilterChange(): void {
    this.loadCourses();
  }

  navigateToCreate(): void {
    this.router.navigate(['/training/courses/new']);
  }

  navigateToEdit(course: Course): void {
    this.router.navigate(['/training/courses', course.id]);
  }

  deleteCourse(course: Course): void {
    if (confirm(`Are you sure you want to delete "${course.title}"? This will also delete all modules. This action cannot be undone.`)) {
      this.trainingService.deleteCourse(course.id).subscribe({
        next: () => {
          this.loadCourses();
        },
        error: (err) => {
          alert('Failed to delete course');
          console.error('Error deleting course:', err);
        }
      });
    }
  }

  togglePublishStatus(course: Course): void {
    const newStatus = !course.is_published;
    const action = newStatus ? 'publish' : 'unpublish';

    if (confirm(`Are you sure you want to ${action} "${course.title}"?`)) {
      this.trainingService.updateCourse(course.id, { is_published: newStatus }).subscribe({
        next: () => {
          course.is_published = newStatus;
        },
        error: (err) => {
          alert(`Failed to ${action} course`);
          console.error(`Error ${action}ing course:`, err);
        }
      });
    }
  }

  getCategoryName(categoryId?: number): string {
    if (!categoryId) return 'Uncategorized';
    const category = this.categories.find(c => c.id === categoryId);
    return category ? category.name : 'Unknown';
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  }

  get currentUserRole(): string {
    return this.authService.getUser()?.role || '';
  }

  get isSuperAdmin(): boolean {
    return this.currentUserRole === UserRole.SUPER_ADMIN;
  }
}
