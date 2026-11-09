import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatbotService } from '../../core/services/chatbot';
import { BehaviorSubject, Observable } from 'rxjs';

interface Message {
  texte: string;
  estUtilisateur: boolean;
}

@Component({
  selector: 'app-chatbot',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './chatbot.html',
  styleUrl: './chatbot.css'
})
export class ChatbotComponent {
  private messagesSubject = new BehaviorSubject<Message[]>([
    { texte: 'Bonjour ! Comment puis-je t\'aider ?', estUtilisateur: false }
  ]);

  messages$: Observable<Message[]> = this.messagesSubject.asObservable();

  question = '';
  chargement = false;

  constructor(private chatbotService: ChatbotService) {}

  envoyer() {
    const texte = this.question.trim();
    if (!texte || this.chargement) return;

    const messagesActuels = this.messagesSubject.value;
    this.messagesSubject.next([
      ...messagesActuels,
      { texte, estUtilisateur: true }
    ]);

    this.question = '';
    this.chargement = true;

    this.chatbotService.envoyerQuestion(texte).subscribe({
      next: (res) => {
        const reponse = res.success ? (res.reponse || 'Pas de réponse') : (res.error || 'Erreur');
        const messagesActuels2 = this.messagesSubject.value;
        this.messagesSubject.next([
          ...messagesActuels2,
          { texte: reponse, estUtilisateur: false }
        ]);
        this.chargement = false;
      },
      error: () => {
        const messagesActuels3 = this.messagesSubject.value;
        this.messagesSubject.next([
          ...messagesActuels3,
          {
            texte: 'Erreur de connexion avec le serveur.',
            estUtilisateur: false
          }
        ]);
        this.chargement = false;
      }
    });
  }

  onKeyPress(event: KeyboardEvent) {
    if (event.key === 'Enter') {
      this.envoyer();
    }
  }
}