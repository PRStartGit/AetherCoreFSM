import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm: FormGroup;
  loading = false;
  hidePassword = true;
  hideConfirmPassword = true;

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {
    this.registerForm = this.fb.group({
      // Organization details
      company_name: ['', Validators.required],
      org_id: ['', [Validators.required, Validators.pattern(/^[a-zA-Z0-9-_]+$/)]],

      // Contact details
      contact_person: ['', Validators.required],
      contact_email: ['', [Validators.required, Validators.email]],
      contact_phone: [''],
      address: [''],

      // Admin user details
      admin_first_name: ['', Validators.required],
      admin_last_name: ['', Validators.required],
      admin_email: ['', [Validators.required, Validators.email]],
      admin_password: ['', [Validators.required, Validators.minLength(8)]],
      confirm_password: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    // If already logged in, redirect to appropriate dashboard
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
  }

  onSubmit(): void {
    if (this.registerForm.invalid) {
      this.markAllFieldsAsTouched();
      return;
    }

    const { confirm_password, ...formData } = this.registerForm.value;

    // Check if passwords match
    if (formData.admin_password !== confirm_password) {
      this.snackBar.open('Passwords do not match', 'Close', { duration: 3000 });
      return;
    }

    this.loading = true;

    this.authService.register(formData).subscribe({
      next: (response) => {
        this.loading = false;
        this.snackBar.open(
          'Registration successful! Please check your email for login credentials.',
          'Close',
          { duration: 5000 }
        );
        // Redirect to login page after successful registration
        setTimeout(() => {
          this.router.navigate(['/login']);
        }, 2000);
      },
      error: (error) => {
        this.loading = false;
        const message = error.error?.detail || 'Registration failed. Please try again.';
        this.snackBar.open(message, 'Close', { duration: 5000 });
      }
    });
  }

  private markAllFieldsAsTouched(): void {
    Object.keys(this.registerForm.controls).forEach(key => {
      this.registerForm.get(key)?.markAsTouched();
    });
  }

  goToLogin(): void {
    this.router.navigate(['/login']);
  }
}
