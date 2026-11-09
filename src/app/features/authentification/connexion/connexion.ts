// Importe les outils Angular du composant
import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
// À ajouter avec les autres imports
import { Router } from '@angular/router';

// Permet d'utiliser [(ngModel)] dans le formulaire
import { FormsModule } from '@angular/forms';

// Service de connexion administrateur
import { Authentification } from '../../../core/services/authentification';


// Configuration du composant de connexion
@Component({
  selector: 'app-connexion',
  standalone: true,
  imports: [FormsModule, CommonModule],
  templateUrl: './connexion.html',
  styleUrl: './connexion.css'
})
export class Connexion {
  // Valeur saisie dans le champ email
  email = '';

  // Valeur saisie dans le champ mot de passe
  motDePasse = '';

  // Message affiché lorsqu'une erreur survient
  erreur = '';

  // Indique qu'une connexion est en cours
  chargement = false;

  // Injecte le service d'authentification
  private authentification = inject(Authentification);
  // Injecte le système de navigation Angular
  private router = inject(Router);

  // Méthode appelée lors de l'envoi du formulaire
  seConnecter(): void {
    // Réinitialise l'ancien message d'erreur
    this.erreur = '';

    // Vérifie que les champs sont remplis
    if (!this.email || !this.motDePasse) {
      this.erreur = 'Veuillez remplir tous les champs';
      return;
    }

    // Active l'indicateur de chargement
    this.chargement = true;

    // Envoie les identifiants à l'API Flask
    this.authentification
      .connexion(this.email, this.motDePasse)
      .subscribe({
        // Exécuté si Flask accepte la connexion
        next: (reponse) => {
          // Enregistre le token JWT dans le navigateur
          this.authentification.enregistrerToken(
            reponse.access_token
          );

          this.router.navigate(['/tableau-de-bord']);

          this.chargement = false;
          
        },


        // Exécuté si les identifiants sont incorrects
        error: () => {
          this.erreur = 'Email ou mot de passe incorrect';
          this.chargement = false;
        }
      });
  }
}
