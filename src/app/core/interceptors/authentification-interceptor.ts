// Type utilisé pour créer un intercepteur HTTP fonctionnel
import { HttpInterceptorFn } from '@angular/common/http';


// Ajoute automatiquement le token JWT aux requêtes Angular
export const authentificationInterceptor: HttpInterceptorFn = (
  requete,
  suivant
 ) => {
  // Récupère le token enregistré après la connexion
  const token = localStorage.getItem('access_token');

  // Si aucun token n'existe, envoie la requête normalement
  if (!token) {
    return suivant(requete);
  }

  // Clone la requête et ajoute l'en-tête Authorization
  const requeteAvecToken = requete.clone({
    setHeaders: {
      Authorization: `Bearer ${token}`
    }
  });

  // Envoie la nouvelle requête vers Flask
  return suivant(requeteAvecToken);
};
