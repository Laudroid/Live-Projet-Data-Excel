# Corrigé — Création d'indicateurs temporels pour l'analyse de données

**Fichier(s) de données :** `Ventes_Projet.xlsx` (600 lignes, 10 colonnes) — tableau structuré nommé `Ventes`
**Durée indicative :** 45 min
**Prérequis :** Fonctions de date (`ANNEE`, `MOIS`, `TEXTE`), notion de tableau structuré Excel, insertion d'un TCD de base

---

## 1. Ce que l'exercice évalue réellement

L'exercice mesure la capacité à enrichir un tableau avec des colonnes temporelles dérivées, et surtout à identifier le piège du tri alphabétique dans un TCD. La clé `TEXTE(...;"mmm-aaaa")` est une chaîne de texte : triée alphabétiquement, elle place `avr.-2023` avant `janv.-2023` et mélange les deux années. Comme la plage couvre exactement 24 mois (2023–2024), ce problème est immédiatement visible dans les données et ne peut pas passer inaperçu si le TCD est construit correctement. La colonne d'index `ANNEE*100+MOIS` est la solution attendue pour forcer un tri chronologique.

---

## 2. Corrigé pas à pas

### Étape 1 — Préparation du jeu de données

Ouvrir `Ventes_Projet.xlsx`. Le fichier contient un tableau structuré nommé `Ventes` sur l'onglet `Ventes`, avec 600 lignes de données et les colonnes suivantes :

`ID_Vente` | `Date_Vente` | `ID_Produit` | `Produit` | `Categorie` | `Region` | `Vendeur` | `Quantite` | `Prix_Unitaire` | `Chiffre_Affaires`

Aucune colonne temporelle dérivée n'est présente : c'est entièrement le travail de l'apprenant.

**Vérification du format de date :** sélectionner une cellule de la colonne `Date_Vente` et vérifier dans la barre de formule qu'Excel l'affiche comme une date (pas comme un nombre ou un texte). Si la cellule affiche un entier à 5 chiffres, appliquer le format `JJ/MM/AAAA` via **Accueil > Format de cellule > Date**. Si la cellule affiche du texte aligné à gauche, utiliser `DATEVAL` (DATEVALUE) pour convertir.

---

### Étape 2 — Création des quatre colonnes calculées

Les colonnes s'ajoutent à l'intérieur du tableau structuré : cliquer dans la cellule à droite de la dernière colonne et saisir l'en-tête. Excel étend automatiquement le tableau.

#### 2a. Colonne « Année »

```
=ANNEE([@Date_Vente])
```

`ANNEE` (YEAR) extrait l'année sous forme d'entier (2023 ou 2024 sur ce jeu de données).

#### 2b. Colonne « Mois »

```
=MOIS([@Date_Vente])
```

`MOIS` (MONTH) extrait le numéro du mois (1 à 12). Cette colonne numérique sert de base à la clé de tri de l'étape suivante.

#### 2c. Colonne « Nom du Mois »

```
=TEXTE([@Date_Vente];"mmmm")
```

`TEXTE` (TEXT) formate la date en nom de mois complet selon la langue du système (`"janvier"`, `"février"`, etc.). Le code `"mmmm"` (4 m) donne le nom complet ; `"mmm"` (3 m) donne l'abréviation.

Cette colonne est uniquement illustrative — elle ne sert pas au tri du TCD.

#### 2d. Colonne « Mois-Année »

```
=TEXTE([@Date_Vente];"mmm-aaaa")
```

Cette formule produit des chaînes comme `"janv.-2023"` ou `"avr.-2024"`. C'est la clé affichée dans le TCD.

**Attention — piège central du TP :** cette valeur est du texte, pas une date. Excel la triera alphabétiquement si elle est placée en lignes du TCD sans précaution. Le tri alphabétique sur `mmm-aaaa` donne :

```
avr.-2023   ← avant janv.-2023 (« a » < « j »)
avr.-2024
août-2023
août-2024
déc.-2023
...
```

Les deux années sont mélangées et l'ordre chronologique est perdu. C'est exactement ce que le jeu de données à 24 mois rend visible.

#### 2e. Colonne « Index_Tri » (indispensable pour le TCD)

```
=[@Année]*100+[@Mois]
```

Produit un entier de la forme `202301`, `202302`, …, `202412`. Trié de manière croissante, cet index garantit l'ordre chronologique, même sur deux années. Cette colonne est à placer en valeur auxiliaire dans le TCD (voir étape 3).

---

### Étape 3 — Tableau croisé dynamique

#### Insertion

Cliquer dans le tableau `Ventes` > **Insertion > Tableau croisé dynamique > Nouvelle feuille de calcul**.

#### Configuration

- **Lignes :** `Mois-Année` (la clé textuelle pour l'affichage)
- **Valeurs :** `Chiffre_Affaires` (somme)
- Ne pas encore trier.

#### Forcer le tri chronologique

Sans la colonne d'index, le TCD trie `Mois-Année` alphabétiquement. Pour corriger :

1. Ajouter `Index_Tri` également en **Lignes** (sous `Mois-Année`).
2. Faire un clic droit sur n'importe quelle valeur `Index_Tri` dans le TCD > **Trier > Du plus petit au plus grand**. Le TCD se réordonne chronologiquement.
3. Pour masquer la colonne `Index_Tri` dans le rendu : clic droit sur le champ `Index_Tri` dans la liste des champs > **Paramètres de champ** > activer l'option **Masquer les éléments sans données** ; ou simplement laisser le champ visible — le barème ne pénalise pas son affichage tant que l'ordre est correct.

**Alternative moderne (Excel 365 / 2019+) :** Grouper directement le champ `Date_Vente` dans le TCD sans colonne dérivée. Clic droit sur une date dans le TCD > **Grouper** > sélectionner `Mois` et `Années`. Excel crée automatiquement les niveaux hiérarchiques avec tri chronologique intégré. Cette solution est plus robuste et ne dépend pas de la colonne `Mois-Année` textuelle. Elle n'est pas attendue au barème principal (l'énoncé impose les colonnes calculées), mais elle est recevable en prolongement et peut être signalée à l'oral.

---

### Réponse à la question finale de l'énoncé

**Intérêt de la colonne « Mois-Année » plutôt que du seul nom de mois :**

Sur une plage de 24 mois (2023–2024), la colonne `Nom du Mois` seule (`"janvier"`, `"février"`, etc.) agrège dans le TCD `janvier 2023` et `janvier 2024` dans la même ligne, produisant un total de 22 207,90 € (12 574,60 + 9 633,30 €) au lieu de deux valeurs distinctes. L'analyse temporelle est impossible : on perd toute visibilité sur la tendance d'une année à l'autre.

La colonne `Mois-Année` (`"janv.-2023"`, `"janv.-2024"`) crée 24 clés distinctes, une par mois calendaire, et permet de lire la progression mois par mois sur les deux années, y compris la légère baisse de -0,87 % de 2024 par rapport à 2023.

---

## 3. Valeurs de contrôle

| Contrôle | Valeur attendue |
|---|---|
| Lignes | 600 |
| Colonnes fournies | 10 |
| Tableau structuré | oui, nommé `Ventes` |
| Plage | 01/01/2023 au 31/12/2024 |
| Mois distincts | 24 |
| CA total | 274 527,30 € |
| CA 2023 | 137 863,10 € |
| CA 2024 | 136 664,20 € |
| Croissance 2024 vs 2023 | -0,87 % |
| Mois le plus performant | déc.-2023 avec 17 007,50 € |

CA mensuel attendu dans le TCD (ordre chronologique, après tri par `Index_Tri`) :

| Mois-Année | Index_Tri | CA |
|---|---|---|
| janv.-2023 | 202301 | 12 574,60 € |
| févr.-2023 | 202302 | 9 669,10 € |
| mars-2023 | 202303 | 9 791,10 € |
| avr.-2023 | 202304 | 10 235,20 € |
| mai-2023 | 202305 | 6 231,30 € |
| juin-2023 | 202306 | 10 707,00 € |
| juil.-2023 | 202307 | 9 610,90 € |
| août-2023 | 202308 | 11 578,10 € |
| sept.-2023 | 202309 | 13 521,20 € |
| oct.-2023 | 202310 | 13 175,20 € |
| nov.-2023 | 202311 | 13 761,90 € |
| déc.-2023 | 202312 | 17 007,50 € |
| janv.-2024 | 202401 | 9 633,30 € |
| févr.-2024 | 202402 | 8 335,90 € |
| mars-2024 | 202403 | 8 542,30 € |
| avr.-2024 | 202404 | 14 545,60 € |
| mai-2024 | 202405 | 10 072,70 € |
| juin-2024 | 202406 | 9 332,10 € |
| juil.-2024 | 202407 | 11 638,60 € |
| août-2024 | 202408 | 13 278,20 € |
| sept.-2024 | 202409 | 10 803,30 € |
| oct.-2024 | 202410 | 13 804,20 € |
| nov.-2024 | 202411 | 13 621,30 € |
| déc.-2024 | 202412 | 13 056,70 € |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| TCD commence par `avr.-2023` ou `août-2023` | `Mois-Année` trié alphabétiquement, sans colonne d'index | Regarder la première ligne du TCD : doit être `janv.-2023` |
| `janv.-2023` et `janv.-2024` fusionnés dans la même ligne du TCD | Champ `Nom du Mois` utilisé en lignes à la place de `Mois-Année` | Compter les lignes du TCD : doit avoir 24 lignes de données, pas 12 |
| CA total du TCD différent de 274 527,30 € | Une colonne calculée a écrasé `Chiffre_Affaires` ou la somme porte sur `Prix_Unitaire` | Sélectionner `Chiffre_Affaires` dans Valeurs du TCD et vérifier l'agrégation |
| Colonne `Année` contient 45292 (entier de date) | Utilisation de `TEXTE([@Date_Vente];"aaaa")` au lieu de `ANNEE([@Date_Vente])` | La colonne `Année` doit contenir 2023 ou 2024, pas un nombre à 5 chiffres |
| Colonne `Mois-Année` affiche `janv.-24` | Code de format `"mmm-aa"` (2 chiffres d'année) au lieu de `"mmm-aaaa"` | Cliquer sur une cellule et lire la formule : doit contenir `"mmm-aaaa"` |
| `Index_Tri` calculé sans les colonnes intermédiaires | `ANNEE([@Date_Vente])*100+MOIS([@Date_Vente])` — formule correcte mais colonnes `Année` et `Mois` absentes | Acceptable techniquement ; noter que les colonnes `Année` et `Mois` séparées sont demandées par l'énoncé |
| La colonne `Nom du Mois` affiche des majuscules (`Janvier`) | Paramètre régional du système en anglais ou code de format incorrect | Vérifier avec `TEXTE(DATE(2023;1;1);"mmmm")` dans une cellule vide |

---

## 5. Volet IA

**Ce qu'on attend dans le livrable :** l'apprenant qui a utilisé l'IA doit expliquer pourquoi `ANNEE([@Date_Vente])` renvoie un entier et non une chaîne, et pourquoi cela rend cette colonne utilisable dans le calcul de l'index (`ANNEE*100+MOIS`). Il doit aussi montrer qu'il a testé le tri du TCD avant et après ajout de la colonne d'index.

**Ce qui distingue un apprenant qui a compris :** il identifie spontanément le problème du tri alphabétique de `mmm-aaaa`, cite un exemple concret (`avr.-2023` avant `janv.-2023`), et explique pourquoi la formule `ANNEE*100+MOIS` résout le problème sans en créer d'autres.

**Question de vérification orale (soutenance) :** « Votre TCD affiche `avr.-2023` à la quatrième ligne. Comment expliquez-vous que ce mois ne soit pas en tête, et quelle manipulation avez-vous faite pour le remettre dans l'ordre ? Si vous aviez une troisième année de données (2025), votre formule d'index fonctionnerait-elle encore ? »

---

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Colonne `Année` correcte | 2 | Valeur 2023 ou 2024 pour chaque ligne, type numérique |
| Colonne `Mois` correcte | 2 | Valeur 1 à 12 pour chaque ligne, type numérique |
| Colonne `Nom du Mois` correcte | 1 | `"janvier"` pour les lignes de janvier (minuscule, nom complet) |
| Colonne `Mois-Année` au format `mmm-aaaa` | 2 | `"janv.-2023"` pour la première ligne du tableau |
| Colonne d'index `ANNEE*100+MOIS` présente | 2 | Valeur 202301 pour janvier 2023 |
| TCD avec `Mois-Année` en lignes et somme de `Chiffre_Affaires` | 3 | TCD présent, somme totale = 274 527,30 € |
| TCD trié chronologiquement (janv.-2023 en tête) | 3 | Première ligne du TCD = `janv.-2023` / 12 574,60 € |
| Explication sur l'intérêt de `Mois-Année` vs nom de mois seul | 3 | Au moins deux phrases expliquant la fusion des mois sur 24 mois et la perte de la distinction inter-annuelle |
| Qualité du prompt IA commenté (si utilisé) | 2 | Prompt lisible, explication en propres mots de chaque argument de formule |

**Total : 20 points**

Note : si la colonne d'index est absente mais le TCD est trié correctement par un autre moyen (groupement de dates natif), 1 point sur 2 accordé pour le critère d'index, et les 3 points de tri chronologique sont maintenus.

---

## 7. Prolongements

Pour les apprenants rapides, trois pistes d'approfondissement :

1. **Groupement natif du TCD sur les dates :** explorer l'option **Clic droit > Grouper** directement sur le champ `Date_Vente` dans le TCD pour créer une hiérarchie Année / Trimestre / Mois sans aucune colonne calculée, et comparer les résultats avec l'approche par formules.

2. **Format de nombre personnalisé sur une vraie date :** plutôt que de convertir la date en texte avec `TEXTE`, conserver une colonne de type date et appliquer le format d'affichage `mmm-aaaa` via **Format de cellule > Personnalisé**. La colonne reste tritable chronologiquement comme une date, sans formule d'index.

3. **Calcul de la croissance mensuelle glissante :** ajouter une colonne qui compare le CA de chaque mois au même mois de l'année précédente, à l'aide de `SOMME.SI.ENS` (SUMIFS) sur `Chiffre_Affaires` avec critère `Annee-1` et `Mois` correspondant, pour matérialiser la croissance de -0,87 % à l'échelle mensuelle.
