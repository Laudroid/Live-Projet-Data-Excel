# 2-2-1 Fonctions de manipulation textuelle

La manipulation textuelle est une compétence fondamentale pour structurer des données non formatées. Ces fonctions permettent de nettoyer, fusionner ou transformer des chaînes de caractères pour les rendre exploitables par des systèmes tiers ou des outils d'analyse.

## Concepts fondamentaux

Ces fonctions sont présentes dans la quasi-totalité des langages de programmation (Python, SQL, outils de BI, tableurs). Bien que la syntaxe puisse varier, la logique reste identique.

### Fonctions de transformation et nettoyage

| Fonction | Rôle | Exemple |
| :--- | :--- | :--- |
| **TRIM** | Supprime les espaces inutiles (début/fin). | `"  Data  "` -> `"Data"` |
| **UPPER** | Convertit en majuscules. | `"data"` -> `"DATA"` |
| **LOWER** | Convertit en minuscules. | `"DATA"` -> `"data"` |
| **SUBSTITUTE** | Remplace une sous-chaîne par une autre. | `"2023-01"` -> `"2023/01"` |
| **CONCAT** | Fusionne plusieurs chaînes. | `"Jean" + " " + "Dupont"` -> `"Jean Dupont"` |

## Fonctionnement détaillé

### 1. Nettoyage (TRIM)
Le `TRIM` est la première étape de toute chaîne de traitement. Il élimine les caractères invisibles qui empêchent souvent les jointures de bases de données (ex: une clé primaire `"ID01"` ne correspondra pas à `"ID01 "`).

### 2. Transformation de casse (UPPER/LOWER)
Ces fonctions permettent d'homogénéiser des entrées utilisateur. Elles sont systématiquement utilisées avant une comparaison ou un regroupement pour éviter que `"Paris"` et `"paris"` ne soient traités comme deux entités distinctes.

### 3. Remplacement (SUBSTITUTE)
Le `SUBSTITUTE` (ou `REPLACE` selon les langages) permet de corriger des formats.
*   *Usage courant* : Remplacer les virgules par des points dans les nombres décimaux importés de fichiers CSV européens.

### 4. Fusion (CONCAT)
La concaténation permet de reconstruire des identifiants uniques ou des libellés complets à partir de colonnes séparées (ex: `Prénom` + `Nom` = `Nom Complet`).

## Exemple concret : Automatisation en SQL

```sql
-- Nettoyage et création d'un identifiant unique
SELECT 
    UPPER(TRIM(nom)) AS nom_propre,
    CONCAT(LOWER(prenom), '.', LOWER(nom)) AS email_provisoire,
    SUBSTITUTE(date_format, '-', '/') AS date_standard
FROM utilisateurs;
```

## Bonnes pratiques professionnelles

*   **Enchaînement des fonctions** : Combinez les fonctions pour un nettoyage complet.
    *   *Exemple* : `UPPER(TRIM(valeur))` garantit une donnée propre et normalisée.
*   **Gestion des valeurs nulles** : La plupart des fonctions de manipulation textuelle retournent `NULL` si l'entrée est `NULL`. Prévoyez une gestion des valeurs par défaut (ex: `COALESCE` en SQL ou `.fillna('')` en Python).
*   **Lisibilité** : Si vous enchaînez plus de trois fonctions, créez des étapes intermédiaires ou des colonnes calculées pour faciliter le débogage.

## Erreurs fréquentes à éviter

*   **Concaténation sans séparateur** : Oublier d'ajouter un espace ou un caractère de séparation lors de la fusion de deux champs (ex: `"Jean"+"Dupont"` devient `"JeanDupont"`).
*   **Remplacement partiel** : Utiliser `SUBSTITUTE` sans vérifier si la chaîne cible n'apparaît pas ailleurs dans le texte (risque de remplacer des caractères par erreur).
*   **Confusion entre TRIM et REPLACE** : `TRIM` ne supprime que les espaces aux extrémités. Pour supprimer les espaces au milieu d'une chaîne, utilisez `REPLACE` ou `SUBSTITUTE`.

## Points de vigilance

*   **Performance** : Sur des tables contenant des millions de lignes, l'application de fonctions textuelles sur chaque ligne peut ralentir considérablement les requêtes. Privilégiez, si possible, le nettoyage lors de l'ingestion (ETL) plutôt qu'à chaque lecture.
*   **Encodage** : Assurez-vous que les fonctions gèrent correctement les caractères accentués, sous peine de voir des caractères corrompus après transformation.

## Sources

*   *Documentation SQL standard (ISO/IEC 9075).*
*   *Documentation Python : String Methods.*