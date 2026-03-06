import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE } from '../constants/api';
import { Skill } from '../../models/skill.model';

@Injectable({ providedIn: 'root' })
export class SkillService {
  private url = `${API_BASE}/skills/`;

  constructor(private http: HttpClient) {}

  getAll(): Observable<Skill[]> {
    return this.http.get<Skill[]>(this.url);
  }
}
