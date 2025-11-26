import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  template: `
    <router-outlet></router-outlet>
    <app-cookie-consent></app-cookie-consent>
  `,
  styles: []
})
export class AppComponent {
  title = 'Zynthio';
}
