import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { TrainingService } from '../../training/services/training.service';
import { JobRole } from '../../training/models/training.models';

@Component({
  selector: 'app-job-roles-list',
  templateUrl: './job-roles-list.component.html',
  styleUrls: ['./job-roles-list.component.scss']
})
export class JobRolesListComponent implements OnInit {
  jobRoles: JobRole[] = [];
  loading = true;
  error: string | null = null;
  showDeleteConfirm = false;
  roleToDelete: JobRole | null = null;

  constructor(
    private trainingService: TrainingService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.loadJobRoles();
  }

  loadJobRoles(): void {
    this.loading = true;
    this.error = null;

    this.trainingService.getAllJobRoles().subscribe({
      next: (roles) => {
        this.jobRoles = roles;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load job roles';
        this.loading = false;
        console.error('Error loading job roles:', err);
      }
    });
  }

  createJobRole(): void {
    this.router.navigate(['/super-admin/job-roles', 'new']);
  }

  editJobRole(id: number): void {
    this.router.navigate(['/super-admin/job-roles', id]);
  }

  confirmDelete(role: JobRole): void {
    this.roleToDelete = role;
    this.showDeleteConfirm = true;
  }

  cancelDelete(): void {
    this.roleToDelete = null;
    this.showDeleteConfirm = false;
  }

  deleteJobRole(): void {
    if (!this.roleToDelete) return;

    this.trainingService.deleteJobRole(this.roleToDelete.id).subscribe({
      next: () => {
        this.showDeleteConfirm = false;
        this.roleToDelete = null;
        this.loadJobRoles();
      },
      error: (err) => {
        this.error = 'Failed to delete job role';
        console.error('Error deleting job role:', err);
        this.showDeleteConfirm = false;
      }
    });
  }
}
