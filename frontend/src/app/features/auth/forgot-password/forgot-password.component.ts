import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-forgot-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './forgot-password.component.html',
  styleUrl: './forgot-password.component.scss'
})
export class ForgotPasswordComponent implements OnInit {
  forgotPasswordForm: FormGroup;
  loading = false;
  submitted = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.forgotPasswordForm = this.fb.group({
      organization_id: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]]
    });
  }

  ngOnInit(): void {}

  onSubmit(): void {
    if (this.forgotPasswordForm.invalid) {
      return;
    }

    this.loading = true;
    const data = this.forgotPasswordForm.value;

    this.authService.requestPasswordReset(data).subscribe({
      next: (response) => {
        this.loading = false;
        this.submitted = true;
        this.snackBar.open(
          'If an account exists with that email, a password reset link has been sent.',
          'Close',
          { duration: 8000 }
        );
      },
      error: (error) => {
        this.loading = false;
        this.submitted = true;
        // Always show success message for security
        this.snackBar.open(
          'If an account exists with that email, a password reset link has been sent.',
          'Close',
          { duration: 8000 }
        );
      }
    });
  }

  backToLogin(): void {
    this.router.navigate(['/login']);
  }
}
