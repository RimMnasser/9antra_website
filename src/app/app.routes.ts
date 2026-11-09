// Importe le type Route d'Angular
import { Routes } from '@angular/router';
// Importe le tableau de bord administrateur
import { TableauDeBord } from './features/tableau-de-bord/tableau-de-bord';

// Importe la page de connexion
import { Connexion } from './features/authentification/connexion/connexion';

// Importe le guard de protection
import { authentificationGuard } from './core/guards/authentification-guard';

// Importe la liste des formations
import { ListeFormations } from './features/formations/liste-formations/liste-formations';

// Importe le composant du formulaire
import {
  FormulaireFormation
} from './features/formations/formulaire-formation/formulaire-formation';

// Importe le formulaire de modification
import {
  ModifierFormation
} from './features/formations/modifier-formation/modifier-formation';

// Importe le composant de gestion des documents
import {
  GestionDocuments
} from './features/documents-cours/gestion-documents/gestion-documents';




// Définit les URLs de l'application
export const routes: Routes = [
  {
    // Page accessible sans connexion
    path: 'connexion',
    component: Connexion
  },

  {
  // Page principale protégée par le guard
  path: 'tableau-de-bord',
  component: TableauDeBord,
  canActivate: [authentificationGuard]
},

{
  // Exemple : /modifier-formation/2
  path: 'modifier-formation/:id',

  // Composant affiché pour modifier la formation
  component: ModifierFormation,

  // Réserve la page à l'administrateur connecté
  canActivate: [authentificationGuard]
},



  {
    // Page formations protégée par le guard
    path: 'formations',
    component: ListeFormations,
    canActivate: [authentificationGuard]
  },

  {
  // Page de création d'une formation
  path: 'ajouter-formation',

  // Composant affiché sur cette page
  component: FormulaireFormation,

  // Page accessible uniquement à l'administrateur connecté
  canActivate: [authentificationGuard]
    },

  {
    // Redirection de l'accueil vers la connexion
    path: '',
    redirectTo: 'connexion',
    pathMatch: 'full'
  },
  {
  // Exemple d'URL : /formations/2/documents
  path: 'formations/:id/documents',

  // Affiche la page des documents de la formation
  component: GestionDocuments,

  // Autorise uniquement l'administrateur connecté
  canActivate: [authentificationGuard]
},
{
  path: 'chatbot',
  loadComponent: () => import('./features/chatbot/chatbot').then(m => m.ChatbotComponent)
},


  {
    // Toute URL inconnue revient à la connexion
    path: '**',
    redirectTo: 'connexion'
  }
];
