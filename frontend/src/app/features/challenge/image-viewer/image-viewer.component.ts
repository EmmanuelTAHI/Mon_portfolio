import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { CtfService } from '../../../core/services/ctf.service';

@Component({
  selector: 'app-image-viewer',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './image-viewer.component.html',
  styleUrl: './image-viewer.component.css'
})
export class ImageViewerComponent implements OnInit {
  imageUrl = '';
  imageBlob: Blob | null = null;
  imageLoading = false;
  errorMessage = '';
  sessionId = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private ctfService: CtfService
  ) {}

  ngOnInit(): void {
    // Récupérer le session_id depuis les query params
    this.route.queryParams.subscribe(params => {
      this.sessionId = params['session_id'];
      if (this.sessionId) {
        this.loadImage();
      } else {
        this.errorMessage = 'Session ID missing';
      }
    });
  }

  loadImage(): void {
    this.imageLoading = true;
    this.errorMessage = '';
    console.log('[ImageViewer] loadImage start session_id=', this.sessionId);

    this.ctfService.downloadImage(this.sessionId).subscribe({
      next: (blob) => {
        console.log('[ImageViewer] next blob size=', blob?.size, 'type=', blob?.type);
        if (blob && blob.size > 0) {
          this.imageBlob = blob;
          this.imageUrl = window.URL.createObjectURL(blob);
          console.log('[ImageViewer] imageUrl set (blob URL) length=', this.imageUrl?.length);
          this.imageLoading = false;
        } else {
          console.warn('[ImageViewer] blob empty or invalid', blob);
          this.errorMessage = 'The received image is empty or invalid';
          this.imageLoading = false;
        }
      },
      error: (error) => {
        console.error('[ImageViewer] error', error);
        console.error('[ImageViewer] error.status=', error?.status, 'error.message=', error?.message, 'error.error=', error?.error);
        if (error.status === 403) {
          this.errorMessage = 'Access denied. Please log in first.';
        } else if (error.status === 404) {
          this.errorMessage = 'Image not found on server.';
        } else {
          this.errorMessage = 'Error loading image: ' + (error.error?.error || error.message || 'Unknown error');
        }
        this.imageLoading = false;
      }
    });
  }

  downloadImage(): void {
    if (!this.imageBlob) {
      this.errorMessage = 'Image not available for download';
      return;
    }

    try {
      // Créer une nouvelle URL d'objet pour le téléchargement (plus fiable)
      const downloadUrl = window.URL.createObjectURL(this.imageBlob);
      
      // Créer un élément <a> pour déclencher le téléchargement
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = 'Ma_maison.jpg';
      link.style.display = 'none';
      
      // Ajouter au DOM, cliquer, puis retirer
      document.body.appendChild(link);
      link.click();
      
      // Nettoyer après un court délai
      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
      }, 100);
    } catch (error) {
      console.error('Erreur lors du téléchargement:', error);
      this.errorMessage = 'Error downloading image';
    }
  }

  continue(): void {
    // Rediriger vers la page du challenge pour continuer
    this.router.navigate(['/_my_challenge'], { queryParams: { session_id: this.sessionId, from_image: '1' } });
  }

  /** Retour au challenge (même comportement que Continuer, raccourci visuel). */
  goBackToChallenge(): void {
    this.continue();
  }

  ngOnDestroy(): void {
    // Nettoyer l'URL de l'image
    if (this.imageUrl) {
      window.URL.revokeObjectURL(this.imageUrl);
    }
  }
}
