import { Injectable } from '@angular/core';
import { Observable, from, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import emailjs from '@emailjs/browser';
import { environment } from '../../../environments/environment';
import { ContactPayload } from '../../models/contact.model';

export interface ContactSuccess {
  message: string;
  id: number;
}

@Injectable({ providedIn: 'root' })
export class ContactService {
  private get emailJsConfig(): { publicKey: string; serviceId: string; templateId: string } | null {
    const env = environment as Record<string, unknown>;
    const publicKey = env['emailJsPublicKey'] as string | undefined;
    const serviceId = env['emailJsServiceId'] as string | undefined;
    const templateId = env['emailJsTemplateId'] as string | undefined;
    if (publicKey && serviceId && templateId) {
      return { publicKey, serviceId, templateId };
    }
    return null;
  }

  send(payload: ContactPayload): Observable<ContactSuccess> {
    const config = this.emailJsConfig;
    if (!config) {
      return throwError(
        () => ({ message: 'EmailJS is not configured. Please try again later or use the social links below.' })
      );
    }

    const templateParams = {
      name: payload.name,
      email: payload.email,
      user_name: payload.name,
      user_email: payload.email,
      user_message: payload.message,
    };

    const promise = emailjs.send(
      config.serviceId,
      config.templateId,
      templateParams,
      config.publicKey
    );

    return from(promise).pipe(
      map(() => ({
        message: 'Votre message a été envoyé avec succès.',
        id: 0,
      })),
      catchError((err) => {
        const message =
          err?.text || err?.message || 'Unable to send email. Please try again later or use the social links below.';
        return throwError(() => ({ message }));
      })
    );
  }
}
