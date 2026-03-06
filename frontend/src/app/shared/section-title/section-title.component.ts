import { Component, input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-section-title',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="section-title-block mb-8">
      <h2 class="font-jetbrains text-2xl sm:text-3xl tracking-wider text-neonGreen mb-2 flex items-center gap-2">
        <span class="text-gray-500 font-jetbrains">[</span>
        <span class="drop-shadow-[0_0_15px_rgba(0,255,159,0.3)]">{{ title() }}</span>
        <span class="text-gray-500 font-jetbrains">]</span>
      </h2>
      @if (subtitle()) {
        <p class="font-jetbrains text-gray-400 text-sm max-w-2xl">{{ subtitle() }}</p>
      }
      <div class="h-px w-24 bg-gradient-to-r from-neonGreen to-transparent mt-3 opacity-60"></div>
    </div>
  `,
  styles: [],
})
export class SectionTitleComponent {
  title = input.required<string>();
  subtitle = input<string>('');
}
