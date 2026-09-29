# Corrigé — Présenter les résultats

**Fichier(s) de données :** Aucun fichier propre — la matière est issue de l'analyse de `ventes_2023.csv` (exercice précédent).
**Durée indicative :** 60 min
**Prérequis :** Avoir produit les quatre résultats de l'exercice « Résoudre un problème data métier » ; connaître les principes élémentaires de présentation (titre porteur de message, un graphique par message).

---

## 1. Ce que l'exercice évalue réellement

L'exercice évalue la capacité à transformer des chiffres corrects en narration compréhensible par un décideur qui n'a pas vu le fichier Excel. Le piège n'est pas technique mais rhétorique : l'apprenant dispose de résultats valides mais peut les présenter de manière opaque (titre descriptif, graphique sans conclusion) ou, pire, construire un argument séduisant sur des données mal interprétées (le classement des vendeurs). Un corrigé de restitution ne porte pas sur des formules : il porte sur la qualité de la narration et la fidélité des chiffres cités.

---

## 2. Structure de référence de la présentation

L'énoncé demande 3 à 5 slides en 5 minutes. La structure attendue est constat / découverte / recommandation. Ci-dessous, une version de référence slide par slide, avec des titres construits sur les vrais chiffres du jeu de données.

---

### Slide 1 — Le constat : un CA de 655 954 € sur 12 mois, avec un T4 en forte accélération

**Rôle.** Poser le contexte et le périmètre de l'analyse. Le chiffre du titre ancre immédiatement la crédibilité : le jury peut le retrouver dans l'onglet `Calculs`.

**Contenu attendu.**
- CA annuel total après nettoyage : 655 953,60 €.
- Évolution trimestrielle : T1 à 142 716,40 €, T4 à 186 782,10 €, soit +30,88 % de croissance.
- Une phrase sur la qualité des données : 36 lignes écartées (23 doublons, 6 quantités aberrantes, 4 prix à 0,01 €, 3 quantités négatives), avec mention du choix retenu pour les retours.

**Ce qui doit y figurer.** La courbe ou le graphique en barres du CA mensuel total (12 points, janvier à décembre), sans filtre de catégorie. La courbe ascendante de T1 à T4 est le fil directeur de toute la présentation.

---

### Slide 2 — La découverte : chaque catégorie a son propre mois de pointe

**Rôle.** C'est l'insight le plus fin de l'analyse. Dire « décembre est le meilleur mois » est exact mais incomplet. La slide doit montrer que les stratégies d'approvisionnement et de promotion ne peuvent pas être uniformes.

**Titre porteur de message :** « Les mois de pointe divergent selon la catégorie : juin pour l'Électroménager, août pour la Papeterie, novembre pour l'Électronique ».

**Principe un message par slide — avant/après.**

Titre faible (descriptif) : « Évolution du CA par catégorie et par mois ».

Titre fort (conclusion chiffrée) : « L'Électroménager culmine en juin (22 891,10 €) tandis que l'Électronique attend novembre (21 699,10 €) ».

Le titre fort permet à un décideur qui ne lit que les titres de comprendre la recommandation sans ouvrir le graphique.

**Contenu attendu.**
- Un graphique en courbes ou en barres groupées, catégories en séries de couleurs distinctes, mois en abscisse.
- Les valeurs de pointe annotées : Électroménager juin 22 891,10 €, Papeterie août 12 873,40 €, Mobilier septembre 12 160,50 €, Téléphonie décembre 21 606,20 €, Électronique novembre 21 699,10 €.
- Une légende lisible sans zoom.

---

### Slide 3 — La recommandation : concentrer les efforts sur les 3 produits à plus forte marge

**Rôle.** Passer de l'observation à l'action. La recommandation doit être directement étayée par les chiffres de Q2.

**Titre porteur de message :** « Le Smartphone Signal génère la marge brute la plus élevée dans 4 régions sur 6 : c'est le levier prioritaire ».

**Contenu attendu.**
- Tableau ou graphique du top 3 de la marge brute pour deux ou trois régions représentatives (Île-de-France et Sud suffisent, elles couvrent le chiffre d'affaires le plus élevé).
- Exemple Île-de-France : Smartphone Signal 4 838,00 €, Casque Bluetooth Aria 4 786,40 €, Câble tressé Lien 4 419,80 €.
- Exemple Sud : Smartphone Signal 3 540,00 €, Bureau réglable Altitude 3 204,00 €, Casque Bluetooth Aria 2 817,80 €.
- Une recommandation opérationnelle : anticiper les stocks de Smartphone Signal avant le T4 (pic de croissance +30,88 % entre T1 et T4) pour éviter les ruptures lors du pic de novembre-décembre en Électronique.

---

### Slide 4 (optionnelle) — Slide de synthèse : les 3 chiffres à retenir

**Rôle.** Récapitulatif pour le décideur pressé. Trois bullets, trois chiffres, trois actions.

Structure de référence :
- « +30,88 % de croissance T4/T1 — renforcer les effectifs terrain en fin d'année. »
- « Électroménager : pic en juin (22 891,10 €) — avancer les négociations fournisseurs au printemps. »
- « Smartphone Signal : top marge dans 4 régions sur 6 — prioriser la disponibilité de ce produit à l'échelle nationale. »

---

### L'insight faux mais séduisant : le classement des vendeurs

**Ce que certains apprenants présentent.** Un graphique de barres trié par CA vendeur, avec Camille Fournier en tête (99 293,10 €) et Bastien Roux en queue (2 257,70 €), présenté comme un « classement de performance commerciale ».

**Pourquoi c'est faux.** Chaque vendeur n'opère que sur une région. L'écart entre Camille Fournier et Bastien Roux reflète d'abord le poids commercial de l'Île-de-France versus l'Est, et le nombre de transactions (200 contre 6). Ce n'est pas une comparaison de performance individuelle, c'est une comparaison de marchés.

**Comment un jury doit challenger cet apprenant.** Trois questions suffisent :
1. « Si vous déplaciez Bastien Roux en Île-de-France, son CA resterait-il à 2 257,70 € ? »
2. « Quel indicateur permettrait de comparer equitablement deux vendeurs opérant dans des régions différentes ? »
3. « Sofia Renard a un CA de 6 565,90 € pour 13 transactions. Son panier moyen est de 505,07 €. Camille Fournier a un panier de 496,47 €. Qui est le plus performant en valeur par acte de vente ? »

Un apprenant qui ne sait pas répondre à ces trois questions a copié un graphique sans analyser les données.

---

## 3. Valeurs de contrôle

Chiffres que le jury doit pouvoir retrouver dans la présentation. Leur présence ou absence permet de vérifier que l'apprenant a réellement fait l'analyse, pas seulement récupéré des captures d'écran.

| Chiffre | Valeur exacte | Où il doit apparaître |
|---|---|---|
| CA annuel total | 655 953,60 € | Slide 1, titre ou sous-titre |
| Lignes retenues après nettoyage | 1 486 | Slide 1, note méthodologique |
| Taux de croissance T4/T1 | +30,88 % | Slide 1 ou slide de synthèse |
| CA T4 | 186 782,10 € | Slide 1 ou calcul de croissance |
| CA T1 | 142 716,40 € | Slide 1 ou calcul de croissance |
| Pic Électroménager | juin, 22 891,10 € | Slide 2 |
| Pic Électronique | novembre, 21 699,10 € | Slide 2 |
| Pic Téléphonie | décembre, 21 606,20 € | Slide 2 |
| Pic Papeterie | août, 12 873,40 € | Slide 2 |
| Pic Mobilier | septembre, 12 160,50 € | Slide 2 |
| Marge top 1 Île-de-France | Smartphone Signal, 4 838,00 € | Slide 3 |
| Marge top 1 Sud | Smartphone Signal, 3 540,00 € | Slide 3 |
| Marge totale annuelle | 276 667,80 € | Slide 3 ou annexe |

Un apprenant qui cite des chiffres arrondis différemment (ex. 655 000 € au lieu de 655 953,60 €) n'a pas forcément fait d'erreur grave, mais la présence des centimes signale qu'il a travaillé depuis ses propres calculs et non depuis sa mémoire ou une IA générative.

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| Titre descriptif sur toutes les slides (« Ventes par catégorie ») | Principe un message par slide non appliqué | Aucun des titres ne contient de chiffre ni de verbe d'action |
| Graphique illisible (12 courbes superposées sans légende) | Trop de séries sur un seul graphique | La slide 2 nécessite 5 séries au maximum ; au-delà, décomposer |
| Chiffres différents des valeurs de contrôle | Données brutes présentées sans nettoyage préalable | CA total hors tolérance : si supérieur à 3 M€, les aberrantes n'ont pas été retirées |
| Classement vendeurs présenté comme performance individuelle | Piège Q3 non détecté dans l'exercice précédent | Vérifier que la copie mentionne la structure vendeur = région |
| Recommandation sans chiffre | Note de synthèse générique | Demander en soutenance : « sur quoi vous appuyez-vous pour proposer cela ? » |
| Slide de synthèse absente | Livrable incomplet | L'énoncé demande explicitement un Key Takeaway |

---

## 5. Volet IA

**Ce qu'on attend dans la copie.**
L'énoncé autorise l'IA pour structurer l'argumentaire et améliorer la clarté des messages. Un usage pertinent consiste à soumettre ses propres chiffres à l'IA en lui demandant de reformuler un titre descriptif en titre porteur de message, puis à vérifier que le titre produit correspond bien aux données. Un usage non pertinent consiste à laisser l'IA générer des chiffres sans les vérifier (l'IA peut fabriquer des valeurs plausibles mais fausses).

**Comment distinguer compréhension et copie-collé.**
Un apprenant qui a compris peut expliquer pourquoi il a choisi ces trois slides dans cet ordre, et pourquoi le titre de la slide 2 cite juin et août plutôt que décembre. Un apprenant qui a recopié citera décembre comme mois de pointe de toutes les catégories.

**Question de vérification orale.**
« Votre slide 2 montre le pic de l'Électroménager en juin. Si la direction vous demande d'expliquer cela en une phrase sans montrer le graphique, que diriez-vous ? Et si elle vous demande pourquoi juin et pas décembre ? »

---

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Structure constat / découverte / recommandation respectée | 3 | Les trois parties sont identifiables dans le plan de slides |
| Titres porteurs de message avec chiffres exacts | 4 | Au moins 2 titres contiennent un chiffre tiré des valeurs de contrôle |
| Slide 2 — saisonnalité différenciée par catégorie | 4 | Les 5 mois de pointe sont identifiés ou au moins 3 sont annotés sur le graphique |
| Slide 3 — recommandation étayée par la marge brute | 3 | Le Smartphone Signal est cité avec sa marge pour au moins une région |
| Identification ou absence du classement vendeurs trompeur | 3 | La copie ne présente pas le CA vendeur comme performance individuelle, ou le nuance avec le panier moyen |
| Lisibilité et sobriété (graphiques lisibles, pas de slide de remplissage) | 2 | Chaque slide contient un seul message principal |
| Slide de synthèse (Key Takeaway) | 1 | Présente, avec au moins un chiffre |
| **Total** | **20** | |

---

## 7. Prolongements

Pour les apprenants rapides, deux pistes pour aller au-delà de la restitution standard.

La présentation comparative avec et sans nettoyage : montrer sur une slide supplémentaire le taux T4/T1 brut (1 748,70 %) face au taux nettoyé (+30,88 %) est une façon percutante de justifier l'étape 1 de l'exercice précédent et de montrer la valeur ajoutée du travail data.

La recommandation régionalisée : le top 3 par marge varie selon la région (la Machine à café Arôme arrive en tête à l'Ouest, le Bureau réglable Altitude au Centre). Une slide par région permettrait des recommandations d'approvisionnement différenciées plutôt qu'une stratégie nationale uniforme.
