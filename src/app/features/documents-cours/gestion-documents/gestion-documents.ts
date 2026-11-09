import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { DocumentCours } from '../../../core/models/document-cours';
import { DocumentsCours } from '../../../core/services/documents-cours';
import { BehaviorSubject } from 'rxjs';
@Component({
  selector: 'app-gestion-documents',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './gestion-documents.html',
  styleUrl: './gestion-documents.css'
})
export class GestionDocuments implements OnInit {
  // Identifiant de la formation récupéré depuis l'URL
  formationId = 0;

  // Liste des documents associés à la formation
  documents: DocumentCours[] = [];

  // Fichier choisi dans le champ input
      private fichierSelectionneSubject = new BehaviorSubject<File | null>(null);
    fichierSelectionne$ = this.fichierSelectionneSubject.asObservable();

    private nomFichierSubject = new BehaviorSubject<string>('');
    nomFichier$ = this.nomFichierSubject.asObservable();

  // Nom affiché dans l'interface
  nomFichier = '';

  // États et messages de l'interface
  chargement = true;
  message = '';
  erreur = '';

  private route = inject(ActivatedRoute);
  private documentsService = inject(DocumentsCours);

  ngOnInit(): void {
    // Récupère l'identifiant présent dans l'URL : /formations/2/documents
    this.formationId = Number(this.route.snapshot.paramMap.get('id'));

    if (!this.formationId) {
      this.erreur = 'Identifiant de formation invalide.';
      this.chargement = false;
      return;
    }

    this.chargerDocuments();
  }

  // Charge les documents depuis Flask
  chargerDocuments(): void {
    this.chargement = true;
    this.erreur = '';

    this.documentsService.listerDocuments(this.formationId).subscribe({
      next: (donnees) => {
        this.documents = donnees;
        this.chargement = false;
      },
      error: () => {
        this.erreur = 'Impossible de charger les documents.';
        this.chargement = false;
      }
    });
  }

  // Mémorise le fichier choisi par l'administrateur
  selectionnerFichier(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {
        this.fichierSelectionneSubject.next(null);
        this.nomFichierSubject.next('');
        this.message = 'Aucun fichier sélectionné.';
        return;
      }

      const fichier = input.files[0];
      this.fichierSelectionneSubject.next(fichier);
      this.nomFichierSubject.next(fichier.name);
          this.message = 'Fichier prêt à être importé.';
    this.erreur = '';
  }

  // Envoie le fichier à l'API Flask
importer(): void {
  const fichier = this.fichierSelectionneSubject.value;

  if (!fichier) {
    this.erreur = 'Veuillez choisir un fichier.';
    return;
  }

    this.message = 'Importation en cours...';
    this.erreur = '';

        this.documentsService
      .importerDocument(this.formationId, fichier)
      .subscribe({
        next: () => {
          this.message = 'Document importé avec succès.';
          this.fichierSelectionneSubject.next(null);
          this.nomFichierSubject.next('');
          this.chargerDocuments();
    },
        error: (response) => {
          this.erreur = response?.error?.erreur ||
            'Erreur lors de l’importation du document.';
          this.message = '';
        }
      });
  }

  // Télécharge un document depuis Flask
  telecharger(documentId: number): void {
    this.documentsService.telechargerDocument(documentId).subscribe({
      next: (fichier) => {
        const url = window.URL.createObjectURL(fichier);
        const lien = document.createElement('a');

        lien.href = url;
        lien.download = this.documents.find(
          (document) => document.id === documentId
        )?.nom_fichier || 'document';

        lien.click();
        window.URL.revokeObjectURL(url);
      },
      error: () => {
        this.erreur = 'Impossible de télécharger le document.';
      }
    });
  }

  // Supprime un document après confirmation
  supprimer(documentId: number): void {
    const confirmation = window.confirm(
      'Voulez-vous vraiment supprimer ce document ?'
    );

    if (!confirmation) {
      return;
    }

    this.documentsService.supprimerDocument(documentId).subscribe({
      next: () => {
        this.message = 'Document supprimé avec succès.';
        this.documents = this.documents.filter(
          (document) => document.id !== documentId
        );
      },
      error: () => {
        this.erreur = 'Impossible de supprimer le document.';
      }
    });
  }
}
