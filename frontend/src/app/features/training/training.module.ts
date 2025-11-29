import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { TrainingRoutingModule } from './training-routing.module';
import { TrainingLandingComponent } from './pages/training-landing/training-landing.component';
import { CourseListComponent } from './pages/course-list/course-list.component';
import { CourseFormComponent } from './pages/course-form/course-form.component';
import { MyCoursesComponent } from './pages/my-courses/my-courses.component';
import { CoursePlayerComponent } from './pages/course-player/course-player.component';
import { VideoPlayerComponent } from './components/video-player/video-player.component';
import { PdfViewerComponent } from './components/pdf-viewer/pdf-viewer.component';
import { MarkdownPipe } from './pipes/markdown.pipe';
import { TrainingService } from './services/training.service';
import { TrainingAccessGuard } from './guards/training-access.guard';

@NgModule({
  declarations: [
    TrainingLandingComponent,
    CourseListComponent,
    CourseFormComponent,
    MyCoursesComponent,
    CoursePlayerComponent,
    VideoPlayerComponent,
    PdfViewerComponent,
    MarkdownPipe
  ],
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    TrainingRoutingModule
  ],
  providers: [
    TrainingService,
    TrainingAccessGuard
  ]
})
export class TrainingModule { }
