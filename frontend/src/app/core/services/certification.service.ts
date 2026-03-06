import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE } from '../constants/api';
import { Certification } from '../../models/certification.model';

@Injectable({ providedIn: 'root' })
export class CertificationService {
  private url = `${API_BASE}/certifications/`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Certification[]> {
    return this.http.get<Certification[]>(this.url);
  }

  getById(id: number): Observable<Certification> {
    return this.http.get<Certification>(`${this.url}${id}/`);
  }
}
