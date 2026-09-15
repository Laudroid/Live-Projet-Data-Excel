# Corrigé — Explorer les données via les TCD

**Fichier(s) de données :** `Ventes_Globales.xlsx` (1 600 lignes, 6 colonnes)
**Durée indicative :** 50 min
**Prérequis :** Savoir insérer un TCD, connaître les notions de champ ligne, colonne et valeur.

---

## 1. Ce que l'exercice évalue réellement

L'exercice évalue la capacité à structurer un TCD depuis une plage brute, à gérer le groupement temporel sur des données bi-annuelles et à interpréter une saisonnalité de façon objectivable plutôt qu'intuitive. Le piège central est le groupement des dates par mois seul sur un jeu couvrant deux années calendaires : un groupement par Mois sans Années agrège janvier 2023 avec janvier 2024, rendant le TCD inexploitable pour une lecture chronologique.

## 2. Corrigé pas à pas

### Étape 1 — Transformation en tableau structuré

Sélectionner une cellule quelconque de la plage de données, puis **Accueil > Styles > Mettre sous forme de tableau** ou raccourci `Ctrl+T`. Dans la boîte de dialogue, vérifier que la plage couvre bien A1:F1601 (en-têtes inclus) et que la case « Mon tableau comporte des en-têtes » est cochée.

Nommer le tableau : cliquer sur le tableau, puis **Création du tableau > Nom du tableau** (coin supérieur gauche du ruban), saisir `DonnéesVentes`.

Ce que le tableau structuré apporte réellement : la plage source du TCD est liée au nom du tableau, pas à une adresse fixe. Si l'on ajoute des lignes sous le tableau, Excel étend automatiquement le tableau et la plage source du TCD sans intervention manuelle. En revanche, le TCD ne se recalcule pas seul : il faut toujours cliquer **Actualiser** (clic droit sur le TCD > Actualiser, ou **Analyse du tableau croisé dynamique > Actualiser**) pour que les nouvelles données apparaissent.

Colonnes du fichier (noms exacts, espaces et parenthèses inclus) :

| Lettre | Nom de colonne |
|---|---|
| A | Date |
| B | Région |
| C | Catégorie de produit |
| D | Vendeur |
| E | Chiffre d'affaires (CA) |
| F | Quantité vendue |

### Étape 2a — TCD 1 : Analyse géographique et temporelle

**Insérer > Tableau croisé dynamique**, source : `DonnéesVentes`, emplacement : nouvelle feuille. Nommer la feuille `TCD_Region_Mois`.

Configuration du TCD :

- Zone **Lignes** : `Région`
- Zone **Colonnes** : `Date`
- Zone **Valeurs** : `Chiffre d'affaires (CA)` en somme

Groupement des dates — point critique :

Clic droit sur un champ Date dans le TCD > **Grouper**. La boîte de dialogue propose Secondes, Minutes, Heures, Jours, Mois, Trimestres, Années.

**Ne pas sélectionner Mois seul.** Avec 24 mois répartis sur deux années (2023 et 2024), un groupement par Mois seul crée 12 colonnes qui additionnent janvier 2023 et janvier 2024, février 2023 et février 2024, etc. Le résultat s'appelle un profil mensuel agrégé, pas une chronologie : on perd la lecture de l'évolution d'une année sur l'autre.

Sélectionner **Années ET Mois** simultanément (maintenir `Ctrl` pour multi-sélection). Le TCD affiche alors 24 colonnes, soit les 24 mois distincts, avec Années comme en-tête de groupe et Mois comme sous-en-tête.

Si le groupement reste grisé ou renvoie une erreur, vérifier que la colonne Date ne contient pas de valeurs textuelles : pandas confirme que le type est `datetime64[ns]`, donc les dates sont bien numériques dans le fichier livré.

Question « quelle région affiche la plus forte saisonnalité ? »

La réponse n'est pas à deviner à l'œil. Trois méthodes objectivables depuis le TCD lui-même, et la force du jeu de données actuel est qu'elles concordent toutes les trois :

1. **Coefficient de variation (CV)** : écart-type des 24 valeurs mensuelles divisé par leur moyenne. Un CV élevé signifie une forte dispersion relative.

2. **Rapport max/min mensuel** : dans une colonne auxiliaire, calculer pour chaque région le CA du mois le plus fort divisé par le CA du mois le plus faible. Plus ce rapport est élevé, plus la région est saisonnière.

3. **Lecture directe du profil mensuel** : pour la région la plus saisonnière, le graphique en courbes montre une bosse estivale impossible à confondre avec les autres régions. L'accord entre les trois méthodes est un signe que la réponse est robuste, pas un artefact de l'indicateur choisi.

Valeurs de référence (CV calculé sur les 24 mois, toutes années confondues) :

| Région | CV mensuel |
|---|---|
| Sud | 68,92 % |
| Ouest | 41,38 % |
| Nord | 39,94 % |
| Est | 37,31 % |
| Centre | 32,33 % |
| Île-de-France | 21,67 % |

**Réponse attendue : le Sud est la région la plus saisonnière, avec un écart de 27 points sur la suivante (Ouest à 41,38 %). L'Île-de-France est la plus stable.**

Profil mensuel de la région Sud (cumul des deux années), pour vérification :

| Mois | CA cumulé |
|---|---|
| janvier | 2 994,80 € |
| février | 3 185,30 € |
| mars | 3 564,30 € |
| avril | 5 979,80 € |
| mai | 11 870,30 € |
| juin | 24 009,30 € |
| juillet | 24 797,40 € |
| août | 25 035,20 € |
| septembre | 15 416,50 € |
| octobre | 15 560,50 € |
| novembre | 6 488,80 € |
| décembre | 9 775,80 € |

Le rapport max/min pour la région Sud vaut 25 035,20 / 2 994,80 = 8,36. L'activité estivale (juin-août) représente à elle seule plus de la moitié du CA annuel de la région. Ce résultat est cohérent avec le CV de 68,92 % et avec la lecture visuelle du profil : les trois méthodes désignent le même vainqueur, ce qui rend la réponse incontestable.

### Étape 2b — TCD 2 : Performance par catégorie

Nouvelle feuille nommée `TCD_Categorie`. Configuration :

- Zone **Lignes** : `Catégorie de produit`
- Zone **Valeurs** :
  - `Chiffre d'affaires (CA)` en somme
  - `Quantité vendue` en moyenne

Pour ajouter la moyenne : faire glisser `Quantité vendue` dans la zone Valeurs une seconde fois. Cliquer sur le champ ajouté > **Paramètres des champs de valeurs** > sélectionner **Moyenne**.

Tri décroissant sur le CA : clic droit sur une cellule de la colonne CA > **Trier > Du plus grand au plus petit**.

### Étape 2c — TCD 3 : Analyse des vendeurs

Nouvelle feuille nommée `TCD_Vendeurs`. Configuration :

- Zone **Filtres** : `Région`
- Zone **Lignes** : `Vendeur`
- Zone **Valeurs** : `Chiffre d'affaires (CA)` en somme

Insertion du segment : cliquer sur le TCD, puis **Analyse du tableau croisé dynamique > Insérer un segment**. Cocher `Catégorie de produit`. Valider. Le segment apparaît sur la feuille et pilote le TCD par clic.

### Étape 3 — Note de conclusion (livrable)

Une bonne note de conclusion sur l'analyse Région x Mois doit mentionner explicitement :

- La région la plus saisonnière identifiée (Sud) et la méthode d'objectivation retenue (CV, rapport max/min ou lecture du profil mensuel — les trois concordent).
- La région la plus stable (Île-de-France), avec son écart avec les autres régions.
- Le pattern réel : le Sud concentre son activité sur l'été (juin-août cumulent plus de la moitié du CA annuel de la région), tandis que l'Île-de-France affiche un CA quasi constant d'un mois sur l'autre.
- Une recommandation opérationnelle courte : ce contraste a des implications concrètes — gestion des stocks saisonniers dans les points de vente du Sud avant juin, planification des effectifs saisonniers sur la période estivale, alors que l'Île-de-France peut fonctionner sur un rythme permanent sans ajustement mensuel significatif.
- Un commentaire sur la structure bi-annuelle : préciser si la saisonnalité se reproduit à l'identique en 2023 et en 2024, ou si des variations d'une année sur l'autre sont visibles.

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Nombre de lignes (hors en-tête) | 1 600 |
| CA total toutes régions | 705 440,90 € |
| Région la plus saisonnière (CV) | Sud — 68,92 % |
| Région la plus stable (CV) | Île-de-France — 21,67 % |
| CA Électronique | 185 924,40 € |
| CA Électroménager | 169 397,00 € |
| CA Téléphonie | 151 224,80 € |
| CA Mobilier | 107 302,00 € |
| CA Papeterie | 91 592,70 € |
| Quantité vendue moyenne — Papeterie | 33,37 |
| Quantité vendue moyenne — Mobilier | 3,63 |
| Premier vendeur (CA) | Camille Fournier — 99 421,80 € |
| Dernier vendeur (CA) | Sofia Renard — 2 424,40 € |

Tableau TCD 2 attendu, trié décroissant sur le CA :

| Catégorie de produit | Somme du CA | Moyenne de Quantité vendue |
|---|---|---|
| Électronique | 185 924,40 € | 5,97 |
| Électroménager | 169 397,00 € | 4,93 |
| Téléphonie | 151 224,80 € | 11,03 |
| Mobilier | 107 302,00 € | 3,63 |
| Papeterie | 91 592,70 € | 33,37 |

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| TCD 1 : 12 colonnes au lieu de 24 | Groupement par Mois seul ; janvier 2023 et janvier 2024 sont fusionnés | Compter les colonnes de dates dans le TCD ; si 12, vérifier les options de groupement (Années doit être coché) |
| Le TCD ne reflète pas les données ajoutées | La plage source est une adresse fixe, pas le tableau DonnéesVentes | Cliquer Analyser > Modifier la source de données ; vérifier que la source affiche DonnéesVentes et non A1:F1601 |
| Région la plus saisonnière indiquée : Île-de-France | Confusion entre la région au CA le plus élevé et la région la plus variable | Rappeler que la saisonnalité se mesure par la dispersion, pas par le volume total |
| Quantité vendue affichée en somme, pas en moyenne | L'apprenant n'a pas changé la fonction d'agrégation dans Paramètres des champs de valeurs | Clic droit sur la valeur > Paramètres ; lire la fonction sélectionnée |
| Segment absent ou non fonctionnel | Segment créé sur une copie du TCD non connectée au bon TCD | Clic droit sur le segment > Connexions de rapports ; vérifier que le bon TCD est coché |
| TCD non actualisé après conversion en tableau | L'apprenant a cru que la conversion automatisait l'actualisation | Modifier manuellement une valeur fictive dans les données, actualiser le TCD, constater la différence |
| Tri décroissant perdu après rafraîchissement | Tri appliqué sur la colonne de résultats et non via Paramètres des champs de valeurs | Cliquer sur la catégorie dans les lignes > Trier > Options supplémentaires > cocher Tri automatique sur le champ CA |

## 5. Volet IA

L'énoncé autorise l'IA pour créer des champs calculés complexes, interpréter les tendances et déboguer les erreurs. Ce qui est attendu dans la copie :

- L'apprenant doit avoir reformulé la réponse de l'IA en ses propres termes dans la note de conclusion. Un apprenant qui comprend peut expliquer pourquoi le groupement Mois seul pose problème ; un apprenant qui a recopié proposera une note générique sans lien avec les valeurs du TCD.
- Les valeurs citées dans la note (CA par région, identification du Sud) doivent correspondre exactement aux résultats visibles dans le fichier rendu.

Question de vérification orale :

« Dans votre TCD Région x Mois, vous avez désigné le Sud comme la région la plus saisonnière. Si je filtre uniquement sur l'année 2024, le classement change-t-il ? Comment calculeriez-vous le coefficient de variation à partir du TCD sans formule externe ? »

Cette question distingue l'apprenant qui a compris la mécanique de la dispersion de celui qui a simplement lu la valeur dans le corrigé.

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Tableau DonnéesVentes créé et nommé correctement | 2 | Onglet Création du tableau > Nom : DonnéesVentes |
| TCD 1 présent avec groupement Années + Mois | 3 | 24 colonnes de dates visibles dans le TCD |
| TCD 1 : identification correcte de la région la plus saisonnière (Sud) | 2 | Réponse écrite dans la note ou annotation dans le fichier |
| TCD 2 : deux valeurs (somme CA et moyenne Quantité) présentes et correctes | 2 | Vérifier Électronique : 185 924,40 € et 5,97 |
| TCD 2 : tri décroissant actif sur le CA | 1 | Électronique en première ligne |
| TCD 3 : Région en filtre, Vendeur en lignes | 2 | Structure du TCD dans le panneau Champs |
| TCD 3 : segment Catégorie de produit fonctionnel | 2 | Cliquer sur une catégorie dans le segment et vérifier que le TCD se filtre |
| Note de conclusion (3-4 lignes, contenu substantiel) | 3 | Note présente, Sud et Île-de-France mentionnées, élément de méthode présent |
| Feuilles correctement nommées (3 feuilles distinctes + Données) | 1 | Onglets visibles dans le classeur |
| Total | 18 | |

## 7. Prolongements

Ajouter un champ calculé dans le TCD 2 pour obtenir le CA par unité vendue (`Chiffre d'affaires (CA)` / `Quantité vendue`) : cliquer **Analyse > Champs, éléments et jeux > Champ calculé**, nommer le champ `CA par unité`, formule `='Chiffre d''affaires (CA)'/'Quantité vendue'`.

Connecter les trois TCD à un même segment Région de façon à créer un mini-tableau de bord interactif : clic droit sur le segment > Connexions de rapports > cocher les trois TCD.

Exporter les données du TCD 2 vers Power Query pour un nettoyage automatique des en-têtes de colonnes générés par Excel lors du groupement (intéressant si le TCD alimente ensuite une formule externe).
