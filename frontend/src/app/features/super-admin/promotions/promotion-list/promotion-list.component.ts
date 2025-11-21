import { Component, OnInit } from '@angular/core';
import { PromotionService, Promotion, PromotionCreate } from '../../../../core/services/promotion.service';

@Component({
  selector: 'app-promotion-list',
  templateUrl: './promotion-list.component.html',
  styleUrls: ['./promotion-list.component.scss']
})
export class PromotionListComponent implements OnInit {
  promotions: Promotion[] = [];
  loading = true;
  error: string | null = null;
  showForm = false;
  editingPromotion: Promotion | null = null;

  formData = {
    name: '',
    description: '',
    trial_days: 14,
    is_active: false
  };

  constructor(private promotionService: PromotionService) {}

  ngOnInit(): void {
    this.loadPromotions();
  }

  loadPromotions(): void {
    this.loading = true;
    this.promotionService.getAll().subscribe({
      next: (promos) => {
        this.promotions = promos;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load promotions';
        this.loading = false;
      }
    });
  }

  openCreateForm(): void {
    this.editingPromotion = null;
    this.formData = { name: '', description: '', trial_days: 14, is_active: false };
    this.showForm = true;
  }

  openEditForm(promo: Promotion): void {
    this.editingPromotion = promo;
    this.formData = {
      name: promo.name,
      description: promo.description || '',
      trial_days: promo.trial_days,
      is_active: promo.is_active
    };
    this.showForm = true;
  }

  closeForm(): void {
    this.showForm = false;
    this.editingPromotion = null;
  }

  submitForm(): void {
    if (this.editingPromotion) {
      this.promotionService.update(this.editingPromotion.id, this.formData).subscribe({
        next: () => {
          this.closeForm();
          this.loadPromotions();
        },
        error: () => alert('Failed to update promotion')
      });
    } else {
      this.promotionService.create(this.formData).subscribe({
        next: () => {
          this.closeForm();
          this.loadPromotions();
        },
        error: () => alert('Failed to create promotion')
      });
    }
  }

  activatePromotion(promo: Promotion): void {
    this.promotionService.activate(promo.id).subscribe({
      next: () => this.loadPromotions(),
      error: () => alert('Failed to activate promotion')
    });
  }

  deletePromotion(promo: Promotion): void {
    if (confirm(`Delete "${promo.name}"?`)) {
      this.promotionService.delete(promo.id).subscribe({
        next: () => this.loadPromotions(),
        error: (err) => alert(err.error?.detail || 'Failed to delete')
      });
    }
  }

  formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString('en-GB');
  }
}
