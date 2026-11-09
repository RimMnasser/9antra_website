// Importe Component, OnInit et inject
import { Component, OnInit, inject, signal } from '@angular/core';

// Permet d'utiliser routerLink
import { RouterLink } from '@angular/router';

// Modèle d'une formation
import { Formation } from '../../../core/models/formation';

// Service qui appelle l'API Flask
import { Formations } from '../../../core/services/formations';


@Component({
  selector: 'app-liste-formations',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './liste-formations.html',
  styleUrl: './liste-formations.css'
})
export class ListeFormations implements OnInit {
  // Stocke les formations et actualise automatiquement le HTML
  formations = signal<Formation[]>([]);

  // Vrai pendant le chargement, puis faux après la réponse
  chargement = signal(true);

  // Message d'erreur éventuel
  erreur = signal('');

  // Injecte le service des formations
  private serviceFormations = inject(Formations);

  // Appel exécuté à l'ouverture du composant
  ngOnInit(): void {
    // Demande les formations à Flask
    this.serviceFormations.getFormations().subscribe({
      // Reçoit les données de l'API
      next: (donnees) => {
        // Met à jour le signal avec les formations reçues
        this.formations.set(donnees);

        // Arrête l'affichage du chargement
        this.chargement.set(false);

        // Affiche les données dans la console
        console.log('Formations reçues :', donnees);
      },

      // Gère les erreurs de l'API
      error: (erreur) => {
        // Affiche l'erreur dans la console
        console.error('Erreur API :', erreur);

        // Définit le message affiché à l'utilisateur
        this.erreur.set('Impossible de charger les formations');

        // Arrête aussi le chargement en cas d'erreur
        this.chargement.set(false);
      }
    });
  }
// Supprime une formation depuis l'interface Angular
supprimer(id: number): void {
  // Demande une confirmation avant la suppression
  const confirmer = confirm(
    'Voulez-vous vraiment supprimer cette formation ?'
  );

  // Arrête la méthode si l'administrateur annule
  if (!confirmer) {
    return;
  }

  // Appelle la route DELETE de Flask
  this.serviceFormations.supprimerFormation(id).subscribe({
    // Exécuté après la suppression réussie
    next: () => {
      // Retire la formation supprimée de la liste affichée
      this.formations.update((liste) =>
        liste.filter((formation) => formation.id !== id)
      );
    },

    // Exécuté si la suppression échoue
    error: (erreur) => {
      // Affiche l'erreur dans la console
      console.error('Erreur suppression :', erreur);

      // Affiche un message dans la page
      this.erreur.set('Impossible de supprimer la formation');
    }
  });
}




}
