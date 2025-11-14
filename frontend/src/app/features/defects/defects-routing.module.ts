import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DefectListComponent } from './defect-list/defect-list.component';
import { DefectFormComponent } from './defect-form/defect-form.component';

const routes: Routes = [
  { path: '', component: DefectListComponent },
  { path: 'new', component: DefectFormComponent },
  { path: ':id/edit', component: DefectFormComponent }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class DefectsRoutingModule { }
