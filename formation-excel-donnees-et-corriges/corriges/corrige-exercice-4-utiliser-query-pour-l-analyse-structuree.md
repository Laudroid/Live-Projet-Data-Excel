# Corrigé — Utiliser QUERY pour l'analyse structurée

**Fichier(s) de données :** `Data_Ventes.csv` (320 lignes, 6 colonnes)
**Durée indicative :** 55 min
**Prérequis :** Connaître les bases des formules matricielles, savoir importer un CSV dans Google Sheets.

---

**Avertissement préalable — outil requis.**
`QUERY` est une fonction Google Sheets. Elle n'existe pas dans Microsoft Excel. Ce TP se réalise exclusivement dans Google Sheets. Toute tentative de reproduire les formules dans Excel aboutira à une erreur `#NOM?`. Le corrigé ci-dessous suppose un classeur Sheets.

**Séparateur d'arguments.** Dans un classeur en locale française (paramètre régional France), le séparateur d'arguments de toutes les fonctions Sheets est le point-virgule. La syntaxe complète de `QUERY` est :

```
=QUERY(données ; requête ; [en-têtes])
```

Dans un classeur en locale anglophone, le séparateur est la virgule :

```
=QUERY(data, query, [headers])
```

Toutes les formules de ce corrigé utilisent le point-virgule. Si l'apprenant travaille dans un classeur anglophone, il remplace chaque point-virgule par une virgule.

---

## 1. Ce que l'exercice évalue réellement

L'exercice évalue la capacité à écrire des requêtes pseudo-SQL dans Sheets, à maîtriser les imbrications de guillemets dans une chaîne de requête et à gérer la dynamisation d'une formule par référence de cellule. Le piège central est la gestion des apostrophes : la chaîne de requête est délimitée par des guillemets doubles, et les valeurs littérales de la clause WHERE exigent des apostrophes simples à l'intérieur — une confusion entre ces deux types de délimiteurs produit une erreur `#VALUE!` difficile à diagnostiquer sans méthode.

## 2. Corrigé pas à pas

### Étape préalable — Import et vérification

Importer `Data_Ventes.csv` dans Google Sheets via **Fichier > Importer > Télécharger**, format CSV, séparateur virgule, encodage UTF-8 (le fichier est écrit en UTF-8 avec BOM, Sheets le détecte automatiquement). Nommer l'onglet `Data_Ventes`.

Vérification obligatoire avant d'écrire les requêtes : la colonne Montant (colonne E) doit être de type numérique entier. Si l'import est réalisé dans un classeur en locale française sur un CSV contenant des décimales avec un point (ex : `549.90`), Sheets interprète la valeur comme du texte et toute agrégation `SUM(E)` renvoie silencieusement 0. Ce risque est écarté ici : les montants de `Data_Ventes.csv` sont des entiers sans décimale, précisément pour éviter ce piège. Vérifier visuellement que la colonne E est alignée à droite (comportement par défaut des nombres dans Sheets) ; si elle est alignée à gauche, elle est en texte.

Ordre des colonnes imposé par l'énoncé :

| Colonne | Nom | Lettre dans QUERY |
|---|---|---|
| A | Date | A |
| B | Catégorie | B |
| C | Produit | C |
| D | Vendeur | D |
| E | Montant | E |
| F | Région | F |

### Étape 1 — Exercice 1 : filtrage multi-critères

Conditions : Catégorie = « Électronique » ET Montant > 500 ET Région = « Nord » OU Région = « Sud ».

Dans un nouvel onglet, en cellule A1 :

```
=QUERY(Data_Ventes!A:F ; "SELECT A, B, C, D, E, F WHERE B = 'Électronique' AND E > 500 AND (F = 'Nord' OR F = 'Sud')" ; 1)
```

Décomposition de la requête :

- `Data_Ventes!A:F` : plage source, onglet `Data_Ventes`, colonnes A à F.
- `SELECT A, B, C, D, E, F` : toutes les colonnes affichées.
- `WHERE B = 'Électronique'` : filtre sur la catégorie.
- `AND E > 500` : filtre sur le montant (valeur numérique, pas d'apostrophe).
- `AND (F = 'Nord' OR F = 'Sud')` : filtre sur la région, parenthèses obligatoires pour la priorité des opérateurs.
- `; 1` : le troisième argument indique que la première ligne de la plage source contient les en-têtes.

Piège des guillemets — règle à retenir : la chaîne de requête est entre guillemets doubles `"..."`. À l'intérieur, toute valeur littérale de type texte prend des apostrophes simples `'...'`. Écrire `B = "Électronique"` (guillemets doubles à l'intérieur) produit une erreur de syntaxe dans le moteur de requête.

Piège des accents : la valeur `Électronique` doit être écrite avec un É majuscule accentué, exactement comme dans les données sources. Une comparaison de chaînes dans QUERY est sensible à la casse.

### Étape 2 — Exercice 2 : agrégation, tri et HAVING

Dans un nouvel onglet, en cellule A1 :
Pour filtrer des résultats basés sur une agrégation (comme `SUM(E) > 1000`), la méthode recommandée est d'imbriquer deux fonctions `QUERY`.

``` 
=QUERY(QUERY(Data_Ventes!A:F, "SELECT D, SUM(E) WHERE D IS NOT NULL GROUP BY D", 1), "SELECT * WHERE Col2 > 1000 ORDER BY Col2 DESC", 1)

```

**Comment fonctionne cette formule :**

1.  **La requête interne** : `QUERY(Data_Ventes!A:F, "SELECT D, SUM(E) WHERE D IS NOT NULL GROUP BY D", 1)`
    Elle extrait les données de votre feuille `Data_Ventes`, regroupe les ventes par vendeur (colonne D) et calcule la somme totale des montants (colonne E) pour chacun d'entre eux.
2.  **La requête externe** : `QUERY(..., "SELECT * WHERE Col2 > 1000 ORDER BY Col2 DESC", 1)`
    Elle prend le tableau généré par la première requête et le filtre. Puisque la somme des montants devient la deuxième colonne du nouveau tableau virtuel, on utilise `Col2` pour indiquer que l'on ne veut garder que les lignes où cette somme est supérieure à 1000. Enfin, elle trie ces résultats par ordre décroissant (`ORDER BY Col2 DESC`).

*(Note : La formule ci-dessus utilise des virgules comme séparateurs d'arguments selon la convention standard. Si les paramètres régionaux de votre document exigent des points-virgules, il vous suffira de remplacer les virgules séparant les arguments par des points-virgules, comme dans votre formule initiale).*

### Étape 3 — Exercice 3 : requête paramétrée

Créer dans l'onglet de travail deux cellules de saisie :

- `H1` : catégorie (ex : `Électronique`)
- `H2` : région (ex : `Nord`)

Formule en cellule A4 (ou tout emplacement non adjacent aux cellules de saisie) :

```
=QUERY(Data_Ventes!A:F ; "SELECT A, B, C, D, E, F WHERE B = '"&H1&"' AND F = '"&H2&"'" ; 1)
```

Décomposition de la concaténation :

La chaîne de requête est découpée en trois fragments joints par `&` :

1. `"SELECT A, B, C, D, E, F WHERE B = '"` : début de la chaîne, se termine par une apostrophe ouvrante.
2. `&H1&` : contenu de la cellule H1, inséré sans guillemets.
3. `"' AND F = '"` : ferme l'apostrophe de H1, ajoute le connecteur AND, ouvre l'apostrophe pour H2.
4. `&H2&` : contenu de la cellule H2.
5. `"'"` : ferme l'apostrophe de H2.

Piège 1 — apostrophes mal refermées : une erreur fréquente est d'écrire `"...WHERE B = '"&H1&"' AND..."` sans la dernière `"'"` fermante, produisant une requête syntaxiquement incorrecte et l'erreur `#VALUE!`. La méthode de vérification est de lire la chaîne reconstituée dans la barre de formule ou dans une cellule auxiliaire : `="SELECT A, B, C, D, E, F WHERE B = '"&H1&"' AND F = '"&H2&"'"`.

Piège 2 — cellule de saisie vide : si H1 ou H2 est vide, la clause WHERE contient `B = ''`, qui ne correspond à aucune ligne et renvoie un résultat vide sans message d'erreur. Ce comportement est silencieux et peut tromper l'apprenant qui croit que la requête est cassée.

Traitement recommandé avec SI (IF) :

```
=SI(H1="";"Saisir une catégorie en H1";QUERY(Data_Ventes!A:F;"SELECT A, B, C, D, E, F WHERE B = '"&H1&"' AND F = '"&H2&"'";1))
```

Ou, pour retourner toutes les lignes quand H1 est vide (comportement « toutes valeurs ») :

```
=QUERY(Data_Ventes!A:F;SI(H1="";"SELECT A, B, C, D, E, F";"SELECT A, B, C, D, E, F WHERE B = '"&H1&"' AND F = '"&H2&"'");1)
```

Cette seconde approche est plus robuste pédagogiquement : elle montre que la chaîne de requête elle-même peut être construite par une formule.

Jeu de test (nombre de lignes attendu pour chaque combinaison catégorie x région) :

| Catégorie | Centre | Est | Nord | Ouest | Sud | Île-de-France |
|---|---|---|---|---|---|---|
| Mobilier | 9 | 5 | 6 | 6 | 4 | 11 |
| Papeterie | 12 | 11 | 18 | 14 | 23 | 16 |
| Téléphonie | 6 | 5 | 7 | 9 | 12 | 22 |
| Électroménager | 8 | 6 | 12 | 16 | 8 | 13 |
| Électronique | 7 | 7 | 15 | 6 | 9 | 17 |

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Lignes sources (hors en-tête) | 320 |
| CA total | 147 934,00 € |
| Exercice 1 — lignes renvoyées | 13 |
| Exercice 1 — somme des montants | 8 951,00 € |
| Exercice 1 — montant minimum | 549 |
| Exercice 1 — montant maximum | 987 |
| Exercice 1 — dont région Nord | 9 lignes |
| Exercice 1 — dont région Sud | 4 lignes |
| Exercice 2 — lignes renvoyées | 11 |
| Exercice 2 — vendeur exclu | Sofia Renard (525,00 €) |
| Exercice 2 — vendeur en limite basse | Bastien Roux (1 167,00 €) |
| Exercice 2 — premier vendeur | Camille Fournier (28 119,00 €) |

Tableau de référence complet pour l'exercice 2 :

| Vendeur | Total montants | Retenu (> 1 000 €) |
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

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| Erreur `#VALUE!` sur toute la formule | Apostrophes ou guillemets mal appariés dans la chaîne de requête | Isoler la chaîne dans une cellule auxiliaire avec `=` et la lire ; repérer l'apostrophe manquante |
| Résultat vide alors que le filtre devrait retourner des lignes | Valeur littérale écrite avec guillemets doubles à l'intérieur (`B = "Électronique"` au lieu de `B = 'Électronique'`) | Vérifier la chaîne avec l'astuce de la cellule auxiliaire |
| `SUM(E)` renvoie 0 | Colonne Montant importée en texte (possible en locale française avec des décimales pointées) | Cliquer sur une cellule E ; si la formule barre affiche `'549` (guillemet précédant le nombre), c'est du texte |
| Exercice 1 : la catégorie Électronique ne ressort pas | Accent absent ou différent dans la valeur littérale (`Electronique` sans accent) | Copier-coller la valeur directement depuis une cellule de données |
| Exercice 2 : 12 lignes au lieu de 11 | Clause HAVING absente ou écrite `HAVING E > 1000` au lieu de `HAVING SUM(E) > 1000` | Lire la formule ; HAVING porte sur l'agrégat, pas sur la valeur individuelle |
| Exercice 3 : cellule H1 vide renvoie vide sans explication | Comportement normal non documenté par l'apprenant | Vérifier si un commentaire ou un SI explicite le cas vide |
| En-têtes générés : `sum E` au lieu de `Total montants` | LABEL absent de la requête | Lire la formule : vérifier la présence de `LABEL SUM(E) 'Total montants'` |

## 5. Volet IA

L'énoncé autorise l'IA pour déboguer des erreurs de syntaxe, à condition que l'apprenant n'ait pas recopié la réponse sans comprendre. Ce qui est attendu dans la copie :

- Un commentaire sur chaque cellule de résultat (consigne de l'énoncé) expliquant la logique de la clause SELECT. Un apprenant qui a compris écrit un commentaire qui reformule avec ses mots ; un apprenant qui a recopié laisse un commentaire générique ou absent.
- Si l'apprenant cite l'IA dans sa démarche, il doit expliquer pourquoi la clause HAVING est nécessaire plutôt que d'utiliser un WHERE avec une condition sur la somme (ce qui est syntaxiquement impossible dans QUERY).

Question de vérification orale :

« Votre exercice 3 filtre sur une catégorie et une région. Si je vide la cellule H1 tout en gardant une valeur en H2, combien de lignes votre formule renvoie-t-elle, et pourquoi ? Comment modifieriez-vous la formule pour retourner toutes les lignes de la région H2 quand H1 est vide ? »

Cette question distingue l'apprenant qui a réfléchi au comportement des cellules vides de celui qui n'a testé qu'un cas de fonctionnement nominal.

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Import correct : onglet nommé Data_Ventes, 320 lignes, colonne Montant numérique | 2 | Compter les lignes, cliquer sur une cellule E |
| Exercice 1 : formule fonctionnelle, 13 lignes renvoyées | 3 | Compter les lignes du résultat |
| Exercice 1 : somme des montants conforme (8 951 €) | 1 | Cellule SUM sous le résultat ou formule vérification |
| Exercice 2 : 11 lignes renvoyées, Sofia Renard absente | 3 | Compter les lignes ; vérifier l'absence de Sofia Renard |
| Exercice 2 : LABEL présent et en-têtes lisibles | 1 | Lire les en-têtes de la plage de résultat |
| Exercice 3 : formule paramétrée fonctionnelle (deux cellules de saisie) | 3 | Changer H1 et H2, vérifier que le résultat change conformément au tableau de test |
| Exercice 3 : cas cellule vide traité (SI ou commentaire explicatif) | 2 | Vider H1 ; observer et lire le commentaire |
| Commentaires sur chaque cellule de résultat | 2 | Survoler chaque cellule de résultat |
| Syntaxe française cohérente (point-virgule) | 1 | Lire les formules |
| Total | 18 | |

## 7. Prolongements

Ajouter une clause `FORMAT E '# ##0 "€"'` dans la requête de l'exercice 2 pour afficher les montants avec le symbole euro directement dans le résultat QUERY, sans mise en forme manuelle de la colonne.

Réécrire l'exercice 1 avec une clause `PIVOT` pour obtenir un tableau croisé catégorie x région directement dans Sheets : `SELECT B, F, SUM(E) GROUP BY B PIVOT F` permet de comparer les montants par région sans TCD.

Tester l'effet du paramètre `en-têtes` (troisième argument de QUERY) : passer de 1 à 0 ou à -1 pour comprendre comment Sheets gère les cas où la première ligne de la plage source ne contient pas d'en-têtes.
