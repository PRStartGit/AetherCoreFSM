import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Subject, takeUntil, interval } from 'rxjs';
import { CourseService } from '../../services/course.service';
import { EnrollmentService } from '../../services/enrollment.service';
import { ModuleProgressService } from '../../services/module-progress.service';
import { Course, CourseModule, CourseEnrollment, ModuleProgress } from '../../models/training.models';

@Component({
  selector: 'app-course-player',
  templateUrl: './course-player.component.html',
  styleUrls: ['./course-player.component.css']
})
export class CoursePlayerComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();
  private progressSaveInterval$ = new Subject<void>();
  private startTime: number = 0;

  enrollmentId!: number;
  enrollment: CourseEnrollment | null = null;
  course: Course | null = null;
  modules: CourseModule[] = [];
  currentModule: CourseModule | null = null;
  currentModuleIndex: number = 0;
  moduleProgress: Map<number, ModuleProgress> = new Map();

  loading = true;
  error: string | null = null;

  // Video player state
  videoElement: HTMLVideoElement | null = null;
  videoCurrentTime: number = 0;
  videoDuration: number = 0;
  videoPlaying: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private courseService: CourseService,
    private enrollmentService: EnrollmentService,
    private moduleProgressService: ModuleProgressService
  ) {}

  ngOnInit(): void {
    this.enrollmentId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadEnrollmentData();
    this.setupProgressAutoSave();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
    this.progressSaveInterval$.next();
    this.progressSaveInterval$.complete();
    this.saveCurrentProgress();
  }

  loadEnrollmentData(): void {
    this.loading = true;
    this.error = null;

    this.enrollmentService.getEnrollment(this.enrollmentId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (enrollment) => {
          this.enrollment = enrollment;
          this.loadCourse(enrollment.course_id);
          this.loadModuleProgress();
        },
        error: (error) => {
          console.error('Error loading enrollment:', error);
          this.error = 'Failed to load course enrollment';
          this.loading = false;
        }
      });
  }

  loadCourse(courseId: number): void {
    this.courseService.getCourse(courseId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (course: Course) => {
          this.course = course;
          this.modules = course.modules?.sort((a: CourseModule, b: CourseModule) => a.order_index - b.order_index) || [];

          // Load first incomplete module or first module
          const firstIncomplete = this.modules.findIndex((m: CourseModule) => !this.isModuleCompleted(m.id));
          this.currentModuleIndex = firstIncomplete >= 0 ? firstIncomplete : 0;
          this.currentModule = this.modules[this.currentModuleIndex] || null;

          this.loading = false;
          this.startTime = Date.now();
        },
        error: (error: any) => {
          console.error('Error loading course:', error);
          this.error = 'Failed to load course details';
          this.loading = false;
        }
      });
  }

  loadModuleProgress(): void {
    this.moduleProgressService.getEnrollmentProgress(this.enrollmentId)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: (progressList) => {
          this.moduleProgress.clear();
          progressList.forEach(p => this.moduleProgress.set(p.module_id, p));
        },
        error: (error) => {
          console.error('Error loading module progress:', error);
        }
      });
  }

  setupProgressAutoSave(): void {
    // Auto-save progress every 30 seconds
    interval(30000)
      .pipe(takeUntil(this.progressSaveInterval$))
      .subscribe(() => {
        this.saveCurrentProgress();
      });
  }

  saveCurrentProgress(): void {
    if (!this.currentModule) return;

    const currentProgress = this.moduleProgress.get(this.currentModule.id);
    const lastPosition = this.videoElement?.currentTime || currentProgress?.last_position_seconds || 0;

    this.moduleProgressService.updateProgress(
      this.enrollmentId,
      this.currentModule.id,
      {
        last_position_seconds: Math.floor(lastPosition),
        time_spent_seconds: (currentProgress?.time_spent_seconds || 0) + Math.floor((Date.now() - this.startTime) / 1000)
      }
    ).subscribe({
      next: (progress) => {
        this.moduleProgress.set(this.currentModule!.id, progress);
        this.startTime = Date.now(); // Reset timer
      },
      error: (error) => {
        console.error('Error saving progress:', error);
      }
    });
  }

  onVideoReady(videoElement: HTMLVideoElement): void {
    this.videoElement = videoElement;
    this.videoDuration = videoElement.duration;

    // Restore last position if available
    const progress = this.moduleProgress.get(this.currentModule!.id);
    if (progress && progress.last_position_seconds > 0) {
      videoElement.currentTime = progress.last_position_seconds;
    }
  }

  onVideoTimeUpdate(currentTime: number): void {
    this.videoCurrentTime = currentTime;
  }

  onVideoEnded(): void {
    this.completeCurrentModule();
  }

  completeCurrentModule(): void {
    if (!this.currentModule) return;

    const timeSpent = Math.floor((Date.now() - this.startTime) / 1000);

    this.moduleProgressService.completeModule(
      this.enrollmentId,
      this.currentModule.id,
      timeSpent
    ).subscribe({
      next: (progress) => {
        this.moduleProgress.set(this.currentModule!.id, progress);
        this.startTime = Date.now();

        // Reload enrollment to get updated progress percentage
        this.loadEnrollmentData();

        // Auto-advance to next module if available
        if (this.hasNextModule()) {
          setTimeout(() => this.nextModule(), 1500);
        }
      },
      error: (error) => {
        console.error('Error completing module:', error);
      }
    });
  }

  markAsComplete(): void {
    this.completeCurrentModule();
  }

  previousModule(): void {
    if (this.hasPreviousModule()) {
      this.saveCurrentProgress();
      this.currentModuleIndex--;
      this.currentModule = this.modules[this.currentModuleIndex];
      this.startTime = Date.now();
      this.videoElement = null;
    }
  }

  nextModule(): void {
    if (this.hasNextModule()) {
      this.saveCurrentProgress();
      this.currentModuleIndex++;
      this.currentModule = this.modules[this.currentModuleIndex];
      this.startTime = Date.now();
      this.videoElement = null;
    }
  }

  selectModule(index: number): void {
    if (index >= 0 && index < this.modules.length) {
      this.saveCurrentProgress();
      this.currentModuleIndex = index;
      this.currentModule = this.modules[index];
      this.startTime = Date.now();
      this.videoElement = null;
    }
  }

  hasPreviousModule(): boolean {
    return this.currentModuleIndex > 0;
  }

  hasNextModule(): boolean {
    return this.currentModuleIndex < this.modules.length - 1;
  }

  isModuleCompleted(moduleId: number): boolean {
    return this.moduleProgress.get(moduleId)?.is_completed || false;
  }

  getModuleProgress(moduleId: number): ModuleProgress | undefined {
    return this.moduleProgress.get(moduleId);
  }

  exitCourse(): void {
    this.saveCurrentProgress();
    this.router.navigate(['/training/my-courses']);
  }

  get completedModulesCount(): number {
    return Array.from(this.moduleProgress.values()).filter(p => p.is_completed).length;
  }

  get totalModulesCount(): number {
    return this.modules.length;
  }

  get courseProgressPercentage(): number {
    return this.enrollment?.progress_percentage || 0;
  }
}
