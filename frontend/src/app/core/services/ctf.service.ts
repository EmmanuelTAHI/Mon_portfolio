import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE } from '../constants/api';

export interface StartChallengeResponse {
  session_id: string;
  message: string;
  instructions: string;
  resumed?: boolean;
}

export interface SubmitFlagResponse {
  success: boolean;
  message: string;
  next_step?: string;
}

export interface LoginResponse {
  success: boolean;
  message: string;
  image_url?: string;
}

export interface FinalFlagResponse {
  success: boolean;
  message: string;
  completion_time?: number;
  rank?: number;
  animations?: string[];
}

export interface LeaderboardEntry {
  hacker_nickname: string;
  completion_time_seconds: number;
  completion_time_formatted: string;
  rank: number;
  completed_at: string;
}

@Injectable({ providedIn: 'root' })
export class CtfService {
  private baseUrl = `${API_BASE}/ctf/`;

  constructor(private http: HttpClient) {}

  startChallenge(hackerNickname: string): Observable<StartChallengeResponse> {
    return this.http.post<StartChallengeResponse>(`${this.baseUrl}start/`, {
      hacker_nickname: hackerNickname
    });
  }

  submitFirstFlag(sessionId: string, flag: string): Observable<SubmitFlagResponse> {
    return this.http.post<SubmitFlagResponse>(`${this.baseUrl}submit-first-flag/`, {
      session_id: sessionId,
      flag: flag
    });
  }

  ubiquitiLogin(sessionId: string, username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.baseUrl}ubiquiti-login/`, {
      session_id: sessionId,
      username: username,
      password: password
    });
  }

  downloadImage(sessionId: string): Observable<Blob> {
    const params = new HttpParams().set('session_id', sessionId);
    return this.http.get(`${this.baseUrl}download-image/`, {
      params,
      responseType: 'blob'
    });
  }

  submitFinalFlag(sessionId: string, flag: string): Observable<FinalFlagResponse> {
    return this.http.post<FinalFlagResponse>(`${this.baseUrl}submit-final-flag/`, {
      session_id: sessionId,
      flag: flag
    });
  }

  getLeaderboard(): Observable<LeaderboardEntry[]> {
    return this.http.get<LeaderboardEntry[]>(`${this.baseUrl}leaderboard/`);
  }

  getUserRanking(sessionId: string): Observable<LeaderboardEntry> {
    const params = new HttpParams().set('session_id', sessionId);
    return this.http.get<LeaderboardEntry>(`${this.baseUrl}user-ranking/`, { params });
  }

  getSessionInfo(sessionId: string): Observable<{hacker_nickname: string, elapsed_time: number, is_completed: boolean, current_step: number}> {
    const params = new HttpParams().set('session_id', sessionId);
    return this.http.get<{hacker_nickname: string, elapsed_time: number, is_completed: boolean, current_step: number}>(`${this.baseUrl}session-info/`, { params });
  }

  checkSession(sessionId: string): Observable<{
    exists: boolean;
    session_id?: string;
    hacker_nickname?: string;
    elapsed_time?: number;
    is_completed?: boolean;
    current_step?: number;
    started_at?: string;
    error?: string;
  }> {
    const params = new HttpParams().set('session_id', sessionId);
    return this.http.get<{
      exists: boolean;
      session_id?: string;
      hacker_nickname?: string;
      elapsed_time?: number;
      is_completed?: boolean;
      current_step?: number;
      started_at?: string;
      error?: string;
    }>(`${this.baseUrl}check-session/`, { params });
  }

  /** Abandons the current session so the user can start again from scratch. */
  abandonSession(sessionId: string): Observable<{ success: boolean; message?: string }> {
    return this.http.post<{ success: boolean; message?: string }>(
      `${this.baseUrl}abandon-session/`,
      { session_id: sessionId }
    );
  }
}
