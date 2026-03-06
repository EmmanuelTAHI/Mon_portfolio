import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SectionTitleComponent } from '@app/shared/section-title/section-title.component';
import { ExperienceService } from '@app/core/services/experience.service';
import { Experience } from '@app/models/experience.model';
import { TranslationService } from '@app/core/services/translation.service';

@Component({
  selector: 'app-experience',
  standalone: true,
  imports: [CommonModule, SectionTitleComponent],
  templateUrl: './experience.component.html',
  styleUrl: './experience.component.css',
})
export class ExperienceComponent implements OnInit {
  items: Experience[] = [];

  constructor(
    private experienceService: ExperienceService,
    private translationService: TranslationService
  ) {}

  ngOnInit(): void {
    this.experienceService.getAll().subscribe({
      next: (list) => {
        if (list?.length) {
          // Translate experience items from French to English
          this.items = this.translationService.translateArray(list, [
            'title',
            'organization',
            'description',
            'location',
          ]);
        } else {
          this.items = [];
        }
      },
      error: () => {
        this.items = [];
      },
    });
  }

  formatDate(d: string | null): string {
    if (!d) return 'Present';
    return new Date(d).toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
  }
}
