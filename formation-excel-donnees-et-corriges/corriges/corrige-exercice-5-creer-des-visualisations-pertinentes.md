# Corrigé — Visualisation de données et mise en évidence de patterns

**Fichier(s) de données :** `Ventes_Nettoyees.xlsx` (820 lignes, 15 colonnes)
**Prérequis :** Savoir insérer un tableau structuré et un TCD ; avoir réalisé les TP de nettoyage et de dérivation de colonnes (Exercices A1 à A4) ; connaître les types de graphiques de base d'Excel.

---

## 1. Ce que l'exercice évalue réellement

L'exercice teste la capacité à lire un jeu de données pour en extraire un message, puis à choisir le type de graphique qui transmet ce message sans l'altérer. Le piège central est l'invention de patterns : le tableau structuré `DonneesNettoyees` contient exactement trois structures lisibles et chiffrables (saisonnalité par catégorie, écart régional de CA, corrélation prix/quantité) ; un quatrième pattern annoncé sans valeur à l'appui dans les données révèle une lecture superficielle ou un résultat d'IA non vérifié sur les vraies colonnes.

## 2. Corrigé pas à pas

### Étape 1 — Sélection des indicateurs

Le fichier est livré avec un tableau structuré nommé `DonneesNettoyees`, 820 lignes, 0 valeur manquante. Colonnes disponibles : `ID_Vente`, `Date`, `Année`, `Mois`, `Nom_Mois`, `Mois_Année`, `Catégorie`, `Produit`, `Région`, `Vendeur`, `Quantité`, `Prix_Unitaire`, `Chiffre_Affaires`, `Marge`, `Taux_Marge`. Les colonnes temporelles (`Année`, `Mois`, `Nom_Mois`, `Mois_Année`) sont déjà dérivées : l'apprenant n'a pas à les recréer.

**Pattern 1 — Saisonnalité par catégorie**

Construire un TCD : champ `Catégorie` en colonnes, champ `Mois` (valeur numérique 1–12, pour garantir le tri chronologique) en lignes, `Chiffre_Affaires` en valeurs (Somme). Lire la table résultante :

- Papeterie : pics en août (7 182,80 €) et septembre (6 912,40 €) — pic de rentrée scolaire confirmé.
- Électronique : pics en novembre (12 363,00 €) et décembre (11 534,60 €) — pic de fin d'année.
- Téléphonie : pic en décembre (9 858,20 €) — aligné sur l'électronique.
- Électroménager : pics en juin (8 786,60 €), juillet (8 789,30 €) et août (13 375,50 €) — pic estival.
- Mobilier : pas de pic saisonnier marqué, comportement relativement plat.

Si l'apprenant utilise `Nom_Mois` (texte) à la place de `Mois` (entier) sans configurer un ordre de tri manuel, l'axe X sera alphabétique (août avant avril) : c'est une erreur détectable en 5 secondes en lisant les deux premières valeurs de l'axe.

**Pattern 2 — Écart de CA entre régions**

Construire un TCD : `Région` en lignes, `Chiffre_Affaires` en valeurs (Somme), tri décroissant. Valeurs attendues sur 820 lignes : Île-de-France 93 302,60 €, Sud 69 435,60 €, Nord 57 346,50 €, Est 47 576,30 €, Ouest 46 085,50 €, Centre 45 172,10 €. L'Île-de-France représente 26,00 % du CA total de 358 918,60 €. L'écart entre la première et la dernière région est de 48 130,50 €.

**Pattern 3 — Corrélation négative entre prix et quantité**

Deux outils complémentaires :

Formule de vérification dans une cellule hors tableau :
```
=COEFFICIENT.CORRELATION(DonneesNettoyees[Prix_Unitaire];DonneesNettoyees[Quantité])
```
`COEFFICIENT.CORRELATION` (CORREL en anglais) retourne **r = -0,54** sur 820 points. La valeur indique une relation négative modérée. Elle est décroissante mais non linéaire : à bas prix, les quantités sont très variables (papeterie, haute fréquence) ; à haut prix, les quantités sont systématiquement faibles (électroménager, achat rare). Cette non-linéarité justifie l'ajout d'une échelle logarithmique sur l'axe des prix.

Nuage de points : `Prix_Unitaire` en X, `Quantité` en Y, une série, 820 marqueurs. Activer l'échelle logarithmique sur l'axe X : **Format de l'axe > Options d'axe > Échelle logarithmique**.

**Repérer un pattern absent des données :** si l'apprenant annonce, par exemple, une corrélation positive entre marge et quantité, une tendance de croissance régulière sur 24 mois ou un écart de taux de marge entre régions, le formateur demande la valeur du coefficient de corrélation ou le CA mensuel correspondant. S'il ne peut pas produire ce chiffre depuis son fichier, le pattern est non vérifié ou inventé.

### Étape 2 — Choix et construction des graphiques

| Pattern | Type recommandé | Source | Axe X | Axe Y | Séries |
|---|---|---|---|---|---|
| Saisonnalité par catégorie | Courbes avec marqueurs | TCD mois × catégorie | Mois 1–12 | Chiffre_Affaires (€) | 5 courbes |
| Écart régional | Barres horizontales triées | TCD région | CA total (€) | Région | 1 série |
| Corrélation prix/quantité | Nuage de points | Colonnes Prix_Unitaire et Quantité | Prix_Unitaire (€, log) | Quantité | 820 marqueurs |

**Courbe de saisonnalité — construction exacte**

1. Insérer un TCD depuis `DonneesNettoyees` (**Insertion > Tableau croisé dynamique**).
2. Glisser `Mois` (entier) en Lignes, `Catégorie` en Colonnes, `Chiffre_Affaires` en Valeurs (Somme). Ne pas utiliser `Nom_Mois` sans colonne de tri numérique associée.
3. **Analyse du tableau croisé dynamique > Graphique croisé dynamique > Courbes avec marqueurs**.
4. Ce que la copie doit montrer : deux pics distincts sur la courbe Papeterie (août-septembre) ; montée de l'Électronique et de la Téléphonie en novembre-décembre ; sommet de l'Électroménager en juillet-août ; cinq courbes distinguables par couleur, sans légende dupliquée.

**Histogramme régional — construction exacte**

1. TCD : `Région` en lignes, `Chiffre_Affaires` en valeurs, tri décroissant sur les valeurs.
2. **Insertion > Barres groupées** (barres horizontales, non colonnes verticales : les libellés de régions sont lisibles sans rotation et les différences de longueur entre régions sont plus perceptibles à l'horizontal).
3. Ce que la copie doit montrer : Île-de-France nettement en tête (93 302,60 €), Centre et Ouest quasi à égalité en bas (≈ 45 000–46 000 €) ; l'écart visuel entre première et dernière barre doit être saisissant sans commentaire.

**Nuage de points prix/quantité — construction exacte**

1. Sélectionner les deux colonnes `Prix_Unitaire` et `Quantité` du tableau `DonneesNettoyees` (820 lignes).
2. **Insertion > Nuage de points > Nuage de points simple**.
3. Activer l'échelle logarithmique sur l'axe X : clic droit sur l'axe X > **Format de l'axe > Options d'axe > Échelle logarithmique**.
4. Limites à mentionner dans la note de graphique : 820 points superposés produisent du surtracé (overplotting). Correction partielle dans Excel : réduire la taille des marqueurs (**Format de la série > Options des marqueurs > taille 3 pt**) et abaisser l'opacité (**Format de la série > Remplissage > Transparence à 60 %**). Ajouter une courbe de tendance de type Puissance (**clic droit sur la série > Ajouter une courbe de tendance > Puissance**) pour matérialiser la relation décroissante non linéaire sans imposer une linéarité artificielle.
5. Ce que la copie doit montrer : nuage descendant de gauche à droite ; zone de forte densité entre 5 € et 50 € avec des quantités élevées (papeterie, consommables) ; marqueurs rares au-dessus de 300 € avec quantités faibles (électroménager, électronique haut de gamme).

### Étape 3 — Mise en forme

Les critères ci-dessous sont observables dans le fichier rendu.

**Titre porteur d'un message :** ne pas écrire « CA par région » mais « L'Île-de-France concentre 26 % du CA ». Critère observable : le titre contient-il un fait chiffré ou une comparaison explicite ? Un titre purement descriptif ne transmet pas de conclusion et oblige le lecteur à la déduire seul.

**Axes nommés avec unité :** chaque axe comporte une étiquette non vide avec unité. Pour le nuage de points : « Prix unitaire (€) » en X, « Quantité vendue » en Y. Critère : sélectionner l'axe — l'étiquette d'axe est-elle présente et non vide ?

**Suppression du superflu :** quadrillage horizontal uniquement (pas de vertical), pas de bordure de zone de traçage, pas d'ombres, pas de dégradés, pas d'effets 3D. Règle opérationnelle : si on peut supprimer un élément graphique sans perdre d'information, il doit l'être. Vérifier en mode d'impression.

**Charte cohérente entre graphiques :** une même catégorie a la même couleur sur tous les graphiques du fichier. Critère observable : comparer la couleur de la Papeterie sur la courbe de saisonnalité et sur un éventuel histogramme catégoriel — elles doivent être identiques.

**Légende :** présente uniquement si le graphique comporte plusieurs séries non auto-documentées par étiquettes directes. Absente sur l'histogramme régional (une seule série, les régions sont déjà sur l'axe).

**Note par graphique (livrable imposé par l'énoncé) :** la note (3–4 lignes) doit contenir trois éléments distincts du titre : (1) le pattern observé énoncé comme conclusion (« La Papeterie pic en août, preuve d'une saisonnalité de rentrée. »), (2) le type de graphique choisi et la raison (« La courbe est préférée à l'histogramme car elle rend visible l'évolution temporelle entre mois. »), (3) une limite éventuelle ou une précaution d'interprétation (« Le pic d'août 2023 est particulièrement marqué ; vérifier s'il reflète une promotion ponctuelle ou une tendance récurrente. »). Une note qui paraphrase simplement le titre ou qui liste des définitions de termes n'est pas acceptée.

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Lignes du tableau DonneesNettoyees | 820 |
| Colonnes | 15 |
| Valeurs manquantes | 0 |
| CA total | 358 918,60 € |
| Marge totale | 152 433,90 € |
| Taux de marge global | 42,47 % |
| CA Île-de-France | 93 302,60 € |
| Part Île-de-France dans le CA total | 26,00 % |
| CA Centre (dernier rang) | 45 172,10 € |
| Écart Île-de-France / Centre | 48 130,50 € |
| Coefficient de Pearson Prix_Unitaire / Quantité | r = -0,54 |
| Pic Papeterie — mois (cumul 2023-2024) | août : 7 182,80 € |
| Pic Électronique — mois (cumul 2023-2024) | novembre : 12 363,00 € |
| Pic Électroménager — mois (cumul 2023-2024) | août : 13 375,50 € |
| Pic Téléphonie — mois (cumul 2023-2024) | décembre : 9 858,20 € |

Saisonnalité par catégorie — cumul 2023-2024, CA en euros (pour vérification du TCD ligne par ligne) :

| Mois | Mobilier | Papeterie | Téléphonie | Électroménager | Électronique |
|---|---|---|---|---|---|
| 1 — janv. | 4 985,00 | 3 230,60 | 2 736,00 | 5 829,20 | 10 469,20 |
| 2 — févr. | 1 377,50 | 2 331,80 | 2 531,10 | 10 536,10 | 6 258,70 |
| 3 — mars | 5 987,50 | 2 038,20 | 3 585,40 | 2 492,00 | 10 267,90 |
| 4 — avr. | 2 574,00 | 3 864,70 | 4 326,10 | 7 432,10 | 6 094,30 |
| 5 — mai | 6 074,00 | 5 537,60 | 5 358,20 | 4 783,90 | 8 675,20 |
| 6 — juin | 2 362,50 | 3 290,20 | 5 172,60 | 8 786,60 | 8 163,60 |
| 7 — juil. | 3 488,50 | 2 360,20 | 5 208,90 | 8 789,30 | 8 751,30 |
| 8 — août | 6 043,50 | 7 182,80 | 6 081,90 | 13 375,50 | 8 205,20 |
| 9 — sept. | 2 979,00 | 6 912,40 | 7 220,20 | 4 646,10 | 11 467,70 |
| 10 — oct. | 5 247,00 | 4 919,20 | 2 838,90 | 1 930,80 | 11 667,20 |
| 11 — nov. | 4 258,50 | 3 563,50 | 4 478,90 | 7 346,00 | 12 363,00 |
| 12 — déc. | 6 759,50 | 2 339,80 | 9 858,20 | 9 949,20 | 11 534,60 |

Série mensuelle complète du CA global — 24 points (2023-01 à 2024-12) — pour vérifier le TCD de la courbe d'évolution générale :

| Mois_Année | CA | Mois_Année | CA |
|---|---|---|---|
| 2023-01 | 11 346,40 € | 2024-01 | 15 903,60 € |
| 2023-02 | 10 953,10 € | 2024-02 | 12 082,10 € |
| 2023-03 | 16 325,00 € | 2024-03 | 8 046,00 € |
| 2023-04 | 14 002,00 € | 2024-04 | 10 289,20 € |
| 2023-05 | 14 114,10 € | 2024-05 | 16 314,80 € |
| 2023-06 | 10 265,80 € | 2024-06 | 17 509,70 € |
| 2023-07 | 13 674,70 € | 2024-07 | 14 923,50 € |
| 2023-08 | 24 732,40 € | 2024-08 | 16 156,50 € |
| 2023-09 | 16 457,80 € | 2024-09 | 16 767,60 € |
| 2023-10 | 14 355,00 € | 2024-10 | 12 248,10 € |
| 2023-11 | 15 374,90 € | 2024-11 | 16 635,00 € |
| 2023-12 | 18 326,80 € | 2024-12 | 22 114,50 € |

Répartition par catégorie — pour un éventuel histogramme de comparaison de volume :

| Catégorie | CA | Nombre de transactions |
|---|---|---|
| Électronique | 113 917,90 € | 199 |
| Électroménager | 85 896,80 € | 139 |
| Téléphonie | 59 396,40 € | 149 |
| Mobilier | 52 136,50 € | 72 |
| Papeterie | 47 571,00 € | 261 |

Point pédagogique : la Papeterie génère le plus grand nombre de transactions (261) mais le CA le plus faible — ce contraste entre volume de transactions et CA est un quatrième angle d'analyse acceptable si l'apprenant le met en évidence avec un graphique à double axe ou deux barres côte à côte.

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| L'axe X de la courbe de saisonnalité est alphabétique (août avant avril) | Le champ utilisé est `Nom_Mois` (texte) sans ordre de tri configuré | Lire les deux premiers mois sur l'axe : si « août » précède « avril », le tri est alphabétique |
| La courbe de saisonnalité affiche 24 points au lieu de 12 | L'apprenant a utilisé `Mois_Année` au lieu de `Mois` — pas d'agrégation par mois calendaire | Compter les points sur la courbe |
| Le nuage de points est une masse opaque sans structure visible | Marqueurs trop grands (> 6 pt) et opacité à 100 % | Sélectionner un marqueur : lire taille et transparence dans Format de la série |
| La courbe de tendance du nuage est linéaire malgré une relation non linéaire | Type de tendance laissé par défaut (linéaire) | Clic droit sur la courbe de tendance > Format : vérifier le type sélectionné |
| Le coefficient annoncé diffère de -0,54 | La formule porte sur une plage réduite, filtrée, ou les colonnes sont inversées | Relancer `=COEFFICIENT.CORRELATION(DonneesNettoyees[Prix_Unitaire];DonneesNettoyees[Quantité])` sur le tableau complet |
| Un quatrième pattern est annoncé sans valeur chiffrée à l'appui | Résultat d'IA non vérifié sur les données réelles | Demander le coefficient ou la valeur de CA correspondante ; absence de réponse = pattern non vérifié |
| Les titres sont descriptifs (« CA par région ») et non porteurs d'un message | L'apprenant n'a pas réfléchi à la conclusion transmise | Lire le titre : contient-il un chiffre, une comparaison ou une conclusion explicite ? |
| Les couleurs de catégorie diffèrent entre les graphiques | Chaque graphique a été formaté indépendamment | Comparer la couleur de la Papeterie sur deux graphiques |

## 5. Volet IA

Ce qu'on attend dans la copie : l'apprenant cite au moins un usage de l'IA pour le conseil méthodologique (quel graphique pour une corrélation ?) ou la mise en forme (comment réduire l'overplotting dans Excel ?), et indique avoir vérifié le résultat sur les données réelles avant de l'intégrer.

Ce qui distingue un apprenant qui a compris : il peut expliquer pourquoi l'échelle logarithmique est adaptée au nuage de points prix/quantité (la relation est multiplicative : doubler le prix ne réduit pas la quantité d'un nombre fixe d'unités) et il nomme la limite du coefficient de Pearson (mesure une corrélation linéaire — insuffisant si la relation est non linéaire, d'où la courbe de tendance de type Puissance).

Ce qui trahit un recopiage sans vérification : la note descriptive mentionne des patterns génériques absents des données (corrélation positive entre ventes et temps, croissance régulière du CA), ou une valeur de coefficient différente de -0,54.

**Question de vérification orale :** « Votre coefficient de Pearson vaut -0,54. Si un produit passe de 50 € à 100 €, de combien d'unités la quantité vendue va-t-elle diminuer ? » Une bonne réponse reconnaît que le coefficient de Pearson ne permet pas de répondre directement à cette question (il mesure une corrélation linéaire, pas une élasticité) et qu'un modèle de régression ou une courbe de tendance de type Puissance serait nécessaire pour quantifier l'effet d'un doublement de prix.

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Trois patterns identifiés avec valeur chiffrée à l'appui | 4 | Chaque pattern accompagné d'un chiffre issu des valeurs de référence (pic de mois, part régionale, coefficient) |
| Courbe de saisonnalité correcte (mois triés 1–12, 5 courbes) | 3 | Axe X en ordre chronologique, 5 courbes distinguables par couleur |
| Histogramme régional trié décroissant et lisible | 2 | Barres horizontales, Île-de-France en tête, libellés sans rotation |
| Nuage de points avec coefficient calculé et échelle logarithmique | 3 | Cellule `=COEFFICIENT.CORRELATION(...)` visible (valeur ≈ -0,54), axe X en log |
| Titres porteurs d'un message (non descriptifs) | 2 | Chaque titre contient un fait chiffré ou une conclusion explicite |
| Axes nommés avec unités | 2 | Chaque axe comporte une étiquette non vide avec unité |
| Mise en forme (ratio données/encre, charte cohérente) | 2 | Pas de quadrillage vertical, pas d'effets 3D, même couleur par catégorie sur l'ensemble du fichier |
| Note par graphique (3–4 lignes) expliquant le pattern et le choix | 2 | Note présente et distincte du titre, mentionnant le pattern observé et la raison du type de graphique |
| **Total** | **20** | |

## 7. Prolongements

Calculer l'élasticité prix-quantité par catégorie en ajustant un modèle log-log : tracer le nuage de points avec des axes logarithmiques sur X et Y, ajouter une courbe de tendance linéaire — la pente de cette droite est directement l'élasticité estimée pour la catégorie ; comparer les pentes entre Papeterie et Électronique.

Exporter automatiquement chaque graphique en image PNG par macro VBA (`ActiveSheet.ChartObjects("Graphique 1").Chart.Export "C:\chemin\graphique.png"`) pour l'intégrer dans un rapport Word ou PowerPoint sans recapture manuelle.

Créer une quatrième visualisation avec Power Map (**Insertion > 3D Maps**) pour afficher le CA par région sur une carte de France, en s'assurant que les noms de régions (`Île-de-France`, `Nord`, etc.) correspondent aux libellés reconnus par le service de géocodage Bing utilisé par Excel.
