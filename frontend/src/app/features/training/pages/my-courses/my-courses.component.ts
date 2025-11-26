import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TrainingService } from '../../services/training.service';
import { CourseEnrollmentWithCourse, EnrollmentStatus } from '../../models/training.models';
import { formatDate } from '../../../../shared/utils/date-utils';

@Component({
  selector: 'app-my-courses',
  templateUrl: './my-courses.component.html',
  styleUrls: ['./my-courses.component.css']
})
export class MyCoursesComponent implements OnInit {
  enrollments: CourseEnrollmentWithCourse[] = [];
  loading = true;
  error: string | null = null;
  EnrollmentStatus = EnrollmentStatus;

  constructor(
    private trainingService: TrainingService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadMyCourses();
  }

  loadMyCourses(): void {
    this.loading = true;
    this.error = null;

    this.trainingService.getMyCourses().subscribe({
      next: (enrollments) => {
        this.enrollments = enrollments;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load courses';
        this.loading = false;
        console.error('Error loading courses:', err);
      }
    });
  }

  getFilteredEnrollments(status?: EnrollmentStatus): CourseEnrollmentWithCourse[] {
    if (!status) return this.enrollments;
    return this.enrollments.filter(e => e.status === status);
  }

  get notStartedCourses(): CourseEnrollmentWithCourse[] {
    return this.getFilteredEnrollments(EnrollmentStatus.NOT_STARTED);
  }

  get inProgressCourses(): CourseEnrollmentWithCourse[] {
    return this.getFilteredEnrollments(EnrollmentStatus.IN_PROGRESS);
  }

  get completedCourses(): CourseEnrollmentWithCourse[] {
    return this.getFilteredEnrollments(EnrollmentStatus.COMPLETED);
  }

  startCourse(enrollment: CourseEnrollmentWithCourse): void {
    // Mark as accessed (will automatically update status to in_progress)
    this.trainingService.markEnrollmentAccessed(enrollment.id).subscribe({
      next: () => {
        // Navigate to course player (Phase 4)
        this.router.navigate(['/training/player', enrollment.id]);
      },
      error: (err) => {
        console.error('Error starting course:', err);
      }
    });
  }

  continueCourse(enrollment: CourseEnrollmentWithCourse): void {
    // Mark as accessed
    this.trainingService.markEnrollmentAccessed(enrollment.id).subscribe({
      next: () => {
        // Navigate to course player (Phase 4)
        this.router.navigate(['/training/player', enrollment.id]);
      },
      error: (err) => {
        console.error('Error continuing course:', err);
      }
    });
  }

  reviewCourse(enrollment: CourseEnrollmentWithCourse): void {
    // Navigate to course player (Phase 4)
    this.router.navigate(['/training/player', enrollment.id]);
  }

  formatDate(dateString?: string): string {
    if (!dateString) return 'N/A';
    return formatDate(dateString);
  }

  getStatusColor(status: EnrollmentStatus): string {
    switch (status) {
      case EnrollmentStatus.NOT_STARTED:
        return 'bg-gray-100 text-gray-800';
      case EnrollmentStatus.IN_PROGRESS:
        return 'bg-blue-100 text-blue-800';
      case EnrollmentStatus.COMPLETED:
        return 'bg-green-100 text-green-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  getStatusLabel(status: EnrollmentStatus): string {
    switch (status) {
      case EnrollmentStatus.NOT_STARTED:
        return 'Not Started';
      case EnrollmentStatus.IN_PROGRESS:
        return 'In Progress';
      case EnrollmentStatus.COMPLETED:
        return 'Completed';
      default:
        return 'Unknown';
    }
  }
}
