// Représente une formation reçue depuis l'API Flask
export interface Formation {
  // Identifiant unique de la formation
  id: number;

  // Titre obligatoire
  titre: string;

  // Description de la formation
  description?: string;

  // Catégorie de la formation
  categorie?: string;

  // Durée de la formation
  duree?: string;

  // Niveau : débutant, intermédiaire ou avancé
  niveau?: string;

  // Statut de la formation
  statut: string;

  // Dates créées par Flask
  created_at?: string;
  updated_at?: string;
}
