# Jeux de données et corrigés — formation data sur Excel

Document formateur. Il décrit ce qui a été produit pour accompagner les
douze énoncés existants, comment les fichiers s'articulent entre eux, et
ce qu'il faut savoir avant de les distribuer.

Les énoncés eux-mêmes n'ont pas été modifiés.

---

## 1. Un univers unique pour les douze exercices

Tous les fichiers décrivent la même entreprise fictive : **Atelier
Nordique**, distributeur retail français d'équipement de bureau et de
petit électroménager. Mêmes 33 produits, mêmes 12 magasins répartis sur
6 régions, mêmes 12 vendeurs, même calendrier 2023-2024.

Ce choix a une conséquence pédagogique directe : le jeu qu'un apprenant
nettoie au premier TP est celui qu'il analysera au quatrième. Les ordres
de grandeur qu'il mémorise restent valables d'une séance à l'autre, et
une incohérence de résultat entre deux TP signale une erreur de méthode
plutôt qu'un changement de contexte.

Le référentiel est décrit dans `referentiel.py` : catégories, prix de
vente et coûts d'achat, poids commercial de chaque région, amplitude de
saisonnalité par région, rattachement des vendeurs.

---

## 2. Correspondance énoncé / fichier de données

Les deux séries d'exercices sont numérotées 1 à 6 chacune. Les fichiers
sont donc rattachés ici au titre complet de l'énoncé, pas au seul numéro.

| Énoncé | Fichier de données | Volume |
|---|---|---|
| 1 — Importer et préparer un dataset réel | `ventes_brutes.csv` | 422 lignes, 14 colonnes |
| 1 — Assurer la qualité des données importées | `ventes_brutes.csv` (le même) | 422 lignes, 14 colonnes |
| 2 — Nettoyer un dataset complet | `clients_brut.xlsx` | 195 lignes, 9 colonnes |
| 2 — Créer des indicateurs dérivés | `Ventes_Projet.xlsx` | 600 lignes, 10 colonnes |
| 3 — Analyser les données avec des fonctions complexes | `Ventes.xlsx` + `Referentiel.xlsx` | 260 lignes / 33 produits + 12 magasins |
| 3 — Optimiser la robustesse des calculs | `Suivi_Marges.xlsx` | 33 références + 120 saisies |
| 4 — Explorer les données via les TCD | `Ventes_Globales.xlsx` | 1 200 lignes, 6 colonnes |
| 4 — Utiliser QUERY pour l'analyse structurée | `Data_Ventes.csv` | 320 lignes, 6 colonnes |
| 5 — Créer des visualisations pertinentes | `Ventes_Nettoyees.xlsx` | 820 lignes, 15 colonnes |
| 5 — Concevoir un dashboard | `Dashboard_Source.xlsx` | 906 lignes, 15 colonnes |
| 6 — Résoudre un problème data métier | `ventes_2023.csv` | 1 522 lignes, 9 colonnes |
| 6 — Présenter les résultats | aucun fichier propre | s'appuie sur les livrables du TP précédent |

Deux énoncés partagent `ventes_brutes.csv` : c'est cohérent avec leur
contenu, l'un porte sur l'import et l'exploration structurelle, l'autre
sur la normalisation et le traitement des erreurs. Rien n'empêche de les
enchaîner sur la même séance.

---

## 3. Ce qu'il faut savoir avant de distribuer

### `ventes_brutes.csv` est volontairement mal encodé

Le fichier est écrit en **UTF-8 sans BOM**. Ouvert par double-clic dans
un Excel français, il s'affiche en mojibake : `Électronique` devient
`Ã‰lectronique`. Ce n'est pas un défaut de fabrication, c'est le sujet de
l'étape 1 de l'énoncé « Assurer la qualité des données importées ».

Ne « corrigez » pas ce fichier avant de le distribuer, et ne l'ouvrez pas
pour l'enregistrer depuis Excel : la sauvegarde détruirait l'anomalie.

### Les montants utilisent un espace insécable

Dans ce même fichier, les montants à quatre chiffres et plus emploient
U+00A0 comme séparateur de milliers. C'est le piège le plus discriminant
de la série : `SUBSTITUE(A2;" ";"")` avec un espace ordinaire ne fonctionne
pas, il faut viser `CAR(160)`. Visuellement, l'apprenant ne voit aucune
différence entre les deux espaces.

### `Data_Ventes.csv` cible Google Sheets, pas Excel

`QUERY` est une fonction Google Sheets ; elle n'existe pas dans Excel. La
colonne `Montant` est en euros entiers, sans décimale : un CSV à
séparateur virgule contenant des décimales pointées s'importe en texte
dans un classeur configuré en locale française, et les `SUM()`
renverraient silencieusement zéro.

### Trois fichiers sont livrés en plage simple, pas en tableau structuré

`Ventes_Globales.xlsx` et `Dashboard_Source.xlsx` sont des plages
ordinaires : leurs énoncés demandent explicitement à l'apprenant de faire
`Ctrl+T`. Les autres classeurs contiennent de vrais tableaux structurés,
nommés `Ventes`, `Clients`, `Produits`, `Magasins`, `Catalogue`,
`Saisies` et `DonneesNettoyees`.

### `Suivi_Marges.xlsx` ne contient aucune formule

Les trois colonnes intitulées « (à compléter) » sont vides, et l'onglet
`Recherche` ne comporte que les libellés et la cellule de saisie. C'est le
travail demandé. L'onglet `Recherche` documente trois codes de test : un
cas nominal, un produit dont le prix de vente vaut 0 (donc `#DIV/0!`) et
un code absent du catalogue (donc `#N/A`).

### Deux colonnes ont été ajoutées à `ventes_2023.csv`

L'énoncé liste `Date`, `ID_Produit`, `Catégorie`, `Vendeur`, `Quantité`,
`Prix_Unitaire` et `Région`. Le fichier livré contient en plus
`Cout_Unitaire`, sans lequel la question Q2 sur la marge brute serait
insoluble, et `Produit`, qui rend le top 3 lisible sans jointure.

### Q3 de l'énoncé « Résoudre un problème data métier » est un piège

Chaque vendeur n'opère que sur une seule région : la corrélation demandée
entre performance des vendeurs et régions est structurellement
impossible à mesurer, les deux variables sont confondues. C'est
intentionnel et le corrigé le traite. Un apprenant qui produit un
classement de CA par vendeur et en déduit une performance individuelle
est tombé dans le piège.

---

## 4. Les corrigés

Un fichier par énoncé, dans `corriges/`, jamais distribué aux apprenants.
Chacun suit la même structure : ce que l'exercice évalue réellement,
corrigé pas à pas, valeurs de contrôle, erreurs fréquentes, volet IA,
barème sur 20, prolongements.

`corriges/valeurs-de-reference.md` regroupe toutes les valeurs numériques
attendues, exercice par exercice, recalculées directement depuis les
fichiers livrés. C'est l'outil de correction rapide : un écart de CA
signale précisément quelle étape de nettoyage a été sautée.

---

## 5. Regénérer ou faire varier les jeux

Les scripts sont déterministes : la graine est fixée dans
`referentiel.py` (`SEED`). Relancer produit exactement les mêmes fichiers.

```
python3 -m gen_01_brutes        # ventes_brutes.csv
python3 -m gen_02_clients       # clients_brut.xlsx
python3 -m gen_03_projet        # Ventes_Projet.xlsx
python3 -m gen_04_ventes_ref    # Ventes.xlsx + Referentiel.xlsx
python3 -m gen_05_marges        # Suivi_Marges.xlsx
python3 -m gen_06_globales      # Ventes_Globales.xlsx
python3 -m gen_07_query         # Data_Ventes.csv
python3 -m gen_08_viz           # Ventes_Nettoyees.xlsx
python3 -m gen_09_dashboard     # Dashboard_Source.xlsx
python3 -m gen_10_ventes2023    # ventes_2023.csv
python3 verifier_donnees.py     # contrôles + valeurs de référence
```

Dépendances : `openpyxl` pour la génération, `pandas` pour la
vérification.

**Pour changer de promotion**, modifiez `SEED` dans `referentiel.py`,
relancez les dix générateurs puis `verifier_donnees.py`. Les anomalies
restent en nombre identique, mais elles changent de lignes et les valeurs
de référence sont recalculées automatiquement : les corrigés doivent
alors être relus sur leurs chiffres, pas sur leur méthode.

`verifier_donnees.py` contrôle notamment que les filtres des énoncés
renvoient des résultats non vides — le filtre à trois critères du TP
QUERY, le seuil `HAVING SUM(E) > 1000`, le comptage des transactions de
plus de 10 unités. Si vous changez la graine, exécutez-le : il échouera
bruyamment si un filtre devient stérile.

---

## 6. Suggestion : ajouter un livrable `USAGE-IA.md`

Les douze énoncés encouragent l'usage de l'IA et demandent, de façon
variable, de commenter les formules obtenues ou de recopier le prompt
utilisé. Cette exigence gagnerait à être homogène et explicitement
livrable, sous la forme d'un fichier `USAGE-IA.md` joint au rendu et
consignant :

* quand et pourquoi l'IA a été sollicitée, à quelle étape ;
* les réponses écartées, avec le motif du rejet ;
* les corrections apportées à une proposition retenue.

Ce livrable rend le volet IA évaluable au lieu de déclaratif, et la
section « Volet IA » de chaque corrigé fournit la question de
vérification orale correspondante. L'ajout se fait en une ligne dans la
rubrique « Livrables attendus » de chaque énoncé.
