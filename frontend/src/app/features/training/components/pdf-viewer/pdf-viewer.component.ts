import { Component, Input, OnInit } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

@Component({
  selector: 'app-pdf-viewer',
  templateUrl: './pdf-viewer.component.html',
  styleUrls: ['./pdf-viewer.component.css']
})
export class PdfViewerComponent implements OnInit {
  @Input() pdfUrl: string = '';

  safePdfUrl: SafeResourceUrl | null = null;
  loading = true;
  error = false;

  constructor(private sanitizer: DomSanitizer) {}

  ngOnInit(): void {
    if (this.pdfUrl) {
      this.safePdfUrl = this.sanitizer.bypassSecurityTrustResourceUrl(this.pdfUrl);
    } else {
      this.error = true;
      this.loading = false;
    }
  }

  onLoad(): void {
    this.loading = false;
  }

  onError(): void {
    this.loading = false;
    this.error = true;
  }
}
