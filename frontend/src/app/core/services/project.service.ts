import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { API_BASE } from '../constants/api';
import { Project } from '../../models/project.model';

export interface PaginatedProjectsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Project[];
}

@Injectable({ providedIn: 'root' })
export class ProjectService {
  private url = `${API_BASE}/projects/`;

  constructor(private http: HttpClient) {}

  /** Liste de la première page (backend renvoie toujours une réponse paginée). */
  getAll(): Observable<Project[]> {
    return this.http.get<PaginatedProjectsResponse>(this.url).pipe(
      map((res) => res.results ?? [])
    );
  }

  getPaginated(page: number = 1, pageSize: number = 3): Observable<PaginatedProjectsResponse> {
    const params = new HttpParams()
      .set('page', page.toString())
      .set('page_size', pageSize.toString());
    
    return this.http.get<PaginatedProjectsResponse>(this.url, { params });
  }

  getBySlug(slug: string): Observable<Project> {
    return this.http.get<Project>(`${this.url}${slug}/`);
  }
}
