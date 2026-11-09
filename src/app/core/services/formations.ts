// Permet d'injecter le service dans les composants
import { Injectable } from '@angular/core';

// Permet d'envoyer des requêtes HTTP à Flask
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
// Représente une réponse asynchrone
import { Observable } from 'rxjs';

// Modèle TypeScript d'une formation
import { Formation } from '../models/formation';


// Rend le service disponible dans toute l'application
@Injectable({
  providedIn: 'root'
} )
export class Formations {
  // Adresse commune des routes formations Flask
  private apiUrl = 'http://127.0.0.1:5000/api/formations';

  // Injecte HttpClient
  constructor(private http: HttpClient ) {}

  // Récupère toutes les formations
  getFormations(): Observable<Formation[]> {
    return this.http.get<Formation[]>(this.apiUrl );
  }
  // Récupère une formation précise depuis l'API Flask
  getFormation(id: number): Observable<Formation> {
  // Envoie une requête GET vers /api/formations/id
  return this.http.get<Formation>(
    `${this.apiUrl}/${id}`
   );
  }


  // Crée une nouvelle formation
  creerFormation(
    formation: Omit<Formation, 'id' | 'created_at' | 'updated_at'>
  ): Observable<Formation> {
    return this.http.post<Formation>(this.apiUrl, formation );
  }

  // Modifie une formation existante
  modifierFormation(
    id: number,
    formation: Partial<Formation>
  ): Observable<Formation> {
    return this.http.put<Formation>(
      `${this.apiUrl}/${id}`,
      formation
     );
  }

  // Supprime une formation
  supprimerFormation(id: number): Observable<void> {
    return this.http.delete<void>(
      `${this.apiUrl}/${id}`
     );
  }

  



  
}
