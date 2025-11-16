import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';

import { DefectsRoutingModule } from './defects-routing.module';
import { DefectListComponent } from './defect-list/defect-list.component';
import { DefectFormComponent } from './defect-form/defect-form.component';


@NgModule({
  declarations: [
    DefectListComponent,
    DefectFormComponent
  ],
  imports: [
    CommonModule,
    ReactiveFormsModule,
    FormsModule,
    DefectsRoutingModule
  ]
})
export class DefectsModule { }
