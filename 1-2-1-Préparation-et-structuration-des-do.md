# 1-2-1 Préparation et structuration des données importées

Une fois les données importées, elles sont rarement exploitables immédiatement. La phase de préparation, souvent appelée *Data Wrangling* ou *Data Cleaning*, consiste à transformer des données brutes en un format cohérent, propre et prêt pour l'analyse ou le stockage.

## Concept fondamental

La préparation des données vise à garantir la **qualité** et la **cohérence** du jeu de données. Elle repose sur la transformation des valeurs, la correction des anomalies et la mise en conformité avec le schéma cible.

### Cycle de vie de la préparation

```mermaid
graph LR
    A[Données Brutes] --> B(Nettoyage)
    B --> C(Normalisation)
    C --> D(Structuration)
    D --> E[Données Exploitables]
```

## Opérations clés de préparation

### 1. Nettoyage (Cleaning)
*   **Gestion des valeurs manquantes** : Suppression des lignes incomplètes ou imputation (remplacement par la moyenne, la médiane ou une valeur par défaut).
*   **Suppression des doublons** : Identification et élimination des enregistrements redondants.
*   **Correction des erreurs de saisie** : Standardisation des formats (ex: mettre tous les noms en majuscules, corriger les fautes de frappe).

### 2. Normalisation
*   **Conversion de types** : S'assurer que les dates sont au format `ISO 8601`, que les nombres sont typés comme `float` ou `int`, et non comme `string`.
*   **Mise à l'échelle** : Harmonisation des unités (ex: convertir toutes les devises en euros, toutes les distances en kilomètres).

### 3. Structuration
*   **Renommage des colonnes** : Utilisation de conventions explicites (ex: `snake_case` comme `date_inscription` au lieu de `Date Inscription`).
*   **Réorganisation** : Sélection des colonnes utiles et suppression des colonnes inutilisées pour optimiser la mémoire.

## Comparatif : Données Brutes vs Données Préparées

| Caractéristique | Données Brutes | Données Préparées |
| :--- | :--- | :--- |
| **Cohérence** | Faible (formats variés) | Haute (standardisé) |
| **Fiabilité** | Risque d'erreurs (doublons, nulls) | Validée (nettoyée) |
| **Usage** | Stockage temporaire | Analyse, Modélisation, BI |

## Exemple concret : Nettoyage avec Pandas

```python
import pandas as pd

# Chargement
df = pd.read_csv('ventes.csv')

# 1. Suppression des doublons
df = df.drop_duplicates()

# 2. Gestion des valeurs manquantes (remplacer par 0)
df['quantite'] = df['quantite'].fillna(0)

# 3. Conversion de type
df['date'] = pd.to_datetime(df['date'])

# 4. Standardisation des colonnes
df.columns = [c.lower().replace(' ', '_') for c in df.columns]
```

## Bonnes pratiques professionnelles

*   **Traçabilité (Audit Trail)** : Documentez chaque transformation effectuée. Si vous supprimez des données, gardez une trace du pourquoi et du combien.
*   **Approche itérative** : Ne tentez pas de tout nettoyer en une seule fois. Procédez par étapes : structure, puis types, puis valeurs.
*   **Validation par échantillonnage** : Après chaque transformation majeure, vérifiez un échantillon de données pour confirmer que le résultat correspond à vos attentes.
*   **Immuabilité** : Travaillez sur une copie du jeu de données original. Ne modifiez jamais la source brute.

## Erreurs fréquentes à éviter

*   **Suppression aveugle** : Supprimer systématiquement les lignes contenant des valeurs manquantes peut introduire un biais statistique important.
*   **Incohérence de format** : Mélanger des formats de date (ex: `JJ/MM/AAAA` et `AAAA-MM-JJ`) dans une même colonne.
*   **Oubli des valeurs aberrantes (Outliers)** : Ignorer des valeurs extrêmes qui pourraient être des erreurs de saisie (ex: un âge de 200 ans) ou des anomalies critiques.

## Points de vigilance

*   **Performance** : Sur de très gros volumes, les opérations de nettoyage peuvent être coûteuses en temps CPU. Utilisez des méthodes vectorisées plutôt que des boucles.
*   **Conformité (RGPD)** : Lors de la préparation, assurez-vous de supprimer ou d'anonymiser les données personnelles (PII - *Personally Identifiable Information*) si elles ne sont pas nécessaires à l'analyse.

## Sources

*   *ISO 8601 : Data elements and interchange formats – Information interchange – Representation of dates and times.*
*   *Pandas User Guide : Working with missing data.*