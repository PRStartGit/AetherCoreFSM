import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

interface AllergenKeyword {
  id: number;
  keyword: string;
  allergen: string;
}

@Component({
  selector: 'app-allergen-keywords-admin',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    ReactiveFormsModule,
    MatSnackBarModule
  ],
  templateUrl: './allergen-keywords-admin.component.html',
  styleUrls: ['./allergen-keywords-admin.component.scss']
})
export class AllergenKeywordsAdminComponent implements OnInit {
  private apiUrl = '/api/v1/recipes/allergen-keywords';

  keywords: AllergenKeyword[] = [];
  groupedKeywords: Map<string, AllergenKeyword[]> = new Map();
  keywordForm: FormGroup;
  isEditing = false;
  editingId: number | null = null;
  expandedAllergens: Set<string> = new Set();

  // UK 14 Allergens
  allergens: string[] = [
    'Celery', 'Cereals containing gluten', 'Crustaceans', 'Eggs', 'Fish',
    'Lupin', 'Milk', 'Molluscs', 'Mustard', 'Nuts', 'Peanuts',
    'Sesame seeds', 'Soybeans', 'Sulphur dioxide and sulphites'
  ];

  constructor(
    private http: HttpClient,
    private fb: FormBuilder,
    private snackBar: MatSnackBar
  ) {
    this.keywordForm = this.fb.group({
      keyword: ['', [Validators.required, Validators.maxLength(100)]],
      allergen: ['', Validators.required]
    });
  }

  ngOnInit(): void {
    this.loadKeywords();
  }

  loadKeywords(): void {
    this.http.get<AllergenKeyword[]>(this.apiUrl).subscribe({
      next: (keywords) => {
        this.keywords = keywords;
        this.groupKeywordsByAllergen();
      },
      error: (error) => {
        this.snackBar.open('Failed to load allergen keywords', 'Close', { duration: 3000 });
        console.error('Error loading keywords:', error);
      }
    });
  }

  groupKeywordsByAllergen(): void {
    this.groupedKeywords = new Map();
    for (const keyword of this.keywords) {
      if (!this.groupedKeywords.has(keyword.allergen)) {
        this.groupedKeywords.set(keyword.allergen, []);
      }
      this.groupedKeywords.get(keyword.allergen)!.push(keyword);
    }
  }

  onSubmit(): void {
    if (this.keywordForm.invalid) {
      return;
    }

    const data = this.keywordForm.value;

    if (this.isEditing && this.editingId) {
      this.http.put<AllergenKeyword>(`${this.apiUrl}/${this.editingId}`, data).subscribe({
        next: () => {
          this.snackBar.open('Keyword updated successfully', 'Close', { duration: 3000 });
          this.loadKeywords();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open(error.error?.detail || 'Failed to update keyword', 'Close', { duration: 3000 });
        }
      });
    } else {
      this.http.post<AllergenKeyword>(this.apiUrl, data).subscribe({
        next: () => {
          this.snackBar.open('Keyword added successfully', 'Close', { duration: 3000 });
          this.loadKeywords();
          this.resetForm();
        },
        error: (error) => {
          this.snackBar.open(error.error?.detail || 'Failed to add keyword', 'Close', { duration: 3000 });
        }
      });
    }
  }

  editKeyword(keyword: AllergenKeyword): void {
    this.isEditing = true;
    this.editingId = keyword.id;
    this.keywordForm.patchValue({
      keyword: keyword.keyword,
      allergen: keyword.allergen
    });
  }

  deleteKeyword(keyword: AllergenKeyword): void {
    if (confirm(`Are you sure you want to delete the keyword "${keyword.keyword}"?`)) {
      this.http.delete(`${this.apiUrl}/${keyword.id}`).subscribe({
        next: () => {
          this.snackBar.open('Keyword deleted successfully', 'Close', { duration: 3000 });
          this.loadKeywords();
        },
        error: (error) => {
          this.snackBar.open('Failed to delete keyword', 'Close', { duration: 3000 });
        }
      });
    }
  }

  resetForm(): void {
    this.keywordForm.reset();
    this.isEditing = false;
    this.editingId = null;
  }

  cancelEdit(): void {
    this.resetForm();
  }

  getKeywordCount(allergen: string): number {
    return this.groupedKeywords.get(allergen)?.length || 0;
  }

  toggleAllergen(allergen: string): void {
    if (this.expandedAllergens.has(allergen)) {
      this.expandedAllergens.delete(allergen);
    } else {
      this.expandedAllergens.add(allergen);
    }
  }
}
