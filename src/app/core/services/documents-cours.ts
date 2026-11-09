// Permet d'utiliser ce service dans toute l'application
import { Injectable } from '@angular/core';

// Permet d'envoyer des requêtes HTTP à Flask
import { HttpClient } from '@angular/common/http';

// Représente les réponses asynchrones de l'API
import { Observable } from 'rxjs';

// Importe le modèle d'un document de cours
import { DocumentCours } from '../models/document-cours';


// Rend le service disponible dans tous les composants Angular
@Injectable({
  providedIn: 'root'
} )
export class DocumentsCours {
  // Adresse de base des routes documents dans Flask
  private apiUrl = 'http://127.0.0.1:5000/api/formations';

  // Injecte HttpClient pour communiquer avec Flask
  constructor(private http: HttpClient ) {}

  // Récupère tous les documents d'une formation
  listerDocuments(
    formationId: number
  ): Observable<DocumentCours[]> {
    // Appelle GET /api/formations/<id>/documents
    return this.http.get<DocumentCours[]>(
      `${this.apiUrl}/${formationId}/documents`
     );
  }

  // Importe un fichier pour une formation
  importerDocument(
    formationId: number,
    fichier: File
  ): Observable<DocumentCours> {
    // FormData est obligatoire pour envoyer un fichier
    const donnees = new FormData();

    // Le nom "fichier" doit correspondre au nom utilisé dans Flask
    donnees.append('fichier', fichier);

    // Envoie le fichier à Flask
    // Ne définis pas manuellement Content-Type : le navigateur le fait
    return this.http.post<DocumentCours>(
      `${this.apiUrl}/${formationId}/documents`,
      donnees
     );
  }

  // Télécharge un document sous forme de Blob
  telechargerDocument(documentId: number): Observable<Blob> {
    // Appelle la route Flask de téléchargement
    return this.http.get(
      `${this.apiUrl}/documents/${documentId}/download`,
      { responseType: 'blob' }
     );
  }

  // Supprime un document
  supprimerDocument(documentId: number): Observable<void> {
    // Appelle la route DELETE Flask
    return this.http.delete<void>(
      `${this.apiUrl}/documents/${documentId}`
     );
  }
}
