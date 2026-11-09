// Importe les outils Angular du composant
import { Component, OnInit, inject } from '@angular/core';

// Permet d'utiliser les champs du formulaire
import { FormsModule } from '@angular/forms';

// Permet de récupérer l'identifiant dans l'URL et de naviguer
import { ActivatedRoute, Router, RouterLink } from '@angular/router'; 

// Service des formations
import { Formations } from '../../../core/services/formations';

// Modèle Formation
import { Formation } from '../../../core/models/formation';


@Component({
  selector: 'app-modifier-formation',
  standalone: true,
  imports: [FormsModule, RouterLink],
  templateUrl: './modifier-formation.html',
  styleUrl: './modifier-formation.css'
})
export class ModifierFormation implements OnInit {
  // Identifiant récupéré depuis l'URL
  id = 0;

  // Champs du formulaire
  titre = '';
  description = '';
  categorie = '';
  duree = '';
  niveau = '';
  statut = 'active';

  // Message d'erreur éventuel
  erreur = '';

  // Injecte les outils nécessaires
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private serviceFormations = inject(Formations);

  // Charge la formation au démarrage
  ngOnInit(): void {
    // Récupère l'id présent dans /modifier-formation/2
    this.id = Number(this.route.snapshot.paramMap.get('id'));

    // Demande la formation à Flask
    this.serviceFormations.getFormation(this.id).subscribe({
      // Remplit le formulaire avec les données reçues
      next: (formation: Formation) => {
        this.titre = formation.titre;
        this.description = formation.description || '';
        this.categorie = formation.categorie || '';
        this.duree = formation.duree || '';
        this.niveau = formation.niveau || '';
        this.statut = formation.statut;
      },

      // Affiche une erreur si la formation est introuvable
      error: () => {
        this.erreur = 'Formation introuvable';
      }
    });
  }

  // Enregistre les modifications
  enregistrer(): void {
    // Vérifie que le titre est rempli
    if (!this.titre.trim()) {
      this.erreur = 'Le titre est obligatoire';
      return;
    }

    // Prépare les données à envoyer à Flask
    const donnees = {
      titre: this.titre,
      description: this.description,
      categorie: this.categorie,
      duree: this.duree,
      niveau: this.niveau,
      statut: this.statut
    };

    // Appelle la route PUT Flask
    this.serviceFormations.modifierFormation(this.id, donnees).subscribe({
      // Retourne à la liste après modification
      next: () => {
        this.router.navigate(['/formations']);
      },

      // Affiche une erreur si la modification échoue
      error: () => {
        this.erreur = 'Impossible de modifier la formation';
      }
    });
  }
}
