import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ChatbotResponse {
  success: boolean;
  reponse?: string;
  error?: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {

  private apiUrl = 'http://localhost:5000/api/chatbot/chat';

  constructor(private http: HttpClient) {}

  envoyerQuestion(question: string): Observable<ChatbotResponse> {
    return this.http.post<ChatbotResponse>(this.apiUrl, { question });
  }
}