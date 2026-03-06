import { Component, OnInit, OnDestroy, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-hero-terminal',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './hero-terminal.component.html',
})
export class HeroTerminalComponent implements OnInit, OnDestroy {
  @Input() role = 'Cybersecurity Student | Pentester';
  @Input() fullName = 'Emmanuel TAHI';
  @Input() description = 'I excel at crafting secure digital experiences and I am proficient in penetration testing, various programming languages and security technologies.';

  /** Ligne actuellement en cours de saisie (typing) */
  currentLine = '';
  /** Index du caractère dans la ligne en cours */
  private charIndex = 0;
  /** Index de la ligne affichée (0 = commande, 1 = role, 2 = name, 3 = description) */
  lineIndex = 0;
  /** Lignes complètes déjà affichées */
  displayedLines: string[] = [];
  /** Exposé pour le template (nombre de lignes de contenu) */
  get contentLinesLength(): number {
    return this.contentLines.length;
  }
  /** Contenu à taper ligne par ligne (après la commande) */
  private get contentLines(): string[] {
    return [this.role, this.fullName, this.description];
  }
  /** Commande affichée au démarrage */
  readonly commandLine = 'cat ~/intro.txt';
  /** Afficher le curseur clignotant */
  showCursor = true;
  private timer: ReturnType<typeof setInterval> | null = null;
  private cursorTimer: ReturnType<typeof setInterval> | null = null;

  ngOnInit(): void {
    // Petit délai avant de commencer à taper la commande
    setTimeout(() => this.runTyping(), 400);
    this.cursorTimer = setInterval(() => (this.showCursor = !this.showCursor), 530);
  }

  private runTyping(): void {
    const delayMs = 45;
    const delayAfterCommand = 600;

    const typeNext = () => {
      // Phase 1 : taper la commande
      if (this.lineIndex === 0 && this.charIndex < this.commandLine.length) {
        this.currentLine = this.commandLine.slice(0, this.charIndex + 1);
        this.charIndex++;
        this.timer = setTimeout(typeNext, delayMs);
        return;
      }
      if (this.lineIndex === 0 && this.charIndex === this.commandLine.length) {
        this.displayedLines.push(this.commandLine);
        this.currentLine = '';
        this.charIndex = 0;
        this.lineIndex = 1;
        this.timer = setTimeout(typeNext, delayAfterCommand);
        return;
      }
      // Phase 2 : taper les lignes de contenu (role, name, description)
      if (this.lineIndex <= this.contentLines.length) {
        const line = this.contentLines[this.lineIndex - 1];
        if (this.charIndex < line.length) {
          this.currentLine = line.slice(0, this.charIndex + 1);
          this.charIndex++;
          this.timer = setTimeout(typeNext, delayMs);
          return;
        }
        this.displayedLines.push(line);
        this.currentLine = '';
        this.charIndex = 0;
        this.lineIndex++;
        if (this.lineIndex <= this.contentLines.length) {
          this.timer = setTimeout(typeNext, delayAfterCommand * 0.5);
        }
      }
    };

    typeNext();
  }

  ngOnDestroy(): void {
    if (this.timer) clearTimeout(this.timer);
    if (this.cursorTimer) clearInterval(this.cursorTimer);
  }
}
