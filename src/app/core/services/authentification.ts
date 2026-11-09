// Injectable permet d'utiliser ce service dans les composants Angular
import { Injectable } from '@angular/core';

// HttpClient envoie la requête vers Flask
import { HttpClient } from '@angular/common/http';

// Observable représente la réponse asynchrone de l'API
import { Observable } from 'rxjs';


// Structure de la réponse envoyée par Flask après la connexion
export interface ReponseConnexion {
  // Token utilisé pour accéder aux routes protégées
  access_token: string;

  // Message de confirmation
  message: string;

  // Informations publiques de l'administrateur
  utilisateur: {
    id: number;
    email: string;
    role: string;
  };
}


// Rend le service disponible dans toute l'application
@Injectable({
  providedIn: 'root'
} )
export class Authentification {
  // Adresse de la route de connexion Flask
  private apiUrl = 'http://127.0.0.1:5000/api/auth/connexion';

  // Injecte HttpClient dans le service
  constructor(private http: HttpClient ) {}

  // Envoie l'email et le mot de passe à Flask
  connexion(
    email: string,
    motDePasse: string
  ): Observable<ReponseConnexion> {
    // Prépare les données attendues par Flask
    const donnees = {
      email: email,
      mot_de_passe: motDePasse
    };

    // Envoie la requête POST et retourne la réponse
    return this.http.post<ReponseConnexion>(
      this.apiUrl,
      donnees
     );
  }

  // Enregistre le token dans le navigateur
  enregistrerToken(token: string): void {
    localStorage.setItem('access_token', token);
  }

  // Récupère le token enregistré
  recupererToken(): string | null {
    return localStorage.getItem('access_token');
  }

  // Supprime le token lors de la déconnexion
  deconnecter(): void {
    localStorage.removeItem('access_token');
  }
}
