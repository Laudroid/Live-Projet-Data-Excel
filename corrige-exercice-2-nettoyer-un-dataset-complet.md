# Corrigé — Nettoyage et fiabilisation d'un jeu de données client

**Fichier(s) de données :** `clients_brut.xlsx` (195 lignes, 9 colonnes) — tableau structuré nommé `Clients`

---

## 1. Ce que l'exercice évalue réellement

L'exercice mesure la capacité à conduire un nettoyage dans le bon ordre : standardiser la casse et les espaces avant de chercher les doublons, et non l'inverse. Le jeu de données contient 15 doublons, dont seuls 8 sont détectables sur les colonnes brutes ; les 7 autres sont masqués par des variations de casse et d'espaces, et n'apparaissent qu'après application de `NOMPROPRE(SUPPRESPACE(...))`. Le piège de la colonne Adresse (extraction de la ville par `DROITE` avec un nombre fixe de caractères) révèle en outre si l'apprenant sait reconnaître la limite d'une approche naïve face aux villes composées.

---

## 2. Corrigé pas à pas

### Étape 1 — Standardisation des données textuelles

#### 1a. Nettoyage des noms

Insérer une colonne auxiliaire à droite de `Nom`. Dans la première cellule de données (par exemple `J2` si le tableau commence en `A1`) :

```
=NOMPROPRE(SUPPRESPACE([@Nom]))
```

- `SUPPRESPACE` (TRIM) supprime les espaces en début, en fin, et réduit les espaces internes multiples à un seul.
- `NOMPROPRE` (PROPER) met en majuscule la première lettre de chaque mot et passe le reste en minuscules.

L'ordre est imposé : `NOMPROPRE` seul ne supprime pas les espaces parasites, et `SUPPRESPACE` seul ne corrige pas la casse. Passer `NOMPROPRE` en premier puis `SUPPRESPACE` est incorrect : `NOMPROPRE("  dupont  jean ")` renvoie `"  Dupont  Jean "` (espaces conservés), que `SUPPRESPACE` réduirait ensuite à `"Dupont Jean"`. L'ordre `NOMPROPRE(SUPPRESPACE(...))` ou l'ordre inverse donnent le même résultat final ici, mais l'imbrication `NOMPROPRE(SUPPRESPACE(...))` est la convention attendue et la plus lisible.

**Variante Power Query :** Onglet **Transformer > Mettre en forme > Rogner**, puis **Capitaliser chaque mot**. Plus robuste car appliqué avant chargement, sans colonne auxiliaire.

#### 1b. Extraction du code postal et de la ville

La colonne `Adresse` contient des valeurs du type `"59000 Lille"`, `"13100 Aix-en-Provence"` ou `"92100 Boulogne-Billancourt"`.

**Approche naïve qui échoue :**

```
=DROITE([@Adresse];5)    ' → "ille " pour Lille, "ence" pour Aix-en-Provence
```

`DROITE` avec un nombre fixe de caractères échoue parce que les noms de villes ont des longueurs variables. Sur les 195 lignes, 23 adresses comportent une ville composée (avec tiret) ; `DROITE([@Adresse];15)` tronquerait Lille, et `DROITE([@Adresse];5)` tronquerait Aix-en-Provence.

**Solution correcte — extraction du code postal (5 caractères fixes) :**

```
=GAUCHE([@Adresse];5)
```

Le code postal français est toujours 5 chiffres ; `GAUCHE` avec 5 est ici sans ambiguïté.

**Solution correcte — extraction de la ville :**

```
=TEXTEAPRES([@Adresse];" ")
```

`TEXTEAPRES` (TEXTAFTER, Excel 365) extrait tout ce qui suit le premier espace, quelle que soit la longueur de la ville.

**Alternative compatible Excel 2016/2019 :**

```
=STXT([@Adresse];7;100)
```

Le code postal occupe toujours les positions 1 à 5, suivi d'un espace en position 6 ; la ville commence donc en position 7. La longueur 100 garantit que les villes longues ne sont pas tronquées.

**Alternative générique (insensible à la longueur du code) :**

```
=STXT([@Adresse];CHERCHE(" ";[@Adresse])+1;NBCAR([@Adresse]))
```

`CHERCHE` (SEARCH) localise le premier espace, +1 donne la position du premier caractère de la ville.

---

### Étape 2 — Gestion des doublons

#### Contexte chiffré à connaître pour la correction

Sur les 195 lignes, 180 clients sont réellement distincts et 15 sont en doublon. Parmi ces 15 :

- **8 sont détectables directement** sur les colonnes brutes (même `Nom` et même `Email` en l'état) : un **Données > Supprimer les doublons** sur les colonnes `Nom` et `Email` les trouve.
- **7 sont masqués par la casse ou les espaces** : la même personne apparaît sous `"  garnier  amandine  "` et `"Garnier Amandine"`. Ces doublons ne deviennent visibles que lorsque la colonne auxiliaire normalisée (étape 1a) est utilisée comme critère.

C'est ce qui justifie l'ordre des étapes de l'énoncé : si l'apprenant supprime les doublons avant de standardiser, il manque 7 occurrences et son fichier contient 187 lignes au lieu de 180.

#### 2a. Marquage des doublons (colonne Statut)

Ajouter une colonne `Statut` avec une formule `NB.SI` (COUNTIF) sur la colonne normalisée. En supposant que la colonne normalisée est `Nom_Nettoye` et que `Email` est en colonne `C` :

```
=SI(NB.SI.ENS(Clients[Nom_Nettoye];[@Nom_Nettoye];Clients[Email];[@Email])>1;
    "Doublon";"Unique")
```

`NB.SI.ENS` (COUNTIFS) compte les lignes ayant la même valeur normalisée de nom ET le même email. Une valeur supérieure à 1 signale un doublon.

#### 2b. Suppression des doublons

Après avoir vérifié le marquage : **Données > Outils de données > Supprimer les doublons**, en sélectionnant les colonnes `Nom_Nettoye` et `Email`. Le résultat attendu est 180 lignes.

#### 2c. Réflexion : pourquoi marquer avant de supprimer ?

Trois raisons fondamentales :

1. **Traçabilité** : la colonne `Statut` constitue un journal d'audit. Le formateur, le responsable CRM ou un auditeur peut vérifier quelles lignes ont été identifiées comme doublons et pourquoi, sans avoir à reconstituer le raisonnement a posteriori.

2. **Réversibilité** : la suppression est irréversible une fois enregistrée (hors annulation). Un marquage préalable permet, en cas d'erreur de critère, de filtrer sur `"Doublon"` pour inspecter les lignes concernées avant de valider la suppression.

3. **Arbitrage sur la ligne à conserver** : quand deux doublons ne sont pas strictement identiques (segment client différent, CA différent, date de création différente), il faut décider laquelle des deux lignes est la référence. Le marquage permet de les examiner côte à côte avant de choisir.

---

### Étape 3 — Traitement des valeurs manquantes dans la colonne Téléphone

#### État des données

| Cas | Nombre de cellules | Nature |
|---|---|---|
| Cellule vide | 16 | Absence de valeur — test `=""` |
| Chaîne `"non renseigné"` | 9 | Valeur texte présente — test `=EXACT([@Telephone];"non renseigné")` |
| Valeur numérique (zéro initial perdu) | 15 | Nombre entier — zéro affiché manquant |
| Formats textuels variés | reste | 5 formats coexistent : brut 10 chiffres, groupé par espaces, groupé par points, `+33`, manquant |

**Distinction cruciale :** une cellule vide et la chaîne `"non renseigné"` ne se testent pas de la même façon. `SI([@Telephone]=""` répond `VRAI` pour la cellule vide mais `FAUX` pour la chaîne. `SI([@Telephone]="non renseigné"` répond `FAUX` pour la cellule vide. Il faut les traiter séparément si l'on souhaite un résultat uniforme.

#### 3a. Identification visuelle par mise en forme conditionnelle

Sélectionner la colonne `Telephone` > **Accueil > Mise en forme conditionnelle > Nouvelle règle > Mettre en forme uniquement les cellules qui contiennent > Valeur de cellule égale à** (laisser vide). Choisir un fond coloré.

#### 3b. Remplacement des cellules vides

Dans une colonne auxiliaire, ou en utilisant **Rechercher et remplacer** sur les vides :

```
=SI([@Telephone]="";"Non renseigné";[@Telephone])
```

Pour traiter simultanément vides et chaîne existante :

```
=SI(OU([@Telephone]="";"non renseigné"=MINUSCULE([@Telephone]));"Non renseigné";[@Telephone])
```

`SI.NON.DISP` (IFNA) n'est pas adapté ici car il intercepte les erreurs `#N/A`, pas les chaînes vides.

#### 3c. Affichage des numéros à zéro initial perdu

Pour les 15 cellules contenant un entier (ex. : `623456789` à la place de `0623456789`), le format personnalisé suivant restitue l'affichage sans modifier la valeur :

**Format de cellule personnalisé :** `0# ## ## ## ##`

Ce format force un `0` en première position, puis affiche les 9 chiffres restants en groupes de deux séparés par des espaces. Il ne modifie que l'affichage — la valeur stockée reste un entier.

**Si l'on veut convertir en texte** (pour uniformiser avec les autres cellules) :

```
=TEXTE([@Telephone];"0# ## ## ## ##")
```

`TEXTE` (TEXT) convertit le nombre en chaîne de caractères au format spécifié.

---

## 3. Valeurs de contrôle

| Contrôle | Valeur attendue |
|---|---|
| Lignes initiales | 195 |
| Colonnes | 9 |
| Clients réellement distincts | 180 |
| Doublons à supprimer | 15 |
| dont détectables sans nettoyage préalable | 8 |
| dont masqués par la casse ou les espaces | 7 |
| Noms à nettoyer (espaces parasites) | 124 |
| Noms en capitales intégrales | 36 |
| Téléphones vides | 16 |
| Téléphones à « non renseigné » | 9 |
| Téléphones numériques (zéro initial perdu) | 15 |
| Adresses à ville composée (tiret) | 23 |
| Codes postaux distincts | 25 |
| Lignes après déduplication | 180 |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| 187 lignes après déduplication au lieu de 180 | L'apprenant a supprimé les doublons sur la colonne `Nom` brute, sans normaliser la casse et les espaces au préalable | Filtrer la copie sur le couple `Garnier Amandine` / `amandine.garnier@mail-test.fr` — les deux doivent avoir disparu |
| La ville affichée commence par un espace | `STXT([@Adresse];6;100)` au lieu de 7, ou `TEXTEAPRES` avec position incorrecte | Sélectionner une cellule ville et appuyer sur F2 pour voir le curseur en début de chaîne |
| Les villes composées sont tronquées | Utilisation de `DROITE([@Adresse];N)` avec N fixe | Chercher une ligne Aix-en-Provence dans la colonne ville obtenue |
| Les 9 cellules « non renseigné » ne sont pas traitées | Test `[@Telephone]=""` ne détecte pas une chaîne non vide | Filtrer la colonne résultat sur « non renseigné » minuscule — doit être vide si le traitement est complet |
| Les numéros numériques s'affichent sans le zéro initial | Format standard ou texte appliqué à une cellule numérique | Vérifier qu'un format personnalisé `0# ## ## ## ##` est appliqué aux cellules de type Nombre |
| Formule `NB.SI` comptant 0 ou 1 pour tous les doublons | Critère appliqué sur la colonne `Nom` brute et non sur la colonne normalisée | Rechercher le couple CLI0087 / CLI0171 (BLANCHARD CAMILLE) — le statut doit être « Doublon » |
| `NOMPROPRE` appliqué avant `SUPPRESPACE` avec résultat correct | Les deux ordres d'imbrication donnent le même résultat final dans ce cas | Acceptable au barème ; noter que l'ordre standard est `NOMPROPRE(SUPPRESPACE(...))` |

---

## 5. Volet IA

**Ce qu'on attend dans le livrable :** l'apprenant qui a utilisé l'IA doit avoir copié le prompt et expliqué, dans ses propres mots, pourquoi `GAUCHE([@Adresse];5)` fonctionne pour le code postal et pourquoi `DROITE` avec un nombre fixe échoue sur les villes composées. Une explication qui se contente de recopier la réponse de l'IA sans reformuler trahit l'absence de compréhension.

**Ce qui distingue un apprenant qui a compris :** il peut citer un exemple de ville composée présente dans le fichier (Aix-en-Provence, Boulogne-Billancourt, Le Havre, Saint-Étienne) et montrer concrètement combien de caractères `DROITE` aurait dû extraire pour chacune — et pourquoi ce nombre diffère.

**Question de vérification orale (soutenance) :** « Dans votre formule `TEXTEAPRES([@Adresse];" ")`, que se passe-t-il si une adresse contient deux espaces — par exemple si un code postal était saisi avec une espace en fin ? Montrez-moi comment vous testeriez ce cas et quelle formule alternative serait plus robuste. »

---

## 7. Prolongements

Pour les apprenants rapides, trois pistes d'approfondissement :

1. **Power Query complet :** reproduire l'intégralité du nettoyage (normalisation, extraction, déduplication) dans Power Query, de façon à rendre le processus rejouable à chaque import de fichier CRM.

2. **Déduplication avec conservation de la ligne la plus récente :** écrire une formule `NB.SI.ENS` qui identifie, parmi deux doublons, celui dont `Date_Creation` est la plus ancienne, pour supprimer le plus ancien et conserver l'entrée la plus récente.

3. **Validation des adresses e-mail par formule :** construire une colonne de contrôle qui vérifie la présence d'un `@` et d'un point après le `@` dans la colonne `Email`, à l'aide de `CHERCHE` et `SIERREUR` (IFERROR).
