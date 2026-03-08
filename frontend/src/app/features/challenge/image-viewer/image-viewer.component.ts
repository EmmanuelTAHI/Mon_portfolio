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
  imageLoading = true;
  errorMessage = '';
  sessionId = '';
  private imageContentType = '';
  private imageBase64 = '';
  private imageFilename = 'Ma_maison.jpg';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private ctfService: CtfService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.sessionId = params['session_id'];
      if (this.sessionId) {
        this.loadImage();
      } else {
        this.errorMessage = 'Session manquante.';
        this.imageLoading = false;
      }
    });
  }

  loadImage(): void {
    this.errorMessage = '';
    this.imageLoading = true;

    this.ctfService.downloadImage(this.sessionId).subscribe({
      next: (data) => {
        if (data.image_data && data.content_type) {
          this.imageBase64 = data.image_data;
          this.imageContentType = data.content_type;
          this.imageFilename = data.filename || 'Ma_maison.jpg';
          this.imageUrl = `data:${data.content_type};base64,${data.image_data}`;
          this.imageLoading = false;
        } else {
          this.errorMessage = 'Réponse invalide du serveur.';
          this.imageLoading = false;
        }
      },
      error: (err) => {
        this.imageLoading = false;
        const serverError = err?.error?.error;
        if (err.status === 403) {
          this.errorMessage = 'Accès refusé. Connectez-vous d\'abord.';
        } else if (err.status === 404) {
          this.errorMessage = 'Image introuvable sur le serveur.';
        } else {
          this.errorMessage = serverError || 'Erreur lors du chargement de l\'image.';
        }
      }
    });
  }

  retry(): void {
    this.loadImage();
  }

  downloadImage(): void {
    if (!this.imageBase64 || !this.imageContentType) return;

    const byteChars = atob(this.imageBase64);
    const byteArray = new Uint8Array(byteChars.length);
    for (let i = 0; i < byteChars.length; i++) {
      byteArray[i] = byteChars.charCodeAt(i);
    }
    const blob = new Blob([byteArray], { type: this.imageContentType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = this.imageFilename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 100);
  }

  continue(): void {
    this.router.navigate(['/_my_challenge'], {
      queryParams: { session_id: this.sessionId, from_image: '1' }
    });
  }

  goBackToChallenge(): void {
    this.continue();
  }
}
