import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { CtfService } from '../../core/services/ctf.service';

type ChallengeStep = 'nickname' | 'instructions' | 'first_flag' | 'login' | 'final_flag' | 'success' | 'leaderboard';

/** Instructions text (same as backend), used when not yet loaded from API (e.g. after Back from login or on restore). */
const DEFAULT_INSTRUCTIONS = 'Emmanuel connected all the Ubiquiti cameras in his house to his website so he could access them remotely, but something is not working. Help him figure out the problem.';

@Component({
  selector: 'app-challenge',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './challenge.component.html',
  styleUrl: './challenge.component.css'
})
export class ChallengeComponent implements OnInit, OnDestroy {
  currentStep: ChallengeStep = 'nickname';
  /** Texte des instructions affiché quand non chargé depuis l'API (retour depuis login ou restauration). */
  readonly defaultInstructions = DEFAULT_INSTRUCTIONS;
  hackerNickname = '';
  sessionId = '';
  instructions = '';
  loginUsername = '';
  loginPassword = '';
  finalFlag = '';
  errorMessage = '';
  successMessage = '';
  completionTime = 0;
  userRank = 0;
  animations: string[] = [];
  currentAnimationIndex = 0;
  showAnimation = false;
  
  leaderboard: any[] = [];
  userEntry: any = null;

  // Timer
  elapsedTime = 0;
  timerInterval: any = null;

  constructor(
    private ctfService: CtfService,
    private router: Router,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    // Charger le leaderboard public dès le chargement de la page
    this.loadLeaderboard();
    
    // Retour depuis la page image : traiter en premier de façon synchrone pour ne pas être écrasé par restoreSession
    const params = this.route.snapshot.queryParams;
    const querySessionId = params['session_id'];
    if (querySessionId && params['from_image']) {
      this.sessionId = querySessionId;
      this.currentStep = 'final_flag';
      this.loadSessionState();
      return;
    }
    
    // Vérifier automatiquement si une session existe et la restaurer
    const savedSession = localStorage.getItem('ctf_session_id');
    if (savedSession) {
      this.restoreSession(savedSession);
    } else {
      // Pas de session, commencer à l'étape nickname
      this.hackerNickname = '';
      this.currentStep = 'nickname';
    }
  }

  restoreSession(sessionId: string): void {
    this.ctfService.checkSession(sessionId).subscribe({
      next: (response) => {
        if (response.exists && !response.is_completed) {
          // Session active trouvée, restaurer l'état
          this.sessionId = response.session_id!;
          this.hackerNickname = response.hacker_nickname || '';
          this.elapsedTime = response.elapsed_time || 0;
          
          // Restaurer l'étape appropriée : 0 ou 1 → Instructions (pas directement Login), 2 → final_flag
          if (response.current_step === undefined || response.current_step === 0 || response.current_step === 1) {
            this.currentStep = 'instructions';
            if (!this.instructions) {
              this.instructions = DEFAULT_INSTRUCTIONS;
            }
          } else if (response.current_step === 2) {
            this.currentStep = 'final_flag';
          } else if (response.is_completed) {
            this.currentStep = 'leaderboard';
          } else {
            this.currentStep = 'instructions';
            if (!this.instructions) {
              this.instructions = DEFAULT_INSTRUCTIONS;
            }
          }
          
          // Sauvegarder dans localStorage
          localStorage.setItem('ctf_session_id', this.sessionId);
          localStorage.setItem('ctf_hacker_nickname', this.hackerNickname);
          
          // Démarrer le timer
          this.startTimer();
        } else {
          // Session invalide ou complétée, nettoyer et recommencer
          this.clearSession();
          this.hackerNickname = '';
          this.currentStep = 'nickname';
        }
      },
      error: (error) => {
        // Erreur lors de la vérification, nettoyer et recommencer
        console.error('Erreur lors de la vérification de la session:', error);
        this.clearSession();
        this.hackerNickname = '';
        this.currentStep = 'nickname';
      }
    });
  }

  clearSession(): void {
    localStorage.removeItem('ctf_session_id');
    localStorage.removeItem('ctf_elapsed_time');
    localStorage.removeItem('ctf_hacker_nickname');
    this.sessionId = '';
    this.elapsedTime = 0;
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
  }

  ngOnDestroy(): void {
    // Arrêter le timer
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
    }
  }

  loadSessionState(): void {
    if (this.sessionId && this.currentStep !== 'nickname') {
      // Restaurer l'état depuis localStorage si disponible
      // MAIS SEULEMENT si on n'est pas à l'étape nickname
      const savedTime = localStorage.getItem('ctf_elapsed_time');
      const savedNickname = localStorage.getItem('ctf_hacker_nickname');
      
      if (savedTime) {
        this.elapsedTime = parseFloat(savedTime);
      }
      if (savedNickname) {
        this.hackerNickname = savedNickname;
      }
      
      // Mettre à jour depuis le serveur et démarrer le timer
      this.updateTimer();
      this.startTimer();
    } else if (this.sessionId && this.currentStep === 'nickname') {
      // Si on a une session mais qu'on est à l'étape nickname, nettoyer
      this.hackerNickname = '';
      localStorage.removeItem('ctf_session_id');
      localStorage.removeItem('ctf_elapsed_time');
      localStorage.removeItem('ctf_hacker_nickname');
      this.sessionId = '';
      this.elapsedTime = 0;
    }
  }

  startChallenge(): void {
    const nickname = this.hackerNickname?.trim() || '';
    if (!nickname) {
      this.errorMessage = 'Please enter a username';
      return;
    }

    this.errorMessage = '';
    this.ctfService.startChallenge(nickname).subscribe({
      next: (response) => {
        this.sessionId = response.session_id;
        this.instructions = response.instructions;
        this.hackerNickname = nickname;
        
        // Sauvegarder dans localStorage
        localStorage.setItem('ctf_session_id', this.sessionId);
        localStorage.setItem('ctf_hacker_nickname', nickname);
        
        // Si le challenge est déjà complété
        if (response.already_completed) {
          this.currentStep = 'success';
          this.completionTime = response.completion_time || 0;
          this.userRank = response.rank || 0;
          this.animations = [];
          this.showAnimation = true;
          this.playAnimations();
          return;
        }

        // Si c'est une session reprise, restaurer l'état approprié
        if (response.resumed) {
          this.restoreSession(this.sessionId);
        } else {
          // Nouvelle session, commencer aux instructions
          this.currentStep = 'instructions';
          this.loadLeaderboard();
          this.startTimer();
        }
      },
      error: (error) => {
        this.errorMessage = error.error?.error || error.error?.message || 'Error starting the challenge';
      }
    });
  }

  startTimer(): void {
    // Mettre à jour le timer toutes les secondes
    this.updateTimer();
    this.timerInterval = setInterval(() => {
      this.updateTimer();
    }, 1000);
  }

  updateTimer(): void {
    if (this.sessionId) {
      this.ctfService.getSessionInfo(this.sessionId).subscribe({
        next: (info) => {
          this.elapsedTime = info.elapsed_time;
          this.hackerNickname = info.hacker_nickname;
          // Sauvegarder l'état dans localStorage pour éviter la réinitialisation
          localStorage.setItem('ctf_session_id', this.sessionId);
          localStorage.setItem('ctf_elapsed_time', this.elapsedTime.toString());
          localStorage.setItem('ctf_hacker_nickname', this.hackerNickname);
          
          if (info.is_completed && this.timerInterval) {
            clearInterval(this.timerInterval);
            localStorage.removeItem('ctf_elapsed_time');
          }
        },
        error: (error) => {
          console.error('Erreur lors de la mise à jour du timer:', error);
        }
      });
    }
  }

  stopChallenge(): void {
    // Kill session on backend so user can start again from 0 (same or new nickname)
    const sessionToAbandon = this.sessionId;
    if (sessionToAbandon) {
      this.ctfService.abandonSession(sessionToAbandon).subscribe({
        next: () => {},
        error: () => {}
      });
    }
    // Clean up local timer and state
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
    localStorage.removeItem('ctf_session_id');
    localStorage.removeItem('ctf_elapsed_time');
    localStorage.removeItem('ctf_hacker_nickname');
    
    // Reset component variables
    this.hackerNickname = '';
    this.sessionId = '';
    this.elapsedTime = 0;
    this.currentStep = 'nickname';
    // Do not redirect, keep the user on the challenge page
  }

  formatTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  }


  goToLogin(): void {
    this.currentStep = 'login';
    this.successMessage = '';
    this.errorMessage = '';
  }

  /** Ouvre la page de l'image de la maison (uniquement après login réussi). */
  goToHouseImage(): void {
    if (this.sessionId) {
      this.router.navigate(['/_my_challenge/image'], { queryParams: { session_id: this.sessionId } });
    }
  }

  /** Retour à l'étape précédente dans le challenge (dans la section challenge, pas la nav). */
  goBackToPreviousStep(): void {
    this.errorMessage = '';
    this.successMessage = '';
    if (this.currentStep === 'instructions') {
      // Ne pas abandonner la session côté backend : on vide seulement l'UI pour revoir le formulaire pseudo.
      // La session reste active ; si l'utilisateur ressaisit le même pseudo, on reprend la session (compteur conservé).
      // La session n'est abandonnée que via Stop ou en validant le bon flag.
      this.clearSession();
      this.hackerNickname = '';
      this.currentStep = 'nickname';
    } else if (this.currentStep === 'login') {
      this.currentStep = 'instructions';
      if (!this.instructions) {
        this.instructions = DEFAULT_INSTRUCTIONS;
      }
    } else if (this.currentStep === 'final_flag') {
      this.router.navigate(['/_my_challenge/image'], { queryParams: { session_id: this.sessionId } });
    }
  }

  /** True si l'étape actuelle permet d'afficher la flèche retour. */
  get showBackInSection(): boolean {
    return this.currentStep === 'instructions' || this.currentStep === 'login' || this.currentStep === 'final_flag';
  }

  submitLogin(): void {
    if (!this.loginUsername.trim() || !this.loginPassword.trim()) {
      this.errorMessage = 'Please enter a username and password';
      return;
    }

    this.errorMessage = '';
    this.successMessage = '';
    this.ctfService.ubiquitiLogin(this.sessionId, this.loginUsername.trim(), this.loginPassword.trim()).subscribe({
      next: (response) => {
        if (response.success) {
          this.router.navigate(['/_my_challenge/image'], { queryParams: { session_id: this.sessionId } });
        } else {
          this.errorMessage = response.message;
        }
      },
      error: (error) => {
        this.errorMessage = error.error?.error || error.error?.message || 'Login error';
      }
    });
  }


  submitFinalFlag(): void {
    if (!this.finalFlag.trim()) {
      this.errorMessage = 'Please enter the final flag';
      return;
    }

    this.errorMessage = '';
    this.ctfService.submitFinalFlag(this.sessionId, this.finalFlag.trim()).subscribe({
      next: (response) => {
        if (response.success) {
          this.completionTime = response.completion_time || 0;
          this.userRank = response.rank || 0;
          this.animations = response.animations || [];
          this.currentStep = 'success';
          this.showAnimation = true;
          this.playAnimations();
        } else {
          this.errorMessage = response.message;
        }
      },
      error: (error) => {
        this.errorMessage = error.error?.error || error.error?.message || 'Error submitting the flag';
      }
    });
  }

  playAnimations(): void {
    if (this.animations.length === 0) {
      this.showLeaderboard();
      return;
    }

    this.currentAnimationIndex = 0;
    const playNext = () => {
      if (this.currentAnimationIndex < this.animations.length) {
        setTimeout(() => {
          this.currentAnimationIndex++;
          if (this.currentAnimationIndex < this.animations.length) {
            playNext();
          } else {
            setTimeout(() => {
              this.showLeaderboard();
            }, 1000);
          }
        }, 1500);
      }
    };
    playNext();
  }

  showLeaderboard(): void {
    this.currentStep = 'leaderboard';
    this.loadLeaderboard();
    this.loadUserRanking();
  }

  loadLeaderboard(): void {
    this.ctfService.getLeaderboard().subscribe({
      next: (entries) => {
        this.leaderboard = entries;
      },
      error: (error) => {
        console.error('Erreur lors du chargement du leaderboard:', error);
      }
    });
  }

  loadUserRanking(): void {
    this.ctfService.getUserRanking(this.sessionId).subscribe({
      next: (entry) => {
        this.userEntry = entry;
      },
      error: (error) => {
        console.error('Erreur lors du chargement du rang:', error);
      }
    });
  }

  resetChallenge(): void {
    // Arrêter le timer
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
    // Nettoyer localStorage
    localStorage.removeItem('ctf_session_id');
    localStorage.removeItem('ctf_elapsed_time');
    localStorage.removeItem('ctf_hacker_nickname');
    // Réinitialiser toutes les variables
    this.currentStep = 'nickname';
    this.hackerNickname = ''; // Forcer à vider
    this.sessionId = '';
    this.elapsedTime = 0;
    this.loginUsername = '';
    this.loginPassword = '';
    this.finalFlag = '';
    this.errorMessage = '';
    this.successMessage = '';
    this.leaderboard = [];
    this.userEntry = null;
  }
}
