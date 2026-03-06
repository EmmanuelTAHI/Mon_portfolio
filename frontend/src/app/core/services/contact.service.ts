import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { API_BASE } from '../constants/api';
import { ContactPayload } from '../../models/contact.model';

export interface ContactSuccess {
  message: string;
  id: number;
}

export interface ContactError {
  detail?: string;
  code?: string;
}

@Injectable({ providedIn: 'root' })
export class ContactService {
  private url = `${API_BASE}/contact/`;

  constructor(private http: HttpClient) {}

  send(payload: ContactPayload): Observable<ContactSuccess> {
    return this.http.post<ContactSuccess>(this.url, payload).pipe(
      catchError((err) => {
        const body: ContactError = err.error || {};
        const message = body.detail || 'Failed to send. Try again or use social links.';
        return throwError(() => ({ message }));
      })
    );
  }
}
