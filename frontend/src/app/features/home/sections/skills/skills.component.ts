import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SectionTitleComponent } from '@app/shared/section-title/section-title.component';
import { SkillService } from '@app/core/services/skill.service';
import { Skill } from '@app/models/skill.model';
import { TranslationService } from '@app/core/services/translation.service';

const CATEGORY_LABELS: Record<string, string> = {
  pentesting: 'Penetration Testing',
  networking: 'Networking',
  programming: 'Programming',
  web: 'Web',
  security: 'Security',
  other: 'Other',
};

@Component({
  selector: 'app-skills',
  standalone: true,
  imports: [CommonModule, SectionTitleComponent],
  templateUrl: './skills.component.html',
  styleUrl: './skills.component.css',
})
export class SkillsComponent implements OnInit {
  skills: Skill[] = [];
  grouped: Record<string, Skill[]> = {};

  constructor(
    private skillService: SkillService,
    private translationService: TranslationService
  ) {}

  ngOnInit(): void {
    this.skillService.getAll().subscribe({
      next: (list) => {
        if (list?.length) {
          // Translate skills from French to English
          const translated = this.translationService.translateArray(list, [
            'name',
            'description',
          ]);
          this.skills = translated;
          this.grouped = translated.reduce((acc, s) => {
            if (!acc[s.category]) acc[s.category] = [];
            acc[s.category].push(s);
            return acc;
          }, {} as Record<string, Skill[]>);
        } else {
          this.skills = [];
          this.grouped = {};
        }
      },
      error: () => {
        this.skills = [];
        this.grouped = {};
      },
    });
  }

  categoryLabel(cat: string): string {
    return CATEGORY_LABELS[cat] || cat;
  }

  objectKeys(obj: Record<string, Skill[]>): string[] {
    return Object.keys(obj);
  }
}
