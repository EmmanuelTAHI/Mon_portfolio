import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeroComponent } from './hero/hero.component';
import { LoadingScreenComponent } from '@app/shared/loading-screen/loading-screen.component';
import { InteractiveTerminalComponent } from '@app/shared/interactive-terminal/interactive-terminal.component';
import { AboutComponent } from './sections/about/about.component';
import { SkillsComponent } from './sections/skills/skills.component';
import { ProjectsComponent } from './sections/projects/projects.component';
import { ExperienceComponent } from './sections/experience/experience.component';
import { CertificationsComponent } from './sections/certifications/certifications.component';
import { ContactComponent } from './sections/contact/contact.component';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule,
    HeroComponent,
    LoadingScreenComponent,
    InteractiveTerminalComponent,
    AboutComponent,
    SkillsComponent,
    ProjectsComponent,
    ExperienceComponent,
    CertificationsComponent,
    ContactComponent,
  ],
  templateUrl: './home.component.html',
})
export class HomeComponent implements OnInit {
  showLoading = true;

  ngOnInit(): void {
    setTimeout(() => {
      this.showLoading = false;
      this.scrollToHero();
    }, 3200);
  }

  /** Remet la page en haut (Hero) après la disparition du loading. */
  private scrollToHero(): void {
    requestAnimationFrame(() => {
      const hero = document.getElementById('hero');
      if (hero) {
        hero.scrollIntoView({ behavior: 'auto', block: 'start' });
      } else {
        window.scrollTo(0, 0);
      }
    });
  }
}
