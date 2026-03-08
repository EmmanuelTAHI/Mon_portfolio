import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { SectionTitleComponent } from '@app/shared/section-title/section-title.component';
import { ProjectService, PaginatedProjectsResponse } from '@app/core/services/project.service';
import { Project } from '@app/models/project.model';
import { TranslationService } from '@app/core/services/translation.service';
import { environment } from '../../../../../environments/environment';

@Component({
  selector: 'app-projects',
  standalone: true,
  imports: [CommonModule, RouterLink, SectionTitleComponent],
  templateUrl: './projects.component.html',
  styleUrl: './projects.component.css',
})
export class ProjectsComponent implements OnInit {
  projects: Project[] = [];
  currentPage = 1;
  totalPages = 1;
  totalCount = 0;
  loading = false;
  slideDirection: 'left' | 'right' = 'right';
  /** IDs des projets dont l'image n'a pas pu être chargée */
  imageFailedIds = new Set<number>();

  constructor(
    private projectService: ProjectService,
    private translationService: TranslationService
  ) {}

  /** URL d'affichage pour l'image d'un projet. Gère les URLs absolues et relatives (fallback avec backendMediaBase). */
  getProjectImageUrl(p: Project): string {
    if (!p?.image) return '';
    if (p.image.startsWith('http://') || p.image.startsWith('https://')) return p.image;
    const base = (environment as { backendMediaBase?: string }).backendMediaBase || '';
    if (base) return base + (p.image.startsWith('/') ? p.image : '/' + p.image);
    return p.image;
  }

  ngOnInit(): void {
    this.loadProjects(1);
  }

  loadProjects(page: number): void {
    this.loading = true;
    this.projectService.getPaginated(page, 3).subscribe({
      next: (response: PaginatedProjectsResponse) => {
        // Translate projects from French to English
        this.projects = this.translationService.translateArray(response.results, [
          'title',
          'short_description',
          'description',
          'technologies',
        ]);
        this.currentPage = page;
        this.totalCount = response.count;
        this.totalPages = Math.ceil(response.count / 3);
        this.loading = false;
      },
      error: () => {
        this.projects = [];
        this.loading = false;
      },
    });
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages && !this.loading) {
      this.slideDirection = 'right';
      this.loadProjects(this.currentPage + 1);
    }
  }

  previousPage(): void {
    if (this.currentPage > 1 && !this.loading) {
      this.slideDirection = 'left';
      this.loadProjects(this.currentPage - 1);
    }
  }

  techList(tech: string): string[] {
    return tech ? tech.split(',').map((t) => t.trim()) : [];
  }

  onImageError(projectId: number): void {
    this.imageFailedIds.add(projectId);
  }

  showProjectImage(p: Project): boolean {
    return !!(p.image && !this.imageFailedIds.has(p.id));
  }
}
