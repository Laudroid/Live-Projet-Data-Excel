# 2-1-2 Normalisation des données : casse, espaces, formats

La normalisation consiste à transformer des données textuelles et numériques pour qu'elles respectent une convention unique. Cette étape est indispensable pour permettre les jointures entre tables, le regroupement (*group by*) et la recherche efficace.

## Concepts fondamentaux

*   **Casse (Case)** : Uniformisation des majuscules et minuscules (ex: "Paris", "PARIS", "paris" deviennent "Paris").
*   **Espaces (Whitespace)** : Suppression des espaces inutiles en début, fin ou au milieu des chaînes de caractères.
*   **Formats** : Application d'un masque de saisie cohérent pour les données semi-structurées (téléphones, codes postaux, emails).

## Fonctionnement détaillé

La normalisation repose sur des fonctions de transformation de chaînes de caractères.

### Opérations de base
1.  **Trim** : Suppression des espaces superflus (ex: `"  valeur  "` -> `"valeur"`).
2.  **Casse** : Conversion en `lower` (minuscules), `upper` (majuscules) ou `title` (première lettre en majuscule).
3.  **Nettoyage de caractères** : Suppression de la ponctuation ou des caractères spéciaux non désirés.

### Exemple de transformation
| Donnée brute | Opération | Résultat |
| :--- | :--- | :--- |
| `"  FRANCE  "` | `strip()` | `"FRANCE"` |
| `"jean-pierre"` | `title()` | `"Jean-Pierre"` |
| `"01.23.45.67.89"` | `replace('.', '')` | `"0123456789"` |

## Cas d'usage professionnels

*   **Gestion de la relation client (CRM)** : Fusionner les doublons de clients saisis différemment ("Société X", "société x ", "SOCIETE X").
*   **Marketing** : Normaliser les adresses emails pour éviter les envois en double ou les erreurs de routage.
*   **E-commerce** : Standardiser les références produits pour permettre des recherches par mots-clés fiables.

## Exemple concret : Python (Pandas)

```python
import pandas as pd

# Nettoyage d'une colonne 'ville'
df['ville'] = df['ville'].str.strip()        # Supprime espaces
df['ville'] = df['ville'].str.capitalize()   # "PARIS" -> "Paris"

# Normalisation d'un numéro de téléphone
df['tel'] = df['tel'].str.replace(r'\D', '', regex=True) # Garde uniquement les chiffres
```

## Bonnes pratiques professionnelles

*   **Standardisation dès la saisie** : La meilleure normalisation est celle qui n'est pas nécessaire. Utilisez des listes déroulantes ou des masques de saisie dans vos interfaces utilisateurs.
*   **Utilisation de bibliothèques spécialisées** : Pour les adresses postales ou les noms de pays, utilisez des bibliothèques de référence (ex: `pycountry` ou des API de géocodage) plutôt que des expressions régulières manuelles.
*   **Conservation de l'original** : Si la donnée brute contient une information métier (ex: une note manuscrite), ne la normalisez pas de manière destructive. Créez une nouvelle colonne normalisée.

## Erreurs fréquentes à éviter

*   **Normalisation excessive** : Supprimer tous les espaces dans un nom composé (ex: "Saint Etienne" -> "SaintEtienne") peut rendre la donnée illisible pour l'utilisateur final.
*   **Gestion des accents** : Oublier de convertir les caractères accentués (ex: "é" -> "e") lors de la création de clés de recherche ou d'identifiants techniques.
*   **Casse uniforme sur les emails** : Les emails sont insensibles à la casse pour la partie domaine, mais peuvent être sensibles pour la partie locale. Normalisez toujours en minuscules pour éviter les doublons.

## Points de vigilance

*   **Performance** : Les opérations sur les chaînes de caractères (regex, remplacement) sont coûteuses sur des millions de lignes. Vectorisez vos opérations avec les méthodes `.str` de Pandas.
*   **Localisation** : Attention aux règles de casse spécifiques à certaines langues (ex: le "i" turc sans point).

## Sources

*   *Documentation Pandas : Working with text data.*
*   *RFC 5321 : Simple Mail Transfer Protocol (concernant la casse des emails).*