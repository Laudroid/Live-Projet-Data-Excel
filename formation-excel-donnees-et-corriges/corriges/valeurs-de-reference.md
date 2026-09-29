
# Valeurs de reference — jeux de donnees de la formation Excel

Document **formateur**, non distribue aux apprenants.

Toutes les valeurs ci-dessous sont recalculees directement depuis les fichiers livres par `python3 verifier_donnees.py`. Elles servent a corriger sans refaire le TP, et a detecter qu'un apprenant a saute une etape de nettoyage : les ecarts de CA sont signes.

## Exercices A1 et B1 — `ventes_brutes.csv`

Fichier livre en UTF-8 **sans BOM**, separateur `;`, 1 lignes d'en-tete + 422 lignes de donnees dont 2 lignes entierement vides.

| Controle | Valeur attendue |
|---|---|
| Lignes de donnees (y compris lignes vides) | 422 |
| Lignes exploitables (ID_Vente renseigne) | 420 |
| Colonnes | 14 |
| Lignes entierement vides | 2 |
| Dates au format `JJ/MM/AAAA` | 257 |
| Dates au format `AAAA.MM.JJ` | 108 |
| Dates au format `J-mmm-AA` | 55 |
| Dates aberrantes (annee > 2025) | 3 (7-févr-38, 12/05/2035, 2041.11.03) |
| Montants vides | 6 |
| Montants textuels | 5 (-, N/A, NON COMMUNIQUE, erreur import, à valider) |
| Montants avec espace insecable | 22 |
| Montants a point decimal | 59 |
| Libelles `Client` a nettoyer | 83 |
| `ID_Client` manquants | 5 |
| Clients distincts (hors vides) | 95 |
| Plage de dates plausible | 04/01/2023 au 31/12/2023 |

**Valeurs de controle apres nettoyage** (les 11 lignes a montant vide ou textuel etant exclues du calcul) :

| Indicateur | Valeur |
|---|---|
| Lignes a montant exploitable | 409 |
| CA total | 188 322,80 € |
| Montant median (pour imputation) | 387,00 € |
| Montant moyen | 460,45 € |

Repartition par categorie (etape « distribution » de l'exercice A1) :

| Categorie | Nb de ventes | CA |
|---|---|---|
| Électroménager | 72 | 47 926,70 € |
| Électronique | 88 | 47 325,40 € |
| Téléphonie | 86 | 37 663,60 € |
| Mobilier | 44 | 32 200,00 € |
| Papeterie | 119 | 23 207,10 € |

Identifiants des lignes porteuses d'au moins une anomalie (hors format de date ou d'espace) : `V00003`, `V00034`, `V00065`, `V00090`, `V00158`, `V00214`, `V00233`, `V00236`, `V00239`, `V00266`, `V00271`, `V00311`, `V00328`, `V00347`, `V00360`, `V00368`, `V00381`, `V00390`, `V00403`.

## Exercice A2 — `clients_brut.xlsx`

| Controle | Valeur attendue |
|---|---|
| Lignes | 195 |
| Colonnes | 9 |
| Clients reellement distincts | 180 |
| Doublons a supprimer | 15 |
| dont doublons detectables sans nettoyage prealable | 8 |
| dont doublons masques par la casse ou les espaces | 7 |
| Noms a nettoyer (espaces parasites) | 124 |
| Noms en capitales integrales | 36 |
| Telephones vides | 16 |
| Telephones a « non renseigné » | 9 |
| Telephones numeriques (zero initial perdu) | 15 |
| Adresses a ville composee (tiret) | 23 |
| Codes postaux distincts | 25 |

**Point de vigilance pedagogique.** Sur les 15 doublons, seuls 8 sont visibles si l'apprenant applique `Supprimer les doublons` directement sur les colonnes brutes. Les 7 autres ne se revelent qu'apres `NOMPROPRE(SUPPRESPACE(...))` : c'est ce qui justifie l'ordre des etapes de l'enonce.

Couples en doublon (a verifier lors de la correction) :

| ID_Client | Nom saisi | Email |
|---|---|---|
| CLI0087 | BLANCHARD CAMILLE | camille.blanchard@courriel-demo.net |
| CLI0171 | BLANCHARD CAMILLE | camille.blanchard@courriel-demo.net |
| CLI0058 | Delaunay  Lucie | lucie.delaunay@example.com |
| CLI0114 | Delaunay  Lucie | lucie.delaunay@example.com |
| CLI0176 |   dumas  marion  | marion.dumas@societe-demo.fr |
| CLI0049 |   dumas  marion  | marion.dumas@societe-demo.fr |
| CLI0117 |   estève  pierre-yves  | pierre-yves.esteve@mail-test.fr |
| CLI0184 | Estève Pierre-Yves | pierre-yves.esteve@mail-test.fr |
| CLI0034 |   garnier  amandine  | amandine.garnier@mail-test.fr |
| CLI0158 | Garnier Amandine | amandine.garnier@mail-test.fr |
| CLI0033 |   garnier  anaïs  | anais.garnier@courriel-demo.net |
| CLI0113 | Garnier Anaïs | anais.garnier@courriel-demo.net |
| CLI0162 |   leroy  mehdi  | mehdi.leroy@mail-test.fr |
| CLI0053 |   leroy  mehdi  | mehdi.leroy@mail-test.fr |
| CLI0161 | Leroy  Naïma | naima.leroy@societe-demo.fr |
| CLI0015 | Leroy  Naïma | naima.leroy@societe-demo.fr |
| CLI0060 | MERCIER Lucie  | lucie.mercier@atelier-nordique.fr |
| CLI0095 |   mercier  lucie  | lucie.mercier@atelier-nordique.fr |
| CLI0056 | MERCIER MARION | marion.mercier@atelier-nordique.fr |
| CLI0022 | MERCIER MARION | marion.mercier@atelier-nordique.fr |
| CLI0008 |   nguyen  étienne  | etienne.nguyen@mail-test.fr |
| CLI0122 |   nguyen  étienne  | etienne.nguyen@mail-test.fr |
| CLI0167 | Ozanne  Fatima | fatima.ozanne@courriel-demo.net |
| CLI0105 |   ozanne  fatima  | fatima.ozanne@courriel-demo.net |
| CLI0149 | Ozanne Nora | nora.ozanne@courriel-demo.net |
| CLI0182 |   ozanne  nora  | nora.ozanne@courriel-demo.net |
| CLI0106 |   renaud  hugo  | hugo.renaud@atelier-nordique.fr |
| CLI0067 |   renaud  hugo  | hugo.renaud@atelier-nordique.fr |
| CLI0038 | Riviere  Léa | lea.riviere@atelier-nordique.fr |
| CLI0139 |   riviere  léa  | lea.riviere@atelier-nordique.fr |

## Exercice B2 — `Ventes_Projet.xlsx`

| Controle | Valeur attendue |
|---|---|
| Lignes | 600 |
| Colonnes fournies | 10 |
| Tableau structure | oui, nomme `Ventes` |
| Plage | 01/01/2023 au 31/12/2024 |
| Mois distincts | 24 |
| CA total | 274 527,30 € |
| CA 2023 | 137 863,10 € |
| CA 2024 | 136 664,20 € |

Croissance 2024 vs 2023 : **-0,87 %**.

CA par cle `Mois-Annee` (resultat attendu du TCD) :

| Mois-Annee (`TEXTE(...;"mmm-aaaa")`) | Cle de tri (`ANNEE*100+MOIS`) | CA |
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

Mois le plus performant : **déc. 2023** avec 17 007,50 €.

Ordre alphabetique trompeur : trie comme du texte, la cle `mmm-aaaa` place `avr.-2023` avant `janv.-2023`. C'est exactement le piege que la colonne d'index `ANNEE*100+MOIS` resout.

## Exercice A3 — `Ventes.xlsx` + `Referentiel.xlsx`

| Controle | Valeur attendue |
|---|---|
| Lignes de `Ventes.xlsx` | 260 |
| Plage | 01/10/2024 au 31/12/2024 |
| References au catalogue Produits | 33 |
| Magasins au referentiel | 12 |
| Lignes a produit orphelin | 4 (codes P512, P998) |
| Lignes a magasin orphelin | 3 (code MAG21) |
| Lignes en `#N/A` sur au moins une recherche | 7 |
| CA total, lignes orphelines exclues | 114 667,60 € |
| CA total si les `#N/A` sont neutralises a 0 | 115 528,70 € |

**Partie 2, question 1** — CA par region (`SOMME.SI.ENS`) :

| Region | CA |
|---|---|
| Île-de-France | 30 118,30 € |
| Ouest | 20 675,30 € |
| Nord | 19 076,90 € |
| Sud | 17 223,60 € |
| Centre | 15 703,80 € |
| Est | 11 869,70 € |

**Partie 2, question 2** — nombre de transactions de plus de 10 unites (`NB.SI.ENS`) :

| Region | Nb de transactions > 10 unites |
|---|---|
| Centre | 11 |
| Est | 8 |
| Nord | 20 |
| Ouest | 17 |
| Sud | 17 |
| Île-de-France | 30 |

Total sur l'ensemble des regions : **103 transactions** de plus de 10 unites, sur 253 lignes exploitables.

**Partie 2, question 3** — analyse croisee produit x region. Trois couples utilisables comme consigne de correction :

| Produit | Region | Nb de lignes | CA |
|---|---|---|---|
| Écran 27 pouces Lumen | Ouest | 3 | 3 290,00 € |
| Fauteuil visiteur Accueil | Île-de-France | 3 | 2 835,00 € |
| Réfrigérateur d'appoint Fraîcheur | Centre | 3 | 2 511,00 € |
| Chaise de bureau Assise | Île-de-France | 3 | 2 241,00 € |
| Disque SSD 1 To Silex | Sud | 3 | 2 180,00 € |
| Clavier mécanique Frappe | Ouest | 3 | 2 151,00 € |

## Exercice B3 — `Suivi_Marges.xlsx`

| Controle | Valeur attendue |
|---|---|
| Onglets | `Catalogue`, `Saisies`, `Recherche` |
| References au catalogue | 33 |
| Lignes de saisie | 120 |
| Colonnes a completer | `Prix_Vente_Catalogue (à compléter)`, `Marge_Unitaire (à compléter)`, `Taux_Atteinte_Objectif (à compléter)` |
| Lignes generant `#N/A` (code introuvable) | 9 (codes P777, P812, P950) |
| Lignes generant `#DIV/0!` sur la marge unitaire | 7 |
| Lignes generant `#DIV/0!` sur le taux d'atteinte | 6 |
| References a prix de vente nul | 2 (P105, P304) |
| Total de cellules en erreur avant traitement | 22 |

**Onglet `Recherche`** — valeurs attendues pour les trois codes de test :

| Code saisi en B3 | Designation | Prix de vente | Taux de marge | Cas teste |
|---|---|---|---|---|
| `P003` | Écran 27 pouces Lumen | 329,00 € | 34,95 % | cas nominal |
| `P105` | Étagère modulaire Strate | 0,00 € | `#DIV/0!` a intercepter | prix de vente a 0 |
| `P777` | `#N/A` a intercepter | `#N/A` a intercepter | `#N/A` a intercepter | code absent du catalogue |

## Exercice A4 — `Ventes_Globales.xlsx`

| Controle | Valeur attendue |
|---|---|
| Lignes | 1600 |
| Colonnes | 6 |
| Forme livree | plage simple — le `Ctrl+T` est a la charge de l'apprenant |
| Plage | 01/01/2023 au 31/12/2024 |
| CA total | 705 440,90 € |
| Regions | 6 |
| Categories | 5 |
| Vendeurs | 12 |

**TCD 1 — saisonnalite par region.** Coefficient de variation du CA mensuel (ecart-type / moyenne, 24 mois cumules par mois calendaire) : plus il est eleve, plus la region est saisonniere.

| Region | CA total | Coefficient de variation mensuel |
|---|---|---|
| Sud | 148 678,00 € | 68,92 % |
| Ouest | 102 553,60 € | 41,38 % |
| Nord | 102 302,60 € | 39,94 % |
| Est | 91 215,90 € | 37,31 % |
| Centre | 76 066,80 € | 32,33 % |
| Île-de-France | 184 624,00 € | 21,67 % |

Reponse attendue : **Sud** est la region la plus saisonniere, **Île-de-France** la plus stable.

**TCD 2 — performance par categorie**, trie decroissant sur le CA :

| Categorie | CA | Quantite moyenne |
|---|---|---|
| Électronique | 185 924,40 € | 5,97 |
| Électroménager | 169 397,00 € | 4,93 |
| Téléphonie | 151 224,80 € | 11,03 |
| Mobilier | 107 302,00 € | 3,63 |
| Papeterie | 91 592,70 € | 33,37 |

**TCD 3 — analyse des vendeurs** (sans filtre de region ni de categorie) :

| Vendeur | CA |
|---|---|
| Camille Fournier | 99 421,80 € |
| Léa Bonnet | 89 742,70 € |
| Yanis Perrot | 87 529,30 € |
| Hugo Marchand | 85 202,20 € |
| Claire Vasseur | 73 642,40 € |
| Nora Lefèvre | 63 436,40 € |
| Samir Haddad | 58 935,30 € |
| Inès Moreau | 57 736,50 € |
| Malik Benali | 44 817,10 € |
| Thomas Girard | 38 866,20 € |
| Bastien Roux | 3 686,60 € |
| Sofia Renard | 2 424,40 € |

Detail du profil mensuel de la region la plus saisonniere (Sud), cumul des deux annees :

| Mois | CA cumule |
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

## Exercice B4 — `Data_Ventes.csv` (Google Sheets)

| Controle | Valeur attendue |
|---|---|
| Lignes | 320 |
| Colonnes | A Date, B Catégorie, C Produit, D Vendeur, E Montant, F Région |
| Encodage | UTF-8 avec BOM, separateur virgule |
| Montants | euros entiers, sans decimale |
| Plage | 02/01/2024 au 31/12/2024 |
| CA total | 147 934,00 € |
| Categories | Mobilier, Papeterie, Téléphonie, Électroménager, Électronique |
| Regions | Centre, Est, Nord, Ouest, Sud, Île-de-France |
| Vendeurs | 12 |

**Exercice 1 — filtrage multi-criteres.** Categorie « Électronique », montant strictement superieur a 500, region « Nord » ou « Sud » :

| Indicateur | Valeur |
|---|---|
| Lignes renvoyees | 13 |
| Somme des montants | 8 951,00 € |
| Montant minimum renvoye | 549 |
| Montant maximum renvoye | 987 |
| dont region Nord | 9 |
| dont region Sud | 4 |

**Exercice 2 — agregation, tri et `HAVING`.** Total par vendeur, trie decroissant :

| Vendeur | Somme des montants | Retenu par `HAVING > 1000` ? |
|---|---|---|
| Camille Fournier | 28 119,00 € | oui |
| Claire Vasseur | 19 422,00 € | oui |
| Hugo Marchand | 13 332,00 € | oui |
| Nora Lefèvre | 13 060,00 € | oui |
| Thomas Girard | 13 038,00 € | oui |
| Malik Benali | 12 892,00 € | oui |
| Inès Moreau | 11 996,00 € | oui |
| Samir Haddad | 11 906,00 € | oui |
| Yanis Perrot | 11 288,00 € | oui |
| Léa Bonnet | 11 189,00 € | oui |
| Bastien Roux | 1 167,00 € | oui |
| Sofia Renard | 525,00 € | **non** |

La requete de l'exercice 2 doit donc renvoyer **11 lignes** : Sofia Renard est exclu par la clause `HAVING`.

**Exercice 3 — filtrage dynamique.** Combinaisons categorie x region a proposer comme jeu de test, avec le nombre de lignes attendu :

| Categorie | Centre | Est | Nord | Ouest | Sud | Île-de-France |
|---|---|---|---|---|---|---|
| Mobilier | 9 | 5 | 6 | 6 | 4 | 11 |
| Papeterie | 12 | 11 | 18 | 14 | 23 | 16 |
| Téléphonie | 6 | 5 | 7 | 9 | 12 | 22 |
| Électroménager | 8 | 6 | 12 | 16 | 8 | 13 |
| Électronique | 7 | 7 | 15 | 6 | 9 | 17 |

## Exercice A5 — `Ventes_Nettoyees.xlsx`

| Controle | Valeur attendue |
|---|---|
| Lignes | 820 |
| Colonnes | 15 |
| Tableau structure | oui, nomme `DonneesNettoyees` |
| Valeurs manquantes | 0 |
| Colonnes temporelles deja derivees | `Année`, `Mois`, `Nom_Mois`, `Mois_Année` |
| CA total | 358 918,60 € |
| Marge totale | 152 433,90 € |
| Taux de marge global | 42,47 % |

**Pattern 1 — saisonnalite.** CA par mois calendaire, cumul des deux annees, par categorie. Le pic de rentree de la papeterie (aout-septembre), le pic de fin d'annee de l'electronique et de la telephonie et le pic estival de l'electromenager sont reellement dans les donnees.

| Mois | Mobilier | Papeterie | Téléphonie | Électroménager | Électronique |
|---|---|---|---|---|---|
| janv. | 4 985,00 | 3 230,60 | 2 736,00 | 5 829,20 | 10 469,20 |
| févr. | 1 377,50 | 2 331,80 | 2 531,10 | 10 536,10 | 6 258,70 |
| mars | 5 987,50 | 2 038,20 | 3 585,40 | 2 492,00 | 10 267,90 |
| avr. | 2 574,00 | 3 864,70 | 4 326,10 | 7 432,10 | 6 094,30 |
| mai | 6 074,00 | 5 537,60 | 5 358,20 | 4 783,90 | 8 675,20 |
| juin | 2 362,50 | 3 290,20 | 5 172,60 | 8 786,60 | 8 163,60 |
| juil. | 3 488,50 | 2 360,20 | 5 208,90 | 8 789,30 | 8 751,30 |
| août | 6 043,50 | 7 182,80 | 6 081,90 | 13 375,50 | 8 205,20 |
| sept. | 2 979,00 | 6 912,40 | 7 220,20 | 4 646,10 | 11 467,70 |
| oct. | 5 247,00 | 4 919,20 | 2 838,90 | 1 930,80 | 11 667,20 |
| nov. | 4 258,50 | 3 563,50 | 4 478,90 | 7 346,00 | 12 363,00 |
| déc. | 6 759,50 | 2 339,80 | 9 858,20 | 9 949,20 | 11 534,60 |

**Pattern 2 — ecart entre regions.** CA par region :

| Region | CA | Part du total |
|---|---|---|
| Île-de-France | 93 302,60 € | 26,00 % |
| Sud | 69 435,60 € | 19,35 % |
| Nord | 57 346,50 € | 15,98 % |
| Est | 47 576,30 € | 13,26 % |
| Ouest | 46 085,50 € | 12,84 % |
| Centre | 45 172,10 € | 12,59 % |

**Pattern 3 — correlation prix / quantite.** Coefficient de Pearson : **r = -0,54** sur 820 points. La relation est decroissante et non lineaire : plus le prix unitaire monte, plus les quantites par transaction chutent. Un nuage de points `Prix_Unitaire` en X et `Quantité` en Y le montre nettement ; une echelle logarithmique sur X ameliore encore la lecture.

Repartition par categorie (pour l'histogramme de comparaison) :

| Categorie | CA | Nb de transactions |
|---|---|---|
| Électronique | 113 917,90 | 199 |
| Électroménager | 85 896,80 | 139 |
| Téléphonie | 59 396,40 | 149 |
| Mobilier | 52 136,50 | 72 |
| Papeterie | 47 571,00 | 261 |

Serie mensuelle complete (pour la courbe d'evolution), 24 points :

| Mois_Année | CA |
|---|---|
| 2023-01 | 11 346,40 € |
| 2023-02 | 10 953,10 € |
| 2023-03 | 16 325,00 € |
| 2023-04 | 14 002,00 € |
| 2023-05 | 14 114,10 € |
| 2023-06 | 10 265,80 € |
| 2023-07 | 13 674,70 € |
| 2023-08 | 24 732,40 € |
| 2023-09 | 16 457,80 € |
| 2023-10 | 14 355,00 € |
| 2023-11 | 15 374,90 € |
| 2023-12 | 18 326,80 € |
| 2024-01 | 15 903,60 € |
| 2024-02 | 12 082,10 € |
| 2024-03 | 8 046,00 € |
| 2024-04 | 10 289,20 € |
| 2024-05 | 16 314,80 € |
| 2024-06 | 17 509,70 € |
| 2024-07 | 14 923,50 € |
| 2024-08 | 16 156,50 € |
| 2024-09 | 16 767,60 € |
| 2024-10 | 12 248,10 € |
| 2024-11 | 16 635,00 € |
| 2024-12 | 22 114,50 € |

## Exercice B5 — `Dashboard_Source.xlsx`

| Controle | Valeur attendue |
|---|---|
| Lignes livrees | 906 |
| Colonnes | 15 |
| Forme livree | plage simple — le `Ctrl+T` est a la charge de l'apprenant |
| Doublons stricts a supprimer | 6 |
| Dates saisies en texte (bloquent le groupement du TCD) | 10 |
| Libelles `Région` a nettoyer (espace parasite) | 8 |
| Remises manquantes | 5 |
| Lignes apres dedoublonnage | 900 |

**KPI de reference apres nettoyage** (doublons supprimes, regions detassees, dates converties) :

| KPI | Valeur |
|---|---|
| CA net total | 384 439,39 € |
| Marge totale | 150 775,59 € |
| Taux de marge | 39,22 % |
| Panier moyen | 427,15 € |
| Nombre de commandes | 900 |
| Quantite totale vendue | 13418 |
| Remise moyenne accordee | 5,09 % |

CA net par region :

| Région | CA net |
|---|---|
| Île-de-France | 107 349,86 € |
| Sud | 68 034,49 € |
| Ouest | 65 595,48 € |
| Nord | 60 524,26 € |
| Centre | 41 862,09 € |
| Est | 41 073,21 € |

CA net par categorie :

| Catégorie | CA net |
|---|---|
| Électronique | 109 772,89 € |
| Électroménager | 97 990,34 € |
| Téléphonie | 65 231,07 € |
| Mobilier | 62 115,19 € |
| Papeterie | 49 329,90 € |

CA net par magasin :

| Magasin | CA net |
|---|---|
| Atelier Paris Réaumur | 55 248,66 € |
| Atelier Créteil Soleil | 52 101,20 € |
| Atelier Marseille Prado | 34 527,22 € |
| Atelier Lille Grand Place | 34 133,12 € |
| Atelier Toulouse Capitole | 33 507,27 € |
| Atelier Nantes Graslin | 33 293,91 € |
| Atelier Rennes Sainte-Anne | 32 301,57 € |
| Atelier Amiens Rivery | 26 391,14 € |
| Atelier Tours Nationale | 24 524,99 € |
| Atelier Dijon Darcy | 22 014,71 € |
| Atelier Strasbourg Krutenau | 19 058,50 € |
| Atelier Orléans Martroi | 17 337,10 € |

CA net par segment client :

| Segment_Client | CA net |
|---|---|
| Administration | 80 285,13 € |
| TPE | 79 622,52 € |
| Grand compte | 77 969,42 € |
| PME | 77 768,24 € |
| Particulier | 68 794,08 € |

Serie mensuelle du CA net (12 points, pour la courbe de tendance du dashboard) :

| Mois | CA net |
|---|---|
| 2024-01 | 30 069,82 € |
| 2024-02 | 25 101,19 € |
| 2024-03 | 27 206,81 € |
| 2024-04 | 34 230,10 € |
| 2024-05 | 30 156,28 € |
| 2024-06 | 28 637,56 € |
| 2024-07 | 34 414,62 € |
| 2024-08 | 29 257,18 € |
| 2024-09 | 33 610,13 € |
| 2024-10 | 27 991,87 € |
| 2024-11 | 35 534,78 € |
| 2024-12 | 48 229,05 € |

## Exercices A6 et B6 — `ventes_2023.csv`

| Controle | Valeur attendue |
|---|---|
| Lignes livrees | 1522 |
| Doublons stricts | 23 |
| Dates au format `AAAA-MM-JJ` (texte) | 180 |
| Dates au format `JJ/MM/AAAA` | 1342 |
| Quantites aberrantes (9 999 / 4 500) | 6 |
| Quantites negatives (retours mal saisis) | 3 |
| Prix unitaires aberrants (0,01 €) | 4 |
| Lignes retenues apres nettoyage | 1486 |
| Lignes ecartees | 36 |
| CA total apres nettoyage | 655 953,60 € |
| Marge brute totale | 276 667,80 € |

**Q1 — tendance mensuelle du CA par categorie.**

| Mois | Mobilier | Papeterie | Téléphonie | Électroménager | Électronique | Total |
|---|---|---|---|---|---|---|
| janvier | 8 454,00 | 6 429,40 | 11 260,50 | 6 917,20 | 8 647,40 | 41 708,50 |
| février | 6 948,00 | 4 799,80 | 11 196,60 | 13 966,90 | 12 268,00 | 49 179,30 |
| mars | 5 947,50 | 5 042,70 | 12 757,80 | 12 544,10 | 15 536,50 | 51 828,60 |
| avril | 10 279,00 | 5 827,60 | 8 881,00 | 9 257,40 | 8 178,40 | 42 423,40 |
| mai | 9 153,50 | 5 107,90 | 10 262,40 | 13 027,70 | 11 861,30 | 49 412,80 |
| juin | 8 757,00 | 6 077,00 | 9 767,30 | 22 891,10 | 11 710,10 | 59 202,50 |
| juillet | 4 824,00 | 5 527,30 | 9 781,00 | 12 435,20 | 17 341,30 | 49 908,80 |
| août | 7 397,00 | 12 873,40 | 11 303,10 | 13 327,20 | 14 095,20 | 58 995,90 |
| septembre | 12 160,50 | 11 516,00 | 13 845,20 | 13 073,80 | 15 916,20 | 66 511,70 |
| octobre | 10 843,00 | 7 483,00 | 11 613,40 | 7 589,20 | 17 102,30 | 54 630,90 |
| novembre | 7 382,00 | 9 013,50 | 11 652,30 | 12 388,00 | 21 699,10 | 62 134,90 |
| décembre | 7 708,00 | 5 500,30 | 21 606,20 | 13 506,00 | 21 695,80 | 70 016,30 |

Mois le plus performant, toutes categories confondues : **décembre** avec 70 016,30 €. Par categorie, le mois de pointe differe : Mobilier en septembre ; Papeterie en août ; Téléphonie en décembre ; Électroménager en juin ; Électronique en novembre.

**Q2 — top 3 des produits les plus rentables par region** (marge brute = quantite x (prix de vente - cout d'achat)).

Region **Centre** :

| Rang | Produit | Marge brute |
|---|---|---|
| 1 | Bureau réglable Altitude | 2 136,00 € |
| 2 | Casque Bluetooth Aria | 2 045,80 € |
| 3 | Batterie externe Réserve | 1 838,20 € |

Region **Est** :

| Rang | Produit | Marge brute |
|---|---|---|
| 1 | Réfrigérateur d'appoint Fraîcheur | 2 288,00 € |
| 2 | Smartphone Signal | 2 006,00 € |
| 3 | Webcam HD Regard | 1 844,40 € |

Region **Nord** :

| Rang | Produit | Marge brute |
|---|---|---|
| 1 | Smartphone Signal | 2 950,00 € |
| 2 | Réfrigérateur d'appoint Fraîcheur | 2 552,00 € |
| 3 | Batterie externe Réserve | 2 161,40 € |

Region **Ouest** :

| Rang | Produit | Marge brute |
|---|---|---|
| 1 | Machine à café Arôme | 2 660,00 € |
| 2 | Aspirateur balai Souffle | 2 414,00 € |
| 3 | Smartphone Signal | 2 360,00 € |

Region **Sud** :

| Rang | Produit | Marge brute |
|---|---|---|
| 1 | Smartphone Signal | 3 540,00 € |
| 2 | Bureau réglable Altitude | 3 204,00 € |
| 3 | Casque Bluetooth Aria | 2 817,80 € |

Region **Île-de-France** :

| Rang | Produit | Marge brute |
|---|---|---|
| 1 | Smartphone Signal | 4 838,00 € |
| 2 | Casque Bluetooth Aria | 4 786,40 € |
| 3 | Câble tressé Lien | 4 419,80 € |

**Q3 — performance des vendeurs par region.** Chaque vendeur n'opere que sur une region : la question de l'enonce est un piege methodologique, il n'y a pas de correlation a mesurer mais un effet de structure a identifier. Le CA d'un vendeur est d'abord determine par le poids commercial de sa region.

| Region | Vendeur | CA | Nb de lignes | Panier moyen |
|---|---|---|---|---|
| Île-de-France | Camille Fournier | 99 293,10 € | 200 | 496,47 € |
| Sud | Léa Bonnet | 78 634,60 € | 148 | 531,31 € |
| Est | Yanis Perrot | 75 738,70 € | 197 | 384,46 € |
| Île-de-France | Hugo Marchand | 74 232,70 € | 179 | 414,71 € |
| Centre | Claire Vasseur | 65 802,30 € | 145 | 453,81 € |
| Nord | Nora Lefèvre | 62 505,80 € | 127 | 492,17 € |
| Ouest | Inès Moreau | 58 623,30 € | 122 | 480,52 € |
| Sud | Samir Haddad | 57 214,30 € | 143 | 400,10 € |
| Nord | Thomas Girard | 38 952,50 € | 112 | 347,79 € |
| Ouest | Malik Benali | 36 132,70 € | 94 | 384,39 € |
| Centre | Sofia Renard | 6 565,90 € | 13 | 505,07 € |
| Est | Bastien Roux | 2 257,70 € | 6 | 376,28 € |

**Q4 — taux de croissance du CA entre le premier et le dernier trimestre.**

| Trimestre | CA |
|---|---|
| T1 | 142 716,40 € |
| T2 | 151 038,70 € |
| T3 | 175 416,40 € |
| T4 | 186 782,10 € |

Taux de croissance T4 / T1 : **+30,88 %** (186 782,10 € contre 142 716,40 €).

Sensibilite au nettoyage : si les valeurs aberrantes ne sont PAS retirees, le CA total passe a 3 452 709,09 € et le taux T4/T1 a 1748,70 %. L'ecart justifie a lui seul l'etape 1 de l'enonce.
