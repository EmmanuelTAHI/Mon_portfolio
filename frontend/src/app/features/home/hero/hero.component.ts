import { Component, OnInit, OnDestroy, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { HeroTerminalComponent } from '@app/shared/hero-terminal/hero-terminal.component';
import { CtfService } from '@app/core/services/ctf.service';

export interface HeroStat {
  value: number;
  label: string;
}

@Component({
  selector: 'app-hero',
  standalone: true,
  imports: [CommonModule, HeroTerminalComponent],
  templateUrl: './hero.component.html',
})
export class HeroComponent implements OnInit, OnDestroy {
  name = 'Emmanuel TAHI';
  roleLabel = 'Cybersecurity Student | Pentester';
  terminalRole = 'Cybersecurity Student | Pentester';
  terminalDescription = 'I excel at crafting secure digital experiences and I am proficient in penetration testing, various programming languages and security technologies.';
  cvUrl = 'assets/pdf/CV Emmanuel TAHI.pdf';
  /** URL de la photo de profil (vide = affichage des initiales) */
  profileImageUrl = 'assets/images/Mon_image.png';
  
  showChallengeButton = false;
  challengeButtonPosition = { x: 0, y: 0 }; // x et y en pourcentage (0-100)

  get initials(): string {
    return this.name
      .split(/\s+/)
      .map((s) => s[0])
      .join('')
      .slice(0, 2)
      .toUpperCase();
  }

  stats: HeroStat[] = [
    { value: 1, label: 'Years of experience' },
    { value: 11, label: 'Projects completed' },
    { value: 12, label: 'Technologies mastered' },
    { value: 87, label: 'Code commits' },
  ];

  /** Valeurs affichées pour l'animation count-up (même longueur que stats) */
  displayedStats = signal<number[]>([]);
  private statsAnimated = false;
  private observer: IntersectionObserver | null = null;

  constructor(
    private router: Router,
    private ctfService: CtfService
  ) {}

  getDisplayStat(index: number): number {
    return this.displayedStats()[index] ?? 0;
  }

  ngOnInit(): void {
    this.displayedStats.set(this.stats.map((s) => 0));
    this.observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting && !this.statsAnimated) {
            this.statsAnimated = true;
            this.animateStats();
          }
        });
      },
      { threshold: 0.2, rootMargin: '0px' }
    );
    const statsEl = document.querySelector('.hero-stats');
    if (statsEl) this.observer.observe(statsEl);
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
  }

  private animateStats(): void {
    const duration = 1500;
    const steps = 40;
    const interval = duration / steps;
    this.stats.forEach((stat, i) => {
      let step = 0;
      const inc = stat.value / steps;
      const timer = setInterval(() => {
        step++;
        const current = this.displayedStats();
        const next = [...current];
        next[i] = Math.min(Math.round(inc * step), stat.value);
        this.displayedStats.set(next);
        if (step >= steps) clearInterval(timer);
      }, interval);
    });
  }

  scrollTo(id: string): void {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }

  onProfileHover(event: MouseEvent): void {
    // Positionner le bouton autour de la photo (en haut à droite, à 45°)
    // Utiliser des pourcentages pour un positionnement relatif au wrapper
    const angle = Math.PI / 4; // 45 degrés (en haut à droite)
    const distance = 65; // Distance du centre en pourcentage (juste à l'extérieur du cercle)
    
    // Calculer la position en pourcentage (50% = centre)
    this.challengeButtonPosition = {
      x: 50 + Math.cos(angle) * distance,
      y: 50 - Math.sin(angle) * distance
    };
    this.showChallengeButton = true;
  }

  onProfileLeave(): void {
    // Délai pour permettre le mouvement vers le bouton
    setTimeout(() => {
      const button = document.querySelector('.challenge-button-hover');
      if (!button || !(button as HTMLElement).matches(':hover')) {
        this.showChallengeButton = false;
      }
    }, 200);
  }

  onChallengeButtonEnter(): void {
    this.showChallengeButton = true;
  }

  onChallengeButtonLeave(): void {
    this.showChallengeButton = false;
  }

  navigateToChallenge(): void {
    // Vérifier si une session active existe
    const savedSession = localStorage.getItem('ctf_session_id');
    if (savedSession) {
      // Vérifier si la session est toujours active
      this.ctfService.checkSession(savedSession).subscribe({
        next: (response: { exists: boolean; is_completed?: boolean }) => {
          if (response.exists && !response.is_completed) {
            // Session active trouvée, rediriger vers le challenge (reprise)
            this.router.navigate(['/_my_challenge']);
          } else {
            // Session invalide ou complétée, nettoyer et rediriger
            localStorage.removeItem('ctf_session_id');
            localStorage.removeItem('ctf_elapsed_time');
            localStorage.removeItem('ctf_hacker_nickname');
            this.router.navigate(['/_my_challenge']);
          }
        },
        error: () => {
          // Erreur, nettoyer et rediriger quand même
          localStorage.removeItem('ctf_session_id');
          localStorage.removeItem('ctf_elapsed_time');
          localStorage.removeItem('ctf_hacker_nickname');
          this.router.navigate(['/_my_challenge']);
        }
      });
    } else {
      // Pas de session, rediriger normalement
      this.router.navigate(['/_my_challenge']);
    }
  }
}
