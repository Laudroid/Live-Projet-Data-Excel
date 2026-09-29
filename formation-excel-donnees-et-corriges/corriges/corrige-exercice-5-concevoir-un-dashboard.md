# Corrigé — Conception d'un Dashboard de Pilotage sous Excel

**Fichier(s) de données :** `Dashboard_Source.xlsx` (906 lignes livrées, 15 colonnes)
**Durée indicative :** 90 min
**Prérequis :** Savoir créer un TCD et un graphique croisé dynamique, insérer des segments ; avoir réalisé les TP de nettoyage (Exercices B1 à B4).

---

## 1. Ce que l'exercice évalue réellement

L'exercice teste la capacité à transformer des données brutes imparfaites en outil de pilotage interactif et cohérent. Le piège est double : sauter l'étape de nettoyage produit des KPI faux vérifiables par les valeurs de référence (CA gonflé par les doublons, chronologie refusée à cause des dates textuelles) ; et la connexion incomplète des segments aux TCD est le défaut de construction le plus fréquent en soutenance — un filtre qui ne s'applique qu'à un seul graphique rend le dashboard incohérent sans que l'apprenant s'en aperçoive immédiatement.

## 2. Corrigé pas à pas

### Étape 1 — Préparation et Modélisation

**1a. Convertir la plage en tableau structuré**

Le fichier est livré en plage simple (pas de tableau structuré). Sélectionner une cellule de données > **Insertion > Tableau** (ou `Ctrl+T`) > cocher « Mon tableau comporte des en-têtes ». Renommer le tableau dans l'onglet **Création de tableau** : `DonneesVentes`. Résultat : 906 lignes de données + 1 ligne d'en-tête, colonnes : `ID_Commande`, `Date`, `Magasin`, `Région`, `Vendeur`, `Catégorie`, `Produit`, `Quantité`, `Prix_Unitaire`, `Cout_Unitaire`, `Remise`, `CA_Net`, `Marge`, `Segment_Client`, `Mode_Paiement`.

**1b. Repérer et corriger les quatre défauts injectés**

*Défaut 1 — 6 doublons stricts*

Chemin : **Données > Supprimer les doublons** > cocher toutes les colonnes (ou au minimum `ID_Commande`, qui est l'identifiant de commande). Résultat attendu : message « 6 valeurs en double trouvées et supprimées. 900 valeurs uniques conservées. »

Conséquence si non corrigé : le nombre de commandes affiché dans un TCD en Nombre est 906 au lieu de 900 ; le CA net total est supérieur à 384 439,39 € d'un montant correspondant aux 6 commandes dupliquées. C'est le signal de détection le plus simple : comparer le nombre de lignes après nettoyage avec la valeur attendue de 900.

*Défaut 2 — 10 dates saisies en texte*

Symptôme : 10 cellules de la colonne `Date` sont alignées à gauche dans la cellule (comportement texte) ; elles contiennent une chaîne au format « JJ/MM/AAAA » et non un numéro de série Excel.

Conséquences opérationnelles en cascade :
- Le TCD ne peut pas grouper par mois les cellules textuelles : ces 10 lignes apparaissent comme valeurs individuelles (ex. « 15/03/2024 ») plutôt qu'être agrégées dans le groupe « Mars ».
- L'outil **Chronologie** vérifie que la colonne source est intégralement de type Date avant de s'insérer. Si une seule cellule est du texte, Excel affiche le message d'erreur « Impossible d'insérer la chronologie, car aucun champ de date n'est sélectionné. »

Correction formule dans une colonne auxiliaire :
```
=SI(ESTTEXTE([@Date]);DATEVAL([@Date]);[@Date])
```
`DATEVAL` (DATEVALUE en anglais) convertit une chaîne « JJ/MM/AAAA » en numéro de série Excel. Copier la colonne auxiliaire > Coller valeurs dans la colonne `Date` > Supprimer la colonne auxiliaire > Reformater la colonne en Date courte.

Alternative Power Query (plus robuste, sans colonne auxiliaire) : **Données > Obtenir et transformer > À partir du tableau** > sélectionner la colonne `Date` > **Transformer > Type de données > Date** > **Fermer et charger**. Power Query homogénéise le type et régénère la colonne sans intervention manuelle.

*Défaut 3 — 8 libellés Région avec espace parasite*

Symptôme : un TCD sur `Région` affiche des doublons du type « Île-de-France » et «  Île-de-France  » (espaces avant ou après), ce qui crée deux groupes distincts dans les segments et fausse les totaux régionaux.

Correction formule dans une colonne auxiliaire :
```
=SUPPRESPACE([@Région])
```
`SUPPRESPACE` (TRIM en anglais) supprime les espaces de début et de fin, et réduit les espaces internes multiples à un seul. Copier > Coller valeurs dans la colonne `Région` > Supprimer la colonne auxiliaire.

Alternative Rechercher/Remplacer : `Ctrl+H`, chercher « ` Île-de-France ` » (avec espaces) et remplacer par « Île-de-France » — mais cette approche est laborieuse si les libellés parasités sont variés (elle ne détecte pas automatiquement les cellules affectées).

*Défaut 4 — 5 remises manquantes*

La colonne `Remise` contient 5 cellules vides. L'imputation attendue est 0 (remise non accordée).

Correction : **Accueil > Rechercher et sélectionner > Sélectionner les cellules vides** (sur la colonne `Remise`) > saisir `0` > `Ctrl+Entrée`. Les 5 cellules sont remplies simultanément. Conséquence si non corrigé : la remise moyenne calculée par un TCD en Moyenne porte sur 895 valeurs au lieu de 900, ce qui produit une remise moyenne légèrement surévaluée (les commandes sans remise ne contribuent pas à la moyenne).

**1c. Colonnes `CA_Net` et `Marge` déjà présentes**

Ces deux colonnes sont dans le fichier livré. L'apprenant n'a pas à les recréer. Il peut vérifier la cohérence :
```
=[@Prix_Unitaire]*[@Quantité]*(1-[@Remise])
```
doit correspondre à `CA_Net`, et :
```
=[@CA_Net]-[@Cout_Unitaire]*[@Quantité]
```
doit correspondre à `Marge`.

### Étape 2 — Extraction des KPIs

Créer un onglet nommé `Calculs`. Pour chaque KPI, insérer un TCD dédié depuis la même source `DonneesVentes` (impératif pour le partage des segments, voir Étape 3d).

| KPI | Construction | Valeur attendue après nettoyage |
|---|---|---|
| CA net total | TCD : `CA_Net` en valeurs, Somme | 384 439,39 € |
| Marge totale | TCD : `Marge` en valeurs, Somme | 150 775,59 € |
| Taux de marge | cellule = Marge totale / CA net total | 39,22 % |
| Panier moyen | TCD : `CA_Net` en valeurs, Moyenne | 427,15 € |
| Nombre de commandes | TCD : `ID_Commande` en valeurs, Nombre | 900 |
| Remise moyenne | TCD : `Remise` en valeurs, Moyenne | 5,09 % |

Remarque technique : le taux de marge et la remise moyenne ne sont pas des moyennes directes de taux unitaires — ils doivent être calculés comme le rapport de deux sommes (Marge totale / CA net total) ou en s'assurant que toutes les lignes contribuent à la moyenne de `Remise`. Créer une cellule de calcul à côté du TCD concerné : `=[cellule Marge] / [cellule CA_Net]`.

Les TCD pour les KPI simples n'ont besoin que d'un champ valeur, sans champ de ligne ni de colonne — ils affichent une seule cellule référençable depuis la feuille Dashboard.

### Étape 3 — Design et Interactivité

**3a. Feuille Dashboard**

Créer l'onglet `Dashboard`. Masquer le quadrillage : **Affichage > décocher Quadrillage**. Masquer les en-têtes de lignes et de colonnes : **Affichage > décocher En-têtes**. Résultat : une feuille blanche sans repères de grille, propice à la mise en page libre.

**3b. Choix des graphiques par type de question**

| Question métier | Type de graphique recommandé | TCD source | Paramétrage clé |
|---|---|---|---|
| Tendance mensuelle du CA | Courbes | Date groupé par mois en lignes, `CA_Net` en valeurs | 12 points, axe X = jan–déc 2024 |
| Comparaison régionale | Barres horizontales triées | `Région` en lignes, `CA_Net` en valeurs | tri décroissant, Île-de-France en tête |
| Répartition par catégorie | Barres verticales ou secteurs | `Catégorie` en lignes, `CA_Net` en valeurs | 5 barres, secteurs si on veut les parts relatives |
| KPI isolé (CA, marge, commandes) | Cellule Excel liée au TCD | Cellule du TCD dédié | mise en forme de cellule (grande police, couleur de fond) |

Les graphiques de type jauge n'existent pas nativement dans Excel ; les remplacer par un KPI textuel (valeur en grande police + libellé en petit) ou un graphique en Anneau simulant une jauge.

**3c. Segments et chronologie**

Insérer au minimum deux segments et une chronologie depuis les TCD de l'onglet `Calculs`.

Segments recommandés : `Région` et `Catégorie` (ou `Segment_Client`). Chemin : **Analyse du tableau croisé dynamique > Insérer un segment** > cocher les champs voulus.

Chronologie : **Analyse du tableau croisé dynamique > Insérer une chronologie** > champ `Date`. Prérequis absolu : la colonne `Date` doit être intégralement de type Date (sans aucune cellule texte restante). Si la chronologie refuse de s'insérer, c'est que le défaut 2 n'a pas été corrigé.

**3d. Connexions de rapport — point critique**

Par défaut, un segment n'est connecté qu'au TCD depuis lequel il a été inséré. Un dashboard avec 4 TCD dont le segment ne filtre que le premier affiche des graphiques incohérents : le segment de Région change la courbe mensuelle mais pas l'histogramme catégoriel, par exemple.

Procédure de connexion : clic droit sur chaque segment > **Connexions de rapport** > cocher tous les TCD du dashboard. Répéter pour la chronologie.

Contrainte technique : la liste des TCD disponibles dans Connexions de rapport n'affiche que les TCD partageant le même cache de données — c'est-à-dire issus de la même source (`DonneesVentes`). Si l'apprenant a créé un TCD depuis une plage copiée-collée dans un autre onglet, ce TCD a son propre cache et ne peut pas partager les segments.

**Vérification en 10 secondes :** cliquer sur une valeur dans le segment (ex. : sélectionner « Nord »), puis vérifier que tous les graphiques du dashboard se mettent à jour simultanément. Si un graphique reste inchangé, sa connexion est manquante. Ouvrir **Connexions de rapport** de ce segment et cocher le TCD correspondant.

### Étape 4 — Revue critique (Auto-évaluation)

**Question 1 : « Un utilisateur qui n'a que 10 secondes comprend-il la performance globale ? »**

Une bonne réponse contient : les KPI principaux (CA net, taux de marge, nombre de commandes) sont visibles en haut du dashboard sans défilement, en police suffisamment grande pour être lus à distance ; la tendance mensuelle est lisible d'un coup d'œil (courbe propre, titre porteur d'un message, pas de légende superflue) ; l'absence de quadrillage et d'en-têtes de lignes/colonnes donne un rendu épuré.

**Question 2 : « Les couleurs sont-elles cohérentes et lisibles ? »**

Une bonne réponse contient : une même catégorie a la même couleur sur tous les graphiques (cohérence) ; le contraste est suffisant pour les personnes daltoniennes — pas de rouge/vert sans différenciation de forme ou de texture ; pas de dégradés ni d'effets 3D ; palette limitée à 5 ou 6 teintes distinctes.

**Question 3 : « L'IA a-t-elle été utilisée pour masquer une lacune technique ? »**

Une bonne réponse décrit un usage précis et vérifiable : « J'ai demandé à l'IA la formule pour convertir les dates textuelles, elle m'a proposé DATEVAL ; j'ai vérifié sur trois cellules que le résultat était bien un numéro de série, puis j'ai testé l'insertion de la chronologie. » Un recopiage se trahit si l'apprenant ne peut pas nommer les défauts qu'il a corrigés ni expliquer pourquoi DATEVAL (DATEVALUE) est nécessaire.

## 3. Valeurs de contrôle

| KPI | Valeur après nettoyage | Signal si la valeur diverge |
|---|---|---|
| CA net total | 384 439,39 € | Supérieur → doublons non supprimés |
| Marge totale | 150 775,59 € | — |
| Taux de marge | 39,22 % | — |
| Panier moyen | 427,15 € | — |
| Nombre de commandes | 900 | 906 → doublons non supprimés |
| Remise moyenne | 5,09 % | Supérieure → remises vides non imputées à 0 |
| CA Île-de-France | 107 349,86 € | Diverge → espaces parasites dans Région non supprimés |
| CA Électronique | 109 772,89 € | — |
| CA Sud | 68 034,49 € | — |
| Mois le plus élevé | déc. 2024 : 48 229,05 € | Décembre absent du TCD → dates textuelles non converties |
| Nombre de mois dans la série | 12 | Moins de 12 → dates textuelles non converties, certains mois non regroupés |

CA net par région (grille de correction complète) : Île-de-France 107 349,86 €, Sud 68 034,49 €, Ouest 65 595,48 €, Nord 60 524,26 €, Centre 41 862,09 €, Est 41 073,21 €.

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| Nombre de commandes = 906 au lieu de 900 | Doublons non supprimés | TCD > `ID_Commande` en Nombre : lire la valeur totale |
| La chronologie refuse de s'insérer | Colonne `Date` contient des cellules textuelles | Sélectionner la colonne `Date` : les cellules textes sont alignées à gauche |
| Le TCD des régions affiche deux lignes pour Île-de-France | Espaces parasites non supprimés | Filtrer la colonne `Région` : les doublons avec espace sont visibles dans la liste déroulante |
| Filtrer par segment ne change qu'un seul graphique | Connexions de rapport non complétées pour ce segment | Clic droit sur le segment > Connexions de rapport : vérifier les cases cochées |
| La remise moyenne affichée est surévaluée | Cellules `Remise` vides non imputées à 0 : la moyenne porte sur 895 lignes au lieu de 900 | Comparer avec la valeur attendue 5,09 % ; chercher des vides dans la colonne `Remise` |
| Décembre n'apparaît pas dans la courbe mensuelle ou apparaît comme texte | 10 dates textuelles non converties, le TCD les traite comme des entrées distinctes | Compter les points sur la courbe : si moins de 12, des dates ne sont pas groupées |
| Les segments ne proposent pas tous les TCD dans Connexions de rapport | TCD créés depuis des sources différentes (pas du même cache `DonneesVentes`) | Clic droit > Connexions de rapport : si un TCD n'apparaît pas dans la liste, il a une source distincte |
| La remise moyenne est calculée comme moyenne des taux unitaires | Formule `=MOYENNE(DonneesVentes[Remise])` au lieu de `Somme Remise / Nb lignes` | Comparer avec 5,09 % : si valeur différente, la méthode est incorrecte |

## 5. Volet IA

Ce qu'on attend dans la copie : au moins un usage documenté de l'IA (formule de conversion de date, suggestion de palette de couleurs, formule de taux de marge), avec mention que le résultat a été vérifié sur les données réelles.

Ce qui distingue un apprenant qui a compris : il explique pourquoi `DATEVAL` (DATEVALUE) est nécessaire — Excel stocke les dates comme numéros de série ; une chaîne de caractères n'est pas reconnue comme date par le moteur de groupement du TCD ni par la Chronologie — et il sait que la Chronologie vérifie le type de la colonne à l'insertion.

**Question de vérification orale :** « Vous avez inséré deux segments. Combien de TCD sont connectés à chacun, et comment avez-vous vérifié que le filtre Catégorie s'applique bien à la courbe mensuelle ? » Une bonne réponse décrit la procédure Connexions de rapport, cite le nombre de TCD cochés (au moins autant que le nombre de TCD présents dans le dashboard), et mentionne la vérification visuelle en cliquant sur une valeur du segment et en observant la mise à jour de tous les graphiques.

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Tableau structuré créé avec nom (`DonneesVentes`) | 1 | L'onglet Création de tableau affiche un nom et un style de tableau |
| Doublons supprimés (900 lignes restantes) | 1 | TCD > `ID_Commande` en Nombre = 900 |
| Dates textuelles converties (chronologie fonctionnelle) | 1 | La chronologie est présente et filtre effectivement |
| Espaces parasites supprimés dans Région | 1 | TCD sur Région : exactement 6 lignes, sans doublon de libellé |
| Remises manquantes imputées à 0 | 1 | Remise moyenne ≈ 5,09 % |
| 5 KPI avec TCD dédié chacun, valeurs conformes | 3 | 5 TCD distincts dans l'onglet Calculs, CA = 384 439,39 €, nb commandes = 900 |
| Feuille Dashboard avec quadrillage et en-têtes masqués | 1 | Mode d'affichage vérifié dans l'onglet Affichage |
| Graphiques adaptés au type de question (courbe pour tendance, barres pour comparaison) | 3 | Courbe pour la série mensuelle, barres horizontales pour la comparaison régionale |
| Au moins 2 segments + 1 chronologie insérés | 2 | Objets Segment et Chronologie présents sur la feuille Dashboard |
| Connexions de rapport complètes (tous les TCD cochés pour chaque segment) | 3 | Clic droit > Connexions de rapport : toutes les cases cochées ; vérification visuelle |
| Réponses à l'auto-évaluation (étape 4) avec arguments factuels | 2 | Note écrite dans le fichier ou argumentaire à l'oral mentionnant des faits vérifiables |
| Mise en forme cohérente (couleurs, titres porteurs d'un message, lisibilité) | 1 | Même couleur par catégorie sur l'ensemble du dashboard ; titres non descriptifs |
| **Total** | **20** | |

## 7. Prolongements

Connecter le tableau `DonneesVentes` à Power BI Desktop pour reproduire le dashboard et explorer les différences de paradigme : modèle de données relationnel avec DAX au lieu de formules de cellule, et publication sur le web en un clic.

Automatiser l'actualisation de tous les TCD via une macro VBA (`ActiveWorkbook.RefreshAll`) déclenchée à l'ouverture du fichier (`Workbook_Open`), puis protéger la feuille Dashboard contre les modifications accidentelles par mot de passe.

Ajouter une mise en forme conditionnelle sur les cellules KPI pour signaler les écarts par rapport à un objectif : vert si le CA mensuel dépasse la moyenne des 12 mois, rouge sinon, en utilisant une règle basée sur une formule faisant référence à la cellule de moyenne du TCD.
