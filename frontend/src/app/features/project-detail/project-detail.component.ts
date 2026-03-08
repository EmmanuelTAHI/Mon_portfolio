import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { ProjectService } from '@app/core/services/project.service';
import { Project } from '@app/models/project.model';
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-project-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './project-detail.component.html',
  styleUrl: './project-detail.component.css',
})
export class ProjectDetailComponent implements OnInit {
  project: Project | null = null;
  loading = true;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private projectService: ProjectService
  ) {}

  getProjectImageUrl(p: Project | null): string {
    if (!p?.image) return '';
    if (p.image.startsWith('http://') || p.image.startsWith('https://')) return p.image;
    const base = (environment as { backendMediaBase?: string }).backendMediaBase || '';
    if (base) return base + (p.image.startsWith('/') ? p.image : '/' + p.image);
    return p.image;
  }

  ngOnInit(): void {
    const slug = this.route.snapshot.paramMap.get('slug');
    if (!slug) {
      this.loading = false;
      this.error = 'Projet non trouvé.';
      return;
    }
    this.projectService.getBySlug(slug).subscribe({
      next: (p) => {
        this.project = p;
        this.loading = false;
      },
      error: () => {
        this.error = 'Projet non trouvé.';
        this.loading = false;
      },
    });
  }

  techList(tech: string): string[] {
    return tech ? tech.split(',').map((t) => t.trim()) : [];
  }
}
