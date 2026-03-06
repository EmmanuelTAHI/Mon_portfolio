import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SectionTitleComponent } from '@app/shared/section-title/section-title.component';
import { CertificationService } from '@app/core/services/certification.service';
import { Certification } from '@app/models/certification.model';
import { TranslationService } from '@app/core/services/translation.service';

@Component({
  selector: 'app-certifications',
  standalone: true,
  imports: [CommonModule, SectionTitleComponent],
  templateUrl: './certifications.component.html',
  styleUrl: './certifications.component.css',
})
export class CertificationsComponent implements OnInit {
  certs: Certification[] = [];

  constructor(
    private certificationService: CertificationService,
    private translationService: TranslationService
  ) {}

  ngOnInit(): void {
    this.certificationService.getAll().subscribe({
      next: (list) => {
        if (list?.length) {
          // Translate certifications from French to English
          this.certs = this.translationService.translateArray(list, [
            'title',
            'issuer',
            'description',
          ]);
        } else {
          this.certs = [];
        }
      },
      error: () => {
        this.certs = [];
      },
    });
  }
}
