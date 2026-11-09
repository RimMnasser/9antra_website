// Importe la configuration principale d'Angular
import {
  ApplicationConfig,
  provideBrowserGlobalErrorListeners
} from '@angular/core';

// Importe le système de navigation Angular
import { provideRouter } from '@angular/router';

// Active HttpClient et l'intercepteur JWT
import {
  provideHttpClient,
  withInterceptors
} from '@angular/common/http';

// Importe les routes Angular
import { routes } from './app.routes';

// Importe l'intercepteur qui ajoute le token JWT
// Importe l'intercepteur JWT
import {
  authentificationInterceptor
} from './core/interceptors/authentification-interceptor';



// Configuration principale de l'application Angular
export const appConfig: ApplicationConfig = {
  providers: [
    // Gère les erreurs globales du navigateur
    provideBrowserGlobalErrorListeners( ),

    // Active les routes Angular
    provideRouter(routes),

    // Active HttpClient et ajoute automatiquement le token JWT
    provideHttpClient(
      withInterceptors([authentificationInterceptor])
    )
  ]
};
