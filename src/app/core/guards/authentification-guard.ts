// Importe le type utilisé pour créer un guard fonctionnel
import { CanActivateFn, Router } from '@angular/router';

// Permet d'injecter Router dans le guard
import { inject } from '@angular/core';


// Vérifie si l'administrateur possède un token JWT
export const authentificationGuard: CanActivateFn = () => {
  // Récupère le token enregistré après la connexion
  const token = localStorage.getItem('access_token');

  // Injecte le système de navigation Angular
  const router = inject(Router);

  // Si le token existe, l'accès est autorisé
  if (token) {
    return true;
  }

  // Sinon, redirige l'utilisateur vers la connexion
  router.navigate(['/connexion']);

  // Refuse l'accès à la page protégée
  return false;
};
