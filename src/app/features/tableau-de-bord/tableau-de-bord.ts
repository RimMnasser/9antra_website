// Importe le décorateur Component
import { Component } from '@angular/core';

// Permet d'utiliser routerLink dans le HTML
import { Router, RouterLink } from '@angular/router';

// Service d'authentification
import { Authentification } from '../../core/services/authentification';
import { ChatbotComponent } from '../../features/chatbot/chatbot';

// Composant principal de l'espace administrateur
@Component({
  selector: 'app-tableau-de-bord',
  standalone: true,
  imports: [RouterLink,ChatbotComponent],
  templateUrl: './tableau-de-bord.html',
  styleUrl: './tableau-de-bord.css'
})
export class TableauDeBord {
  // Titre affiché dans la page
  titre = 'Tableau de bord administrateur';

  // Valeurs provisoires qui seront reliées à l'API plus tard
  nombreFormations = 0;
  nombreDocuments = 0;

  // Injecte le routeur et le service d'authentification
  constructor(
    private router: Router,
    private authentification: Authentification
  ) {}

  // Déconnecte l'administrateur
  deconnecter(): void {
    // Supprime le token JWT du navigateur
    this.authentification.deconnecter();

    // Retourne vers la page de connexion
    this.router.navigate(['/connexion']);
  }
}
