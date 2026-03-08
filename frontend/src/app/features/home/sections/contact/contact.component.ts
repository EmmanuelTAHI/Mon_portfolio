import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SectionTitleComponent } from '@app/shared/section-title/section-title.component';
import emailjs from '@emailjs/browser';

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

    // Use EmailJS directly
    emailjs.send(
      'service_dvdfxfg',     // Service ID
      'template_8gnwokd',    // Template ID
      {
        user_name: this.name,
        user_email: this.email,
        user_message: this.message
      },
      'vREBuWY3ZCsTyIFKc'    // Public Key
    ).then((response) => {
      this.sent = true;
      this.name = '';
      this.email = '';
      this.message = '';
      this.sending = false;
    }).catch((err) => {
      this.error = err?.text || 'Failed to send via EmailJS. Try again or use social links.';
      this.sending = false;
    });
  }
}
