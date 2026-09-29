# Corrigé — Résoudre un problème data métier

**Fichier(s) de données :** `ventes_2023.csv` (1 522 lignes, 9 colonnes)
**Durée indicative :** 120 min
**Prérequis :** Maîtrise des TCD, Power Query ou formules matricielles, notion de marge brute, lecture d'un fichier CSV délimité.

---

## 1. Ce que l'exercice évalue réellement

L'exercice teste la capacité à produire des chiffres fiables malgré des défauts de qualité volontairement injectés, et à interpréter correctement une structure de données avant d'analyser. Le piège central est la question Q3 : la consigne parle de « corrélation vendeur/région », or chaque vendeur n'opère que sur une seule région dans ce jeu de données — il n'y a rien à corréler. Un apprenant qui produit un classement de CA par vendeur et en conclut une performance individuelle n'a pas vu le problème de structure.

**Remarque sur les colonnes.** L'énoncé liste `Date, ID_Produit, Catégorie, Vendeur, Quantité, Prix_Unitaire, Région`. Le fichier livré contient deux colonnes supplémentaires : `Produit` (nécessaire pour que le top 3 de Q2 soit lisible) et `Cout_Unitaire` (indispensable pour calculer la marge brute de Q2). Sans elles, Q2 serait insoluble. Il n'y a pas d'erreur dans le fichier ; c'est un enrichissement voulu.

---

## 2. Corrigé pas à pas

### Étape 1 — Exploration et nettoyage des données

**Chargement du fichier.**
Le fichier est encodé UTF-8 avec BOM, séparateur point-virgule, décimale à la virgule. Dans Power Query : **Données > Obtenir des données > À partir d'un fichier texte/CSV**, puis vérifier que l'encodage détecté est UTF-8 et remplacer la virgule décimale si nécessaire (**Transformation > Remplacer les valeurs** sur `Prix_Unitaire` et `Cout_Unitaire`).

En Python / pandas :
```python
import pandas as pd
df = pd.read_csv("ventes_2023.csv", sep=";", encoding="utf-8-sig", decimal=",")
```

**Suppression des doublons stricts.**
23 lignes sont des doublons exacts sur l'ensemble des colonnes. Dans Excel : **Données > Supprimer les doublons** (toutes les colonnes cochées). En Power Query : **Accueil > Supprimer les lignes > Supprimer les doublons**. Résultat attendu : 1 499 lignes restantes avant les autres corrections.

**Harmonisation des formats de date.**
180 dates sont au format ISO texte `AAAA-MM-JJ` ; 1 342 sont au format français `JJ/MM/AAAA`. Excel les traite différemment selon les paramètres régionaux.

Formule de normalisation (colonne auxiliaire) :
```excel
=SI(LONGUEUR(A2)=10;
   SI(TROUVE("-";A2;5)>0;
      DATE(GAUCHE(A2;4);STXT(A2;6;2);DROITE(A2;2));
      DATEVAL(A2));
   DATEVAL(A2))
```
En Power Query, une seule transformation : **Transformation > Type de données > Date** détecte les deux formats si le séparateur décimal est correctement configuré. C'est la voie la plus robuste.

**Traitement des valeurs aberrantes.**

*Quantités aberrantes.* 6 lignes présentent des quantités de 9 999 ou 4 500 unités, vraisemblablement des saisies erronées (les autres transactions sont dans des plages de 1 à quelques dizaines d'unités). Ces lignes doivent être écartées. L'impact sur le CA est massif : sans ce nettoyage, le CA total atteint 3 452 709,09 € et le taux de croissance T4/T1 monte à 1 748,70 % — deux chiffres qui devraient immédiatement alerter l'analyste.

*Quantités négatives.* 3 lignes affichent des quantités négatives. Deux interprétations sont possibles, et la bonne copie documente son choix :
- Si ce sont des retours clients légitimes, les conserver permet de calculer un CA net réel.
- Si ce sont des erreurs de saisie, les écarter est plus défendable pour une analyse de performance commerciale.

Dans les deux cas, le choix doit figurer dans l'onglet `Données` (cellule commentée ou colonne `Statut`) et être mentionné dans la note de synthèse. Le corrigé ci-dessous écarte ces 3 lignes pour aligner les valeurs avec les chiffres de référence (1 486 lignes retenues).

*Prix unitaires à 0,01 €.* 4 lignes présentent un prix unitaire de 0,01 €. Ces lignes faussent la marge brute et le CA. Elles sont écartées.

**Bilan du nettoyage :**
- Lignes initiales : 1 522
- Doublons supprimés : 23
- Quantités aberrantes supprimées : 6
- Quantités négatives supprimées : 3
- Prix aberrants supprimés : 4
- **Lignes retenues : 1 486**

---

### Q1 — Tendance mensuelle du CA par catégorie

**Méthode recommandée : TCD.**
Insérer un TCD depuis l'onglet `Données` nettoyé : lignes = Mois (groupe par mois sur le champ Date), colonnes = Catégorie, valeurs = Somme de `CA_Ligne` (colonne calculée : `=Quantité * Prix_Unitaire`).

Formule de la colonne calculée dans un tableau structuré nommé `Ventes` :
```excel
=[@Quantité]*[@Prix_Unitaire]
```

**Point de finesse.** Le mois le plus performant toutes catégories est décembre (70 016,30 €). Mais le mois de pointe diffère selon la catégorie :

| Catégorie | Mois de pointe |
|---|---|
| Mobilier | septembre |
| Papeterie | août |
| Téléphonie | décembre |
| Électroménager | juin |
| Électronique | novembre |

Un apprenant qui répond « décembre est le meilleur mois » sans cette nuance n'a pas analysé les catégories séparément — c'est pourtant l'essentiel de la question.

---

### Q2 — Top 3 des produits les plus rentables par région

**Marge brute par ligne :**
```excel
=[@Quantité]*([@Prix_Unitaire]-[@Cout_Unitaire])
```

**Agrégation par produit et région :**
```excel
=SOMME.SI.ENS(Ventes[Marge_Ligne];
              Ventes[Région];[@Région];
              Ventes[Produit];[@Produit])
```
`SOMME.SI.ENS` (SUMIFS) calcule la marge cumulée par couple Produit/Région.

**Classement au sein de chaque région :**
```excel
=RANG([@Marge_Region];
      FILTRE(Marge_Region_Col; Region_Col=[@Région]))
```
Alternative acceptable : un TCD avec filtre de page sur la Région, trié sur la marge décroissante. Les valeurs de référence pour les 6 régions figurent en section 3.

---

### Q3 — Corrélation vendeur/région : identification du piège

**Ce que la structure des données révèle.**
Dans `ventes_2023.csv`, chaque vendeur n'opère que sur une seule région. Les deux variables Vendeur et Région sont parfaitement confondues : connaître le vendeur détermine la région, et réciproquement.

La question « existe-t-il une corrélation ? » est donc un piège méthodologique. Il n'y a pas de corrélation à mesurer : la variable Région est entièrement redondante avec Vendeur. Un coefficient de corrélation calculé entre le CA d'un vendeur et son identifiant de région serait mathématiquement sans objet.

**Ce que le CA d'un vendeur reflète réellement.**
Le CA de Camille Fournier (99 293,10 €, Île-de-France, 200 transactions) est supérieur à celui de Thomas Girard (38 952,50 €, Nord, 112 transactions). Cet écart est-il dû à la performance individuelle ou au poids commercial de la région ? Le tableau ci-dessous montre que le panier moyen nuance le classement brut :

| Région | Vendeur | CA | Panier moyen |
|---|---|---|---|
| Île-de-France | Camille Fournier | 99 293,10 € | 496,47 € |
| Sud | Léa Bonnet | 78 634,60 € | 531,31 € |
| Est | Yanis Perrot | 75 738,70 € | 384,46 € |
| Île-de-France | Hugo Marchand | 74 232,70 € | 414,71 € |
| Centre | Claire Vasseur | 65 802,30 € | 453,81 € |
| Nord | Nora Lefèvre | 62 505,80 € | 492,17 € |
| Ouest | Inès Moreau | 58 623,30 € | 480,52 € |
| Sud | Samir Haddad | 57 214,30 € | 400,10 € |
| Nord | Thomas Girard | 38 952,50 € | 347,79 € |
| Ouest | Malik Benali | 36 132,70 € | 384,39 € |
| Centre | Sofia Renard | 6 565,90 € | 505,07 € |
| Est | Bastien Roux | 2 257,70 € | 376,28 € |

Léa Bonnet (Sud) a le panier moyen le plus élevé (531,31 €) alors qu'elle n'est pas première en CA. Sofia Renard (Centre) affiche un panier de 505,07 € pour seulement 13 transactions — profil très différent d'une faible performance.

**Ce qu'une bonne copie propose.** Plutôt qu'un classement brut de CA, l'apprenant doit proposer un indicateur comparable malgré la structure confondante : panier moyen, CA par transaction, ou part de marché intra-région (CA du vendeur / CA total de la région). Ces indicateurs permettent de comparer deux vendeurs de la même région entre eux (ex. Camille Fournier vs Hugo Marchand en Île-de-France) ou de normaliser les performances inter-régions.

**Pour le formateur.** Cette question est un déclencheur de discussion en soutenance : demander à l'apprenant « comment compareriez-vous Thomas Girard à Camille Fournier ? » permet de vérifier s'il a compris l'effet de structure ou s'il a simplement trié le CA.

---

### Q4 — Taux de croissance T4/T1

Formule de base dans un tableau récapitulatif :
```excel
=(CA_T4-CA_T1)/CA_T1
```

Avec des colonnes de trimestre dérivées de la date :
```excel
=ENT((MOIS([@Date])+2)/3)
```

CA par trimestre après nettoyage :

| Trimestre | CA |
|---|---|
| T1 | 142 716,40 € |
| T2 | 151 038,70 € |
| T3 | 175 416,40 € |
| T4 | 186 782,10 € |

**Taux de croissance T4/T1 : +30,88 %.**

Si les valeurs aberrantes ne sont pas retirées : CA total à 3 452 709,09 €, taux T4/T1 à 1 748,70 %. Cet écart est la démonstration la plus directe de l'importance du nettoyage.

---

### Étape 4 — Note de synthèse (200 mots max)

**Ce qu'une bonne note contient.**
- Un chiffre ancré dans les données pour chaque observation : « Le CA de décembre (70 016,30 €) dépasse de 68 % le CA de janvier (41 708,50 €) ».
- Une recommandation actionnable : « Renforcer les stocks d'électronique en octobre pour profiter du pic de novembre », pas « améliorer la gestion des stocks ».
- La mention du choix opéré sur les quantités négatives et son impact sur les chiffres présentés.

**Ce qui disqualifie la note.**
- Une recommandation non étayée par un chiffre du jeu de données.
- Une action non actionnable (« mieux communiquer », « optimiser les performances »).
- Des chiffres issus des données brutes non nettoyées (repérable par un CA total supérieur à 600 000 € mais non arrondi à 655 953,60 €).

---

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Lignes initiales | 1 522 |
| Doublons stricts | 23 |
| Dates ISO texte | 180 |
| Quantités aberrantes | 6 |
| Quantités négatives | 3 |
| Prix aberrants | 4 |
| Lignes retenues | 1 486 |
| CA total après nettoyage | 655 953,60 € |
| Marge brute totale | 276 667,80 € |
| Mois le plus performant (toutes catégories) | décembre — 70 016,30 € |
| Mois de pointe Électroménager | juin — 22 891,10 € |
| Mois de pointe Papeterie | août — 12 873,40 € |
| Mois de pointe Mobilier | septembre — 12 160,50 € |
| T1 | 142 716,40 € |
| T4 | 186 782,10 € |
| Taux T4/T1 | +30,88 % |
| Taux T4/T1 sans nettoyage | 1 748,70 % |
| Top 1 marge Île-de-France | Smartphone Signal — 4 838,00 € |
| Top 1 marge Sud | Smartphone Signal — 3 540,00 € |
| Top 1 marge Nord | Smartphone Signal — 2 950,00 € |
| Top 1 marge Ouest | Machine à café Arôme — 2 660,00 € |
| Top 1 marge Est | Réfrigérateur d'appoint Fraîcheur — 2 288,00 € |
| Top 1 marge Centre | Bureau réglable Altitude — 2 136,00 € |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| CA total supérieur à 3 M€ | Quantités aberrantes non retirées | Vérifier le CA total : attendu 655 953,60 € |
| Taux T4/T1 supérieur à 1 000 % | Même cause | Taux attendu : +30,88 % |
| Doublons non supprimés (1 522 lignes en fin de nettoyage) | Suppression ignorée ou faite après d'autres filtres | Compter les lignes : attendu 1 486 |
| Dates ISO traitées comme du texte (graphique désordonné) | Format non harmonisé | Vérifier que la colonne Date est bien de type Date dans le TCD |
| Top 3 par CA plutôt que par marge brute | Colonne Cout_Unitaire ignorée | La marge brute exige Prix_Unitaire - Cout_Unitaire ; un top 3 par CA donne des résultats différents |
| Classement vendeurs présenté comme performance individuelle | Piège Q3 non détecté | L'apprenant doit mentionner la confusion vendeur/région |
| Note de synthèse sans chiffre | Recommandation rédigée sans s'appuyer sur les données | Vérifier qu'au moins deux chiffres du jeu apparaissent dans la note |

---

## 5. Volet IA

**Ce qu'on attend dans la copie.**
L'énoncé autorise l'IA pour générer des formules complexes (SOMME.SI.ENS imbriqués, calcul de trimestre, formule de marge) et pour structurer la note de synthèse. La trace attendue est une cellule ou un commentaire indiquant quelle formule a été générée par IA et comment l'apprenant l'a vérifiée.

**Comment distinguer compréhension et copie-collé.**
Un apprenant qui a compris peut reformuler le rôle de chaque argument dans `SOMME.SI.ENS` et expliquer pourquoi la formule de trimestre `ENT((MOIS(date)+2)/3)` fonctionne. Un apprenant qui a recopié produira souvent des formules anglaises (`SUMIFS`, `INT`) sans savoir les adapter aux paramètres régionaux français.

**Question de vérification orale.**
« Votre formule de marge utilise `[@Cout_Unitaire]`. Que se passerait-il si la colonne s'appelait `Coût_Achat` dans un autre fichier ? Comment l'IA vous a-t-elle aidé à identifier ça, ou avez-vous dû l'ajuster vous-même ? »

---

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Nettoyage complet et documenté | 4 | 1 486 lignes, 4 types d'anomalies traités, choix sur quantités négatives explicité |
| Q1 — CA mensuel par catégorie correct | 3 | Total décembre = 70 016,30 € ; mois de pointe par catégorie identifiés |
| Q2 — Top 3 marge brute par région correct | 4 | Au moins 2 régions vérifiées avec les valeurs de référence |
| Q3 — Identification de la confusion vendeur/région | 4 | La copie mentionne explicitement que chaque vendeur n'opère que sur une région et propose un indicateur alternatif |
| Q4 — Taux de croissance T4/T1 correct | 2 | +30,88 % ou valeur cohérente selon le traitement des quantités négatives documenté |
| Note de synthèse (200 mots, 2 actions chiffrées) | 2 | Deux recommandations avec au moins un chiffre chacune |
| Lisibilité du fichier Excel (onglets, titres, mise en forme) | 1 | 3 onglets distincts nommés Données / Calculs / Dashboard |
| **Total** | **20** | |

---

## 7. Prolongements

Pour les apprenants rapides, une piste par axe non couvert par l'énoncé.

La saisonnalité par région : croiser le CA mensuel avec la Région permet de vérifier si le pic de juin en Électroménager est uniforme ou concentré sur certaines zones géographiques.

La marge brute mensuelle : calculer le taux de marge brute mois par mois révèle si la croissance du CA au T4 s'accompagne d'une pression sur les prix (promotions de fin d'année) ou d'une amélioration de la rentabilité.

La concentration du portefeuille produits : le Smartphone Signal apparaît en première position dans quatre régions sur six pour la marge brute — calculer sa part dans la marge totale et évaluer le risque de dépendance à un seul produit.
