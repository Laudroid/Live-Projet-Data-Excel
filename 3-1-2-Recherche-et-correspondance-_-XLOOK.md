# 3-1-2 Recherche et correspondance : XLOOKUP, VLOOKUP

La recherche de données consiste à extraire une valeur dans une table de référence en fonction d'une clé commune. C'est l'opération de base pour enrichir des jeux de données (ex: ajouter le nom d'un client à partir de son ID).

## Concepts fondamentaux

*   **VLOOKUP (RechercheV)** : Fonction historique qui cherche une valeur dans la première colonne d'une plage et renvoie une valeur dans la même ligne, à partir d'une colonne spécifiée.
*   **XLOOKUP (RechercheX)** : Fonction moderne, plus flexible, qui remplace avantageusement `VLOOKUP` et `INDEX/MATCH`.

## Fonctionnement détaillé

### 1. VLOOKUP (La méthode classique)
`=VLOOKUP(valeur_cherchée; table_matrice; no_index_col; [valeur_proche])`
*   **Contrainte** : La clé de recherche doit impérativement se trouver dans la première colonne de la plage sélectionnée.

### 2. XLOOKUP (La méthode moderne)
`=XLOOKUP(valeur_cherchée; matrice_recherche; matrice_retour; [si_non_trouvé])`
*   **Avantage** : La recherche peut se faire dans n'importe quelle colonne. Elle ne nécessite pas de tri préalable et gère nativement les erreurs.

## Comparatif : VLOOKUP vs XLOOKUP

| Caractéristique | VLOOKUP | XLOOKUP |
| :--- | :--- | :--- |
| **Direction de recherche** | Gauche vers droite uniquement | Toutes directions |
| **Gestion des erreurs** | Nécessite `IFERROR` | Argument intégré |
| **Stabilité** | Fragile (si insertion de colonne) | Robuste |
| **Recherche approximative** | Par défaut (dangereux) | Exacte par défaut (sécurisé) |

## Cas d'usage professionnels

*   **Enrichissement de données** : Ajouter des informations de produits (prix, catégorie) à une liste de commandes en utilisant le `Code Produit` comme clé.
*   **Consolidation** : Fusionner des données provenant de deux fichiers différents (ex: fichier RH et fichier de paie).
*   **Recherche de correspondance** : Identifier le responsable d'un projet à partir d'un code département.

## Exemple concret

Imaginons une table `Produits` (A: ID, B: Nom, C: Prix).

```excel
-- Avec VLOOKUP (Risqué si on insère une colonne)
=VLOOKUP("P001"; A2:C100; 3; FALSE)

-- Avec XLOOKUP (Recommandé)
=XLOOKUP("P001"; A2:A100; C2:C100; "Non trouvé")
```

## Diagramme de recherche

```mermaid
graph LR
    A[Clé de recherche] --> B{Table de référence}
    B -->|Trouvé| C[Valeur retournée]
    B -->|Non trouvé| D[Valeur par défaut / Erreur]
```

## Bonnes pratiques professionnelles

*   **Privilégier XLOOKUP** : Si votre version de logiciel le permet (Excel 365, Excel 2021+, Google Sheets), utilisez systématiquement `XLOOKUP`.
*   **Verrouillage des plages** : Utilisez des références absolues (ex: `$A$2:$C$100`) pour éviter que la plage de recherche ne se décale lors de la recopie de la formule.
*   **Recherche exacte** : Forcez toujours la correspondance exacte (`FALSE` ou `0` pour `VLOOKUP`) pour éviter des résultats erronés sur des données non triées.

## Erreurs fréquentes à éviter

*   **Format de données incohérent** : Chercher un nombre stocké en texte (ex: "101") dans une colonne de nombres (ex: 101). La recherche échouera.
*   **Espaces invisibles** : Une clé de recherche contenant un espace de fin (ex: "ID01 ") ne sera pas trouvée si la table de référence contient "ID01". Utilisez `TRIM` au préalable.
*   **Plages dynamiques** : Utiliser des références de colonnes entières (ex: `A:C`) peut ralentir le calcul sur des fichiers très lourds.

## Points de vigilance

*   **Doublons** : `VLOOKUP` et `XLOOKUP` renvoient toujours la **première** occurrence trouvée. Si votre clé n'est pas unique, vous risquez d'extraire une donnée incorrecte sans avertissement.
*   **Performance** : Sur des millions de lignes, ces fonctions deviennent coûteuses. Dans ce cas, préférez une base de données (SQL) ou Power Query pour réaliser des jointures.

## Sources

*   *Documentation Microsoft Support : Fonction XLOOKUP.*
*   *Documentation Google Sheets : Fonction RECHERCHEX.*