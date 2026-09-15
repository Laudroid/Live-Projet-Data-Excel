# Corrigé — Analyser les données avec des fonctions complexes

**Fichier(s) de données :** `Ventes.xlsx` (260 lignes, 4 colonnes) + `Referentiel.xlsx` (onglets `Produits` 33 références, `Magasins` 12 entrées)
**Durée indicative :** 60 min
**Prérequis :** Maîtrise de RECHERCHEV (VLOOKUP), notion de tableau structuré Excel, références inter-feuilles

---

## 1. Ce que l'exercice évalue réellement

L'exercice évalue la capacité à piloter RECHERCHEX (XLOOKUP) sur deux classeurs séparés et à produire des agrégats multi-critères avec SOMME.SI.ENS (SUMIFS) et NB.SI.ENS (COUNTIFS). Le piège central est structurel : 7 lignes de `Ventes.xlsx` portent des identifiants introuvables dans `Referentiel.xlsx` (4 lignes produit orphelines sur les codes P512 et P998, 3 lignes magasin orphelines sur le code MAG21). Un apprenant qui additionne le CA sans avoir détecté les `#N/A` obtient soit une erreur de propagation (SOMME.SI.ENS ignore les `#N/A` dans la plage de condition mais les traite comme zéro dans la plage de somme), soit un total trompeur. L'écart entre les deux totaux de référence — 114 667,60 € hors orphelins et 115 528,70 € si les `#N/A` sont neutralisés à 0 — est le signal de correction attendu.

---

## 2. Corrigé pas à pas

### Étape 1 — Enrichissement produit (Nom_Produit et Prix_Unitaire)

Les deux classeurs doivent être ouverts en même temps pour que la syntaxe inter-classeurs soit lisible dans la barre de formule. Si `Referentiel.xlsx` est fermé, Excel convertit automatiquement la référence en chemin absolu du type `'C:\chemin\[Referentiel.xlsx]Produits'[ID_Produit]` : la formule fonctionne, mais le chemin dur rend le fichier fragile si le classeur source est déplacé. La solution maintenable est soit de rapatrier les onglets `Produits` et `Magasins` dans `Ventes.xlsx`, soit d'utiliser Power Query pour charger les deux sources et les fusionner (option recommandée en environnement de production).

Ajouter deux colonnes au tableau structuré `Ventes` (onglet `Ventes` de `Ventes.xlsx`). Le tableau est nommé `Ventes` et ses colonnes exactes sont `Date`, `ID_Produit`, `Quantité`, `ID_Magasin`.

Colonne `Nom_Produit` — formule en syntaxe française, classeur source ouvert :

```
=RECHERCHEX([@ID_Produit];
            [Referentiel.xlsx]Produits[ID_Produit];
            [Referentiel.xlsx]Produits[Nom_Produit])
```

- `[@ID_Produit]` : clé de recherche issue de la ligne courante du tableau `Ventes`.
- `[Referentiel.xlsx]Produits[ID_Produit]` : tableau de recherche dans l'onglet `Produits` du classeur externe.
- `[Referentiel.xlsx]Produits[Nom_Produit]` : colonne retournée.
- L'argument `si_non_trouve` est omis volontairement à cette étape : les `#N/A` doivent apparaître pour rendre les orphelins visibles.

Colonne `Prix_Unitaire` — même logique sur la troisième colonne du référentiel :

```
=RECHERCHEX([@ID_Produit];
            [Referentiel.xlsx]Produits[ID_Produit];
            [Referentiel.xlsx]Produits[Prix_Unitaire])
```

### Étape 2 — Enrichissement géographique (Région)

Le tableau `Magasins` de `Referentiel.xlsx` contient les colonnes `ID_Magasin`, `Nom_Magasin`, `Ville`, `Région`.

Colonne `Région` dans le tableau `Ventes` :

```
=RECHERCHEX([@ID_Magasin];
            [Referentiel.xlsx]Magasins[ID_Magasin];
            [Referentiel.xlsx]Magasins[Région])
```

Après propagation, 3 cellules affichent `#N/A` (code MAG21 introuvable). Ces lignes sont distinctes des 4 lignes produit orphelines.

### Étape 3 — Calcul du CA

Colonne `CA` dans le tableau `Ventes` :

```
=[@Quantité]*[@Prix_Unitaire]
```

Les 7 lignes orphelines produisent `#N/A` en `Prix_Unitaire` ou en `Région`, ce qui propage `#N/A` dans la colonne `CA`. L'apprenant doit détecter cet état avant de passer à la synthèse.

**Point de contrôle à demander en correction :** afficher un filtre sur la colonne `Nom_Produit` et rechercher `(Vides)` ou `#N/A`. Résultat attendu : 4 lignes produit + 3 lignes magasin = 7 lignes en erreur.

### Étape 4 — Feuille de synthèse : CA par région (SOMME.SI.ENS)

Créer une feuille nommée `Synthèse`. Lister les six régions en colonne A. En colonne B, formule pour la région en A2 :

```
=SOMME.SI.ENS(Ventes[CA];
              Ventes[Région];
              A2)
```

- `Ventes[CA]` : plage des valeurs à additionner (colonne `CA` du tableau `Ventes`).
- `Ventes[Région]` : plage de condition.
- `A2` : critère (nom de la région).

SOMME.SI.ENS (SUMIFS) ignore les cellules en `#N/A` dans la plage de condition (`Ventes[Région]`) — ces lignes ne sont affectées à aucune région et ne contribuent pas aux totaux régionaux. Le total de la colonne B (somme des six régions) donne 114 667,60 € si les formules sont correctes.

Valeurs attendues par région (à vérifier cellule par cellule) :

| Région | CA attendu |
|---|---|
| Île-de-France | 30 118,30 € |
| Ouest | 20 675,30 € |
| Nord | 19 076,90 € |
| Sud | 17 223,60 € |
| Centre | 15 703,80 € |
| Est | 11 869,70 € |

### Étape 5 — Volume de ventes : transactions > 10 unités par région (NB.SI.ENS)

En colonne C de la feuille `Synthèse`, formule pour la région en A2 :

```
=NB.SI.ENS(Ventes[Région];
           A2;
           Ventes[Quantité];
           ">"&10)
```

- Premier couple critère : `Ventes[Région]` = valeur de A2.
- Second couple critère : `Ventes[Quantité]` strictement supérieure à 10.
- L'opérateur de comparaison est concaténé à la valeur numérique avec `&` : `">"&10`.

NB.SI.ENS (COUNTIFS) s'applique sur les lignes où `Région` est renseignée et `Quantité` est un nombre ; les 7 lignes orphelines (dont la région est `#N/A`) sont exclues automatiquement.

Total toutes régions confondues attendu : **103 transactions** sur 253 lignes exploitables.

### Étape 6 — Analyse croisée produit × région

L'énoncé cite « Produit A » dans la région « Nord » comme exemple générique. Le jeu de données réel ne contient pas de produit nommé ainsi. Utiliser un couple réellement présent, par exemple **Écran 27 pouces Lumen** dans la région **Ouest** (3 transactions, CA 3 290,00 €) ou **Fauteuil visiteur Accueil** en **Île-de-France** (3 transactions, CA 2 835,00 €).

Formule pour calculer le CA du produit `Écran 27 pouces Lumen` en région `Ouest` :

```
=SOMME.SI.ENS(Ventes[CA];
              Ventes[Nom_Produit];
              "Écran 27 pouces Lumen";
              Ventes[Région];
              "Ouest")
```

Le résultat attendu est **3 290,00 €**. Le formateur peut proposer n'importe quel des couples du tableau de référence pour varier les questions d'oral.

---

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Lignes totales dans `Ventes.xlsx` | 260 |
| Lignes orphelines (produit ou magasin inconnu) | 7 |
| CA total, lignes orphelines exclues (somme des 6 régions) | 114 667,60 € |
| CA total si les `#N/A` sont neutralisés à 0 | 115 528,70 € |
| Transactions > 10 unités (toutes régions) | 103 |
| CA — Île-de-France | 30 118,30 € |
| CA — Ouest | 20 675,30 € |
| CA — Nord | 19 076,90 € |
| CA — Sud | 17 223,60 € |
| CA — Centre | 15 703,80 € |
| CA — Est | 11 869,70 € |
| CA — Écran 27 pouces Lumen / Ouest | 3 290,00 € |
| CA — Fauteuil visiteur Accueil / Île-de-France | 2 835,00 € |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| CA total = 115 528,70 € au lieu de 114 667,60 € | L'apprenant a neutralisé les `#N/A` par `SIERREUR(...;0)` avant d'agréger, incluant ainsi les orphelins à CA zéro mais en masquant leur existence | Filtrer `Nom_Produit` sur `(Vides)` : la colonne doit afficher `#N/A`, pas 0 |
| SOMME.SI.ENS retourne 0 pour toutes les régions | La colonne `Région` n'a pas été ajoutée au tableau `Ventes` ou pointe vers la mauvaise feuille | Cliquer sur la cellule `Région` d'une ligne : la barre de formule doit montrer le chemin inter-classeurs |
| `#VALEUR!` sur la colonne CA | La colonne `Prix_Unitaire` contient du texte (l'apprenant a saisi les valeurs à la main plutôt que d'utiliser RECHERCHEX) | Insérer `ESTNUM([@Prix_Unitaire])` dans une cellule de test : doit retourner VRAI |
| Résultat SOMME.SI.ENS identique pour toutes les régions | Le critère est une référence absolue figée (`$A$2`) au lieu d'une référence relative ou mixte (`A2`) | Copier la formule sur la ligne suivante et observer si le critère change |
| Erreur de compilation inter-classeurs au rouvrir le fichier | `Referentiel.xlsx` était fermé à l'enregistrement : le chemin absolu ne correspond plus après déplacement | Ouvrir les deux classeurs simultanément puis **Formules > Modifier les liaisons** pour corriger le chemin |
| NB.SI.ENS compte 0 pour chaque région | L'opérateur de comparaison est saisi sans guillemets ou sans concaténation : `>10` au lieu de `">"&10` | Éditer la formule et vérifier la syntaxe du critère numérique |

---

## 5. Prolongements

Pour les apprenants rapides, intégrer les deux classeurs dans un seul modèle de données via **Données > Obtenir des données > Combiner des requêtes > Fusionner** (Power Query) : la jointure gauche sur `ID_Produit` matérialise les orphelins comme des lignes à valeurs nulles et élimine la dépendance au chemin inter-classeurs.

Ajouter une colonne `Mois` dérivée de la colonne `Date` avec `=MOIS([@Date])` puis construire un tableau croisé dynamique CA par mois et par région pour observer la saisonnalité du dernier trimestre (oct.-déc. 2024).

Calculer la part de marché de chaque région sur le CA total avec `=SOMME.SI.ENS(...) / SOMME(Ventes[CA])` et appliquer un format `0,00 %` : c'est l'occasion d'introduire la notion de référence mixte dans une formule de tableau structuré.
