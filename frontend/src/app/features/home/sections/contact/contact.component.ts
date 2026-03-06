import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SectionTitleComponent } from '@app/shared/section-title/section-title.component';
import { ContactService } from '@app/core/services/contact.service';
import { ContactPayload } from '@app/models/contact.model';

@Component({
  selector: 'app-contact',
  standalone: true,
  imports: [CommonModule, FormsModule, SectionTitleComponent],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.css',
})
export class ContactComponent {
  name = '';
  email = '';
  message = '';
  sending = false;
  sent = false;
  error = '';

  constructor(private contactService: ContactService) {}

  submit(): void {
    this.error = '';
    if (!this.name.trim() || !this.email.trim() || !this.message.trim()) {
      this.error = 'Please fill all fields.';
      return;
    }
    // Validation email basique
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.email)) {
      this.error = 'Please enter a valid email address.';
      return;
    }
    this.sending = true;
    this.contactService.send({ name: this.name, email: this.email, message: this.message }).subscribe({
      next: () => {
        this.sent = true;
        this.name = '';
        this.email = '';
        this.message = '';
        this.sending = false;
      },
      error: (err: { message?: string }) => {
        this.error = err?.message || 'Failed to send. Try again or use social links.';
        this.sending = false;
      },
    });
  }
}
