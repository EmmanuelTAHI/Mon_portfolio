import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { API_BASE } from '../../../core/constants/api';

/**
 * Affiche l'image du challenge CTF via une URL directe (pas de blob).
 * Un paramètre _t (cache-buster) évite le cache navigateur/CDN et garantit un 200.
 */
@Component({
  selector: 'app-image-viewer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './image-viewer.component.html',
  styleUrl: './image-viewer.component.css'
})
export class ImageViewerComponent implements OnInit, OnDestroy {
  /** URL directe de l'image avec session_id et cache-buster. */
  imageUrl = '';
  imageLoading = true;
  errorMessage = '';
  sessionId = '';
  /** Permet de réessayer avec une nouvelle URL (nouveau _t). */
  retryCount = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.sessionId = params['session_id'];
      if (this.sessionId) {
        this.buildAndLoadImage();
      } else {
        this.errorMessage = 'Session manquante.';
        this.imageLoading = false;
      }
    });
  }

  /** Construit l'URL d'image avec cache-buster pour forcer un 200 (éviter 304). */
  private buildImageUrl(): string {
    const base = API_BASE.replace(/\/$/, '');
    const t = Date.now() + (this.retryCount > 0 ? this.retryCount * 1000 : 0);
    return `${base}/ctf/download-image/?session_id=${encodeURIComponent(this.sessionId)}&_t=${t}`;
  }

  buildAndLoadImage(): void {
    this.errorMessage = '';
    this.imageLoading = true;
    this.imageUrl = this.buildImageUrl();
  }

  onImageLoad(): void {
    this.imageLoading = false;
    this.errorMessage = '';
  }

  onImageError(): void {
    this.imageLoading = false;
    this.imageUrl = '';
    this.errorMessage = 'Impossible de charger l’image. Vérifiez votre connexion ou réessayez.';
  }

  retry(): void {
    this.retryCount++;
    this.buildAndLoadImage();
  }

  /** Lien de téléchargement : même URL que l’affichage (fraîche). */
  get downloadUrl(): string {
    return this.imageUrl || (this.sessionId ? this.buildImageUrl() : '');
  }

  continue(): void {
    this.router.navigate(['/_my_challenge'], { queryParams: { session_id: this.sessionId, from_image: '1' } });
  }

  goBackToChallenge(): void {
    this.continue();
  }

  ngOnDestroy(): void {}
}
