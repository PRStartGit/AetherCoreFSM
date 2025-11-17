import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UserRole } from '../../models';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  loginForm: FormGroup;
  passwordChangeForm: FormGroup;
  loading = false;
  hidePassword = true;
  hideNewPassword = true;
  hideConfirmPassword = true;
  showPasswordChange = false;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.loginForm = this.fb.group({
      organization_id: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', Validators.required]
    });

    this.passwordChangeForm = this.fb.group({
      new_password: ['', [Validators.required, Validators.minLength(8)]],
      confirm_password: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    // If already logged in, redirect to appropriate dashboard
    if (this.authService.isAuthenticated()) {
      this.redirectToDashboard();
    }
  }

  onSubmit(): void {
    if (this.loginForm.invalid) {
      return;
    }

    this.loading = true;
    const credentials = this.loginForm.value;

    this.authService.login(credentials).subscribe({
      next: (response) => {
        if (response.must_change_password) {
          this.loading = false;
          this.showPasswordChange = true;
          this.snackBar.open('You must change your password before continuing', 'Close', { duration: 5000 });
        } else {
          this.snackBar.open('Login successful!', 'Close', { duration: 3000 });
          this.redirectToDashboard();
        }
      },
      error: (error) => {
        this.loading = false;
        const message = error.error?.detail || 'Login failed. Please check your credentials.';
        this.snackBar.open(message, 'Close', { duration: 5000 });
      }
    });
  }

  onPasswordChangeSubmit(): void {
    if (this.passwordChangeForm.invalid) {
      return;
    }

    const { new_password, confirm_password } = this.passwordChangeForm.value;

    if (new_password !== confirm_password) {
      this.snackBar.open('Passwords do not match', 'Close', { duration: 3000 });
      return;
    }

    const oldPassword = this.loginForm.value.password;

    this.loading = true;
    this.authService.changePassword({
      old_password: oldPassword,
      new_password: new_password
    }).subscribe({
      next: () => {
        this.loading = false;
        this.snackBar.open('Password changed successfully! Redirecting...', 'Close', { duration: 3000 });
        this.showPasswordChange = false;
        this.redirectToDashboard();
      },
      error: (error) => {
        this.loading = false;
        const message = error.error?.detail || 'Failed to change password';
        this.snackBar.open(message, 'Close', { duration: 5000 });
      }
    });
  }

  private redirectToDashboard(): void {
    const user = this.authService.getUser();
    if (!user) {
      return;
    }

    switch (user.role) {
      case UserRole.SUPER_ADMIN:
        this.router.navigate(['/super-admin']);
        break;
      case UserRole.ORG_ADMIN:
        this.router.navigate(['/org-admin']);
        break;
      case UserRole.SITE_USER:
        this.router.navigate(['/site-user']);
        break;
      default:
        this.snackBar.open('Unknown user role', 'Close', { duration: 3000 });
    }
  }
}
