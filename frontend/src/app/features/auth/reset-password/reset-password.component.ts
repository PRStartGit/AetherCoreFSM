import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from '../../../core/auth/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-reset-password',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './reset-password.component.html',
  styleUrl: './reset-password.component.scss'
})
export class ResetPasswordComponent implements OnInit {
  resetPasswordForm: FormGroup;
  loading = false;
  hidePassword = true;
  hideConfirmPassword = true;
  token: string | null = null;
  tokenInvalid = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    public router: Router,
    private route: ActivatedRoute,
    private snackBar: MatSnackBar
  ) {
    this.resetPasswordForm = this.fb.group({
      new_password: ['', [Validators.required, Validators.minLength(6)]],
      confirm_password: ['', Validators.required]
    }, { validators: this.passwordMatchValidator });
  }

  ngOnInit(): void {
    // Get token from query params
    this.route.queryParams.subscribe(params => {
      this.token = params['token'];
      if (!this.token) {
        this.tokenInvalid = true;
        this.snackBar.open('Invalid reset link', 'Close', { duration: 5000 });
      }
    });
  }

  passwordMatchValidator(g: FormGroup) {
    return g.get('new_password')?.value === g.get('confirm_password')?.value
      ? null : { 'mismatch': true };
  }

  onSubmit(): void {
    if (this.resetPasswordForm.invalid || !this.token) {
      return;
    }

    this.loading = true;
    const data = {
      token: this.token,
      new_password: this.resetPasswordForm.value.new_password
    };

    this.authService.resetPassword(data).subscribe({
      next: (response) => {
        this.loading = false;
        this.snackBar.open('Password reset successful! You can now login.', 'Close', { duration: 5000 });
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (error) => {
        this.loading = false;
        const message = error.error?.detail || 'Failed to reset password. The link may be invalid or expired.';
        this.snackBar.open(message, 'Close', { duration: 5000 });
        this.tokenInvalid = true;
      }
    });
  }

  backToLogin(): void {
    this.router.navigate(['/login']);
  }
}
