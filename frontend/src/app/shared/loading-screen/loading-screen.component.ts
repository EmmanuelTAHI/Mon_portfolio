import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading-screen',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './loading-screen.component.html',
  styleUrl: './loading-screen.component.css',
})
export class LoadingScreenComponent implements OnInit, OnDestroy {
  progress = 0;
  bootLines: string[] = [];
  statusLabel = 'Booting system...';
  showPrompt = false;
  private lineIndex = 0;
  private progressInterval: ReturnType<typeof setInterval> | null = null;
  private lineInterval: ReturnType<typeof setInterval> | null = null;
  private readonly bootScript = [
    '[  OK  ] Started Network Manager',
    '[  OK  ] Started SSH Daemon',
    '[  OK  ] Loaded kernel module tcp_ip',
    '[  OK  ] Mounted /dev/sda1',
    '[  OK  ] Started Security Audit Service',
    '[  OK  ] Loaded penetration testing framework',
    '[  OK  ] Initialized crypto modules',
    '[  OK  ] Started terminal multiplexer',
    '',
    'Arch Linux 6.x (tty1)',
    'portfolio login: _',
  ];

  ngOnInit(): void {
    this.lineInterval = setInterval(() => {
      if (this.lineIndex < this.bootScript.length) {
        this.bootLines = [...this.bootLines, this.bootScript[this.lineIndex]];
        this.lineIndex++;
      } else {
        if (this.lineInterval) clearInterval(this.lineInterval);
        this.showPrompt = true;
      }
    }, 180);

    this.progressInterval = setInterval(() => {
      if (this.progress >= 100) {
        if (this.progressInterval) clearInterval(this.progressInterval);
        return;
      }
      this.progress += Math.random() * 8 + 5;
      if (this.progress > 100) this.progress = 100;
      if (this.progress < 30) this.statusLabel = 'Loading kernel modules...';
      else if (this.progress < 60) this.statusLabel = 'Mounting filesystems...';
      else if (this.progress < 90) this.statusLabel = 'Starting services...';
      else this.statusLabel = 'Initializing workstation...';
    }, 140);
  }

  ngOnDestroy(): void {
    if (this.progressInterval) clearInterval(this.progressInterval);
    if (this.lineInterval) clearInterval(this.lineInterval);
  }
}
