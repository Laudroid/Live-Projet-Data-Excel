# 4-1-1 Tableaux croisés dynamiques (TCD) : création et manipulation

Le Tableau Croisé Dynamique (TCD) est l'outil de synthèse par excellence. Il permet de transformer des listes de données brutes en rapports structurés, sans écrire de formules complexes.

## Concepts fondamentaux

*   **Source de données** : Tableau source structuré en colonnes (avec en-têtes).
*   **Zone de lignes/colonnes** : Définit les catégories d'analyse (ex: Date, Région, Catégorie).
*   **Zone de valeurs** : Définit les calculs à effectuer (Somme, Moyenne, Nombre).
*   **Zone de filtres** : Permet de restreindre l'affichage global du rapport.

## Fonctionnement détaillé

Le TCD repose sur le regroupement et l'agrégation des données.

1.  **Sélection** : Sélectionner la plage de données source.
2.  **Insertion** : Créer le TCD (via le menu Insertion > Tableau croisé dynamique).
3.  **Configuration** : Glisser-déposer les champs dans les zones (Lignes, Colonnes, Valeurs).
4.  **Actualisation** : Le TCD ne se met pas à jour automatiquement si la source change ; il nécessite une action manuelle (clic droit > Actualiser).

## Structure d'un TCD

| Zone | Rôle |
| :--- | :--- |
| **Lignes** | Affiche les éléments en vertical. |
| **Colonnes** | Affiche les éléments en horizontal. |
| **Valeurs** | Effectue les calculs (Somme, NB, etc.). |
| **Filtres** | Filtre l'ensemble du rapport. |

## Cas d'usage professionnels

*   **Analyse des ventes** : Chiffre d'affaires par produit et par mois.
*   **Gestion des ressources** : Nombre de tickets de support traités par technicien.
*   **Audit financier** : Comparaison des dépenses réelles par rapport au budget par département.

## Diagramme de flux

```mermaid
graph LR
    A[Données Brutes] --> B[Moteur TCD]
    B --> C{Configuration}
    C -->|Lignes/Colonnes| D[Structure]
    C -->|Valeurs| E[Calculs]
    D & E --> F[Rapport Synthétique]
```

## Bonnes pratiques professionnelles

*   **Utiliser des Tableaux (ListObjects)** : Transformez votre source de données en "Tableau" (Ctrl+L ou Ctrl+T). Ainsi, le TCD s'étendra automatiquement lors de l'ajout de nouvelles lignes.
*   **Nommer les champs** : Assurez-vous que chaque colonne de votre source possède un en-tête clair et unique.
*   **Nettoyage des données** : Un TCD est aussi performant que sa source. Supprimez les lignes vides, les colonnes inutiles et harmonisez les formats (ex: dates, nombres).

## Erreurs fréquentes à éviter

*   **Données sources non contiguës** : Ne laissez jamais de lignes ou colonnes vides dans votre source de données.
*   **Format de nombre incohérent** : Si une colonne contient des nombres et du texte, le TCD risque de compter les éléments au lieu de les sommer.
*   **Oubli d'actualisation** : Croire que le rapport est à jour alors que la source a été modifiée.

## Points de vigilance

*   **Performance** : Sur des millions de lignes, le TCD peut devenir lent. Utilisez alors Power Pivot ou Power Query pour traiter les données en amont.
*   **Doublons** : Le TCD additionne tout ce qu'il trouve. Si votre source contient des doublons, vos résultats seront erronés.
*   **Regroupement de dates** : Par défaut, les tableurs regroupent souvent les dates par mois/trimestre/année. Apprenez à dissocier ces groupes pour retrouver vos dates brutes si nécessaire.

## Sources

*   *Documentation Microsoft Support : Créer un tableau croisé dynamique.*
*   *Documentation Google Sheets : Créer et utiliser des tableaux croisés dynamiques.*