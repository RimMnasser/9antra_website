// Représente un document reçu depuis l'API Flask
export interface DocumentCours {
  // Identifiant du document
  id: number;

  // Nom du fichier
  nom_fichier: string;

  // Chemin du fichier sur le serveur
  chemin_fichier: string;

  // Type du fichier : pdf, docx, etc.
  type_fichier?: string;

  // Taille du fichier en octets
  taille?: number;

  // Identifiant de la formation associée
  formation_id: number;

  // Date d'importation
  created_at?: string;
}
