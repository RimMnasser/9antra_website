// Importe les outils du composant
import { Component, inject } from '@angular/core';
import { ActivatedRoute, Router, RouterLink } from '@angular/router'; // Permet d'utiliser [(ngModel)] dans le formulaire
import { FormsModule } from '@angular/forms';

// Permet de naviguer vers la liste après l'enregistrement


// Service qui communique avec Flask
import { Formations } from '../../../core/services/formations';

import { CommonModule } from '@angular/common';

// Composant du formulaire de création d'une formation
@Component({
  selector: 'app-formulaire-formation',
  standalone: true,
  imports: [FormsModule, CommonModule, RouterLink],
  templateUrl: './formulaire-formation.html',
  styleUrl: './formulaire-formation.css'
})
export class FormulaireFormation {
  // Champs liés au formulaire HTML
  titre = '';
  description = '';
  categorie = '';
  duree = '';
  niveau = '';

  // Message d'erreur affiché à l'écran
  erreur = '';

  // Indique que l'enregistrement est en cours
  chargement = false;

  // Injecte le service formations et le routeur
  private formationsService = inject(Formations);
  private router = inject(Router);

  // Enregistre la formation dans MySQL via Flask
  enregistrer(): void {
    // Vérifie que le titre est renseigné
    if (!this.titre.trim()) {
      this.erreur = 'Le titre est obligatoire';
      return;
    }

    // Active l'indicateur de chargement
    this.chargement = true;
    this.erreur = '';

    // Prépare les données envoyées à l'API
    const formation = {
      titre: this.titre,
      description: this.description,
      categorie: this.categorie,
      duree: this.duree,
      niveau: this.niveau,
      statut: 'active'
    };

    // Appelle la route POST Flask
    this.formationsService.creerFormation(formation).subscribe({
      // En cas de succès, retourne à la liste
      next: () => {
        this.router.navigate(['/formations']);
      },

      // En cas d'erreur, affiche un message
      error: () => {
        this.erreur = 'Impossible de créer la formation';
        this.chargement = false;
      }
    });
  }
}
