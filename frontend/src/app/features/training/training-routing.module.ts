import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TrainingLandingComponent } from './pages/training-landing/training-landing.component';
import { CourseListComponent } from './pages/course-list/course-list.component';
import { CourseFormComponent } from './pages/course-form/course-form.component';
import { MyCoursesComponent } from './pages/my-courses/my-courses.component';
import { CoursePlayerComponent } from './pages/course-player/course-player.component';
import { TrainingAccessGuard } from './guards/training-access.guard';

const routes: Routes = [
  {
    path: '',
    component: TrainingLandingComponent
  },
  {
    path: 'my-courses',
    component: MyCoursesComponent,
    canActivate: [TrainingAccessGuard]
  },
  {
    path: 'courses',
    component: CourseListComponent
  },
  {
    path: 'courses/:id',
    component: CourseFormComponent
  },
  {
    path: 'player/:id',
    component: CoursePlayerComponent,
    canActivate: [TrainingAccessGuard]
  }
  // Future routes will be added here in later phases:
  // { path: 'my-certificates', component: MyCertificatesComponent, canActivate: [TrainingAccessGuard] },
  // etc.
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TrainingRoutingModule { }
