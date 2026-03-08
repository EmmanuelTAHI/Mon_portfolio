import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { API_BASE } from '../constants/api';
import { ContactPayload } from '../../models/contact.model';

export interface ContactSuccess {
  message: string;
  id: number;
}

@Injectable({ providedIn: 'root' })
export class ContactService {
  private readonly contactUrl = `${API_BASE}/contact/`;

  constructor(private http: HttpClient) {}

  send(payload: ContactPayload): Observable<ContactSuccess> {
    return this.http.post<{ message: string; id: number }>(this.contactUrl, payload).pipe(
      map((res) => ({ message: res.message, id: res.id })),
      catchError((err) => {
        const message =
          err?.error?.detail ||
          err?.error?.message ||
          'Unable to send email. Please try again later or use the social links below.';
        return throwError(() => ({ message }));
      })
    );
  }
}
