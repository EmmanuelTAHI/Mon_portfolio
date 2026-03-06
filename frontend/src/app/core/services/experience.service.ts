import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE } from '../constants/api';
import { Experience } from '../../models/experience.model';

@Injectable({ providedIn: 'root' })
export class ExperienceService {
  private url = `${API_BASE}/experience/`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Experience[]> {
    return this.http.get<Experience[]>(this.url);
  }
}
