import { Component, ElementRef, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

interface LogLine {
  text: string;
  type: 'input' | 'output' | 'error' | 'success' | 'info';
}

@Component({
  selector: 'app-interactive-terminal',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './interactive-terminal.component.html',
  styleUrl: './interactive-terminal.component.css',
})
export class InteractiveTerminalComponent implements AfterViewInit {
  @ViewChild('inputEl') inputEl!: ElementRef<HTMLInputElement>;

  log: LogLine[] = [
    { text: 'Pentester Workstation v1.0 — Type "help" for available commands.', type: 'info' },
  ];
  currentInput = '';
  readonly prompt = 'root@sh00ter_X:~$';

  private sectionIds: Record<string, string> = {
    about: 'about',
    skills: 'skills',
    projects: 'projects',
    experience: 'experience',
    contact: 'contact',
  };

  private commands: Record<string, () => LogLine[]> = {
    help: () => [
      { text: 'Available commands:', type: 'output' },
      { text: '  help       — show this help', type: 'output' },
      { text: '  about      — about me & scroll to section', type: 'output' },
      { text: '  skills     — list skills & scroll to section', type: 'output' },
      { text: '  projects   — list projects & scroll to section', type: 'output' },
      { text: '  experience — experience timeline & scroll', type: 'output' },
      { text: '  contact    — contact form & scroll', type: 'output' },
      { text: '  clear      — clear terminal', type: 'output' },
    ],
    whoami: () => [
      { text: 'pentester', type: 'success' },
      { text: 'Cybersecurity & Penetration Testing enthusiast. Pentester | Security Researcher | Developer.', type: 'output' },
    ],
    about: () => {
      this.scrollToSection('about');
      return [
        { text: 'Redirecting to [about] section...', type: 'info' },
        { text: 'Cybersecurity student. Offensive security, CTF, secure development.', type: 'output' },
      ];
    },
    skills: () => {
      this.scrollToSection('skills');
      return [
        { text: 'Redirecting to [skills] dashboard...', type: 'info' },
        { text: 'Pentesting · Networking · Programming · Web · Security', type: 'output' },
      ];
    },
    projects: () => {
      this.scrollToSection('projects');
      return [
        { text: 'Redirecting to [projects] modules...', type: 'info' },
        { text: 'Security tools, web apps, automation, CTF writeups.', type: 'output' },
      ];
    },
    experience: () => {
      this.scrollToSection('experience');
      return [
        { text: 'Redirecting to [experience] timeline...', type: 'info' },
        { text: 'Education, labs, CTF, professional experience.', type: 'output' },
      ];
    },
    contact: () => {
      this.scrollToSection('contact');
      return [
        { text: 'Redirecting to [contact] form...', type: 'info' },
        { text: 'Get in touch via the form or social links.', type: 'output' },
      ];
    },
    clear: () => [],
    theme: () => [{ text: 'Use the theme toggle in the header (top-right).', type: 'info' }],
  };

  ngAfterViewInit(): void {
    // Ne pas focus l'input au chargement pour éviter que la page défile vers le COMMAND CENTER.
    // L'utilisateur peut cliquer dans le terminal pour taper.
  }

  onSubmit(): void {
    const raw = this.currentInput.trim();
    const cmd = raw.toLowerCase();
    this.log.push({ text: this.prompt + ' ' + raw, type: 'input' });
    this.currentInput = '';

    if (cmd === 'clear') {
      this.log = [];
      return;
    }

    const handler = this.commands[cmd];
    if (handler) {
      const lines = handler();
      this.log.push(...lines);
    } else if (cmd) {
      this.log.push({
        text: `bash: ${cmd}: command not found. Type "help" for available commands.`,
        type: 'error',
      });
    }
    this.scrollToBottom();
  }

  private scrollToSection(id: string): void {
    setTimeout(() => {
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  }

  private scrollToBottom(): void {
    setTimeout(() => {
      const el = document.getElementById('terminal-log');
      if (el) el.scrollTop = el.scrollHeight;
    }, 0);
  }
}
