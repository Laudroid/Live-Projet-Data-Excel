# 4-2-1 Requêtes structurées : utilisation de la fonction `QUERY`

La fonction `QUERY` (spécifique à Google Sheets) permet d'interroger des plages de données en utilisant une syntaxe proche du langage SQL (Structured Query Language). Elle offre une puissance de traitement bien supérieure aux fonctions de recherche et de filtrage classiques, permettant de **filtrer, trier, agréger, calculer et restructurer** des données au sein d'une seule formule dynamique.

---

## 1. Contexte & Jeu de données pédagogique

Pour illustrer l'ensemble des exemples de ce cours, nous utiliserons la plage de données suivante nommée `Ventes_Data` (plage **`A1:E11`**) :

|  | A (Date) | B (Commercial) | C (Région) | D (Catégorie) | E (Chiffre_Affaires) |
| --- | --- | --- | --- | --- | --- |
| **1** | **Date** | **Commercial** | **Région** | **Catégorie** | **Chiffre_Affaires** |
| **2** | 05/09/2026 | Sophie | Nord | Logiciels | 1 200 |
| **3** | 06/09/2026 | Marc | Sud | Matériel | 450 |
| **4** | 07/09/2026 | Sophie | Est | Services | 850 |
| **5** | 08/09/2026 | Antoine | Nord | Logiciels | 2 100 |
| **6** | 08/09/2026 | Marc | Nord | Services | 300 |
| **7** | 09/09/2026 | Sophie | Sud | Logiciels | 1 500 |
| **8** | 10/09/2026 | Claire | Est | Matériel | 3 200 |
| **9** | 11/09/2026 | Antoine | Sud | Services | 600 |
| **10** | 12/09/2026 | Claire | Nord | Logiciels | 1 800 |
| **11** | 12/09/2026 | Marc | Est | Matériel | 950 |

---

## 2. Concepts fondamentaux

La fonction `QUERY` s'articule autour de trois arguments :

```excel
=QUERY(données; requête; [en-têtes])

```

* **données** (`A1:E11`) : La plage source contenant les données brutes.
* **requête** (`"SELECT ... "`) : La chaîne de texte contenant les instructions écrites en langage de requête Google Visualization API.
* **en-têtes** (`1`) : Le nombre de lignes d'en-tête en haut de votre plage (optionnel mais recommandé, généralement `1`).

---

## 3. Décomposition des clauses principales

Le tableau ci-dessous résume l'ordre strict d'écriture des clauses dans une requête :

| Clause | Rôle pédagogique | Exemple de syntaxe |
| --- | --- | --- |
| **`SELECT`** | Choisir et ordonner les colonnes à afficher | `SELECT B, E` |
| **`WHERE`** | Filtrer les lignes selon un ou plusieurs critères | `WHERE C = 'Nord' AND E > 1000` |
| **`GROUP BY`** | Regrouper les données pour réaliser des agrégations | `GROUP BY C` *(nécessite `SUM`, `AVG`, `COUNT`, etc.)* |
| **`PIVOT`** | Pivoter une dimension en colonnes (Style Tableau Croisé Dynamique) | `PIVOT D` |
| **`ORDER BY`** | Trier les résultats (croissant/décroissant) | `ORDER BY E DESC` |
| **`LIMIT`** | Restreindre le nombre de lignes retournées | `LIMIT 5` |
| **`LABEL`** | Renommer les en-têtes de colonnes calculées | `LABEL SUM(E) 'Total CA'` |

---

## 4. Progression pédagogique : Du cas simple au cas avancé

### Cas 1 : Extraction & Sélection simple (`SELECT` + `WHERE`)

**Objectif :** Extraire uniquement le nom du commercial, la catégorie et le montant des ventes réalisées dans la région **"Nord"**.

```excel
=QUERY(A1:E11; "SELECT B, D, E WHERE C = 'Nord'"; 1)

```

* **Analyse de la formule :**
* `SELECT B, D, E` évite d'afficher les colonnes A et C devenues redondantes.
* Les chaînes de caractères dans le filtre `WHERE` doivent être entourées de **guillemets simples** (`'Nord'`).



---

### Cas 2 : Filtrage multi-critères et tri (`AND` + `ORDER BY`)

**Objectif :** Afficher toutes les ventes de **"Logiciels"** dont le montant dépasse **1 000 €**, triées de la vente la plus élevée à la plus basse.

```excel
=QUERY(A1:E11; "SELECT A, B, E WHERE D = 'Logiciels' AND E > 1000 ORDER BY E DESC"; 1)

```

* **Analyse de la formule :**
* L'opérateur logique `AND` impose le respect simultané des deux conditions.
* `ORDER BY E DESC` trie la colonne E par ordre décroissant (`ASC` pour croissant).



---

### Cas 3 : Agrégation et statistiques (`GROUP BY` + `LABEL`)

**Objectif :** Calculer le chiffre d'affaires total et la vente moyenne par commercial, puis renommer proprement les en-têtes.

```excel
=QUERY(A1:E11; "SELECT B, SUM(E), AVG(E) GROUP BY B LABEL SUM(E) 'Total CA', AVG(E) 'Panier Moyen'"; 1)

```

* **Analyse de la formule :**
* Toute colonne présente dans le `SELECT` qui n'est pas une fonction d'agrégation (`SUM`, `AVG`, `COUNT`, `MIN`, `MAX`) **doit obligatoirement** figurer dans la clause `GROUP BY`.
* La clause `LABEL` permet de remplacer les titres par défaut (`sum Chiffre_Affaires`) par des libellés professionnels.



---

### Cas 4 : Création d'une vue matricielle (`PIVOT`)

**Objectif :** Obtenir un tableau croisé synthétique affichant le total du chiffre d'affaires par **Commercial** (en lignes) et par **Région** (en colonnes).

```excel
=QUERY(A1:E11; "SELECT B, SUM(E) GROUP BY B PIVOT C"; 1)

```

* **Résultat généré :**
Un tableau à double entrée dynamique se génère automatiquement avec les commerciaux en premier champ de ligne et les régions ventilées en colonnes.

---

### Cas 5 : Dynamicité avec référence à une cellule

**Objectif :** Filtrer le tableau en fonction d'une valeur saisie par l'utilisateur dans la cellule **`G1`** (ex: un menu déroulant pour choisir la Région).

```excel
=QUERY(A1:E11; "SELECT B, D, E WHERE C = '" & G1 & "'"; 1)

```

* **Astuce pédagogique pour comprendre la concaténation :**
Pour injecter la cellule `G1` dans la chaîne de texte SQL, on la découpe : `"SELECT ... WHERE C = '"` `& G1 &` `"'"` :
1. Guillemet double pour fermer le premier morceau du texte.
2. Esperluette (`&`) pour lier la valeur de la cellule `G1`.
3. Re-ouvertures de texte entourant le guillemet simple de fin requise par SQL.



---

## 5. Schéma de flux de traitement

```mermaid
graph TD
    A[Plage Source : Données Brutes A1:E11] --> B[Moteur QUERY]
    B --> C{Application des clauses dans l'ordre}
    C -->|1. WHERE| D[Filtrage des lignes]
    C -->|2. GROUP BY / PIVOT| E[Agrégation / Restructuration]
    C -->|3. SELECT| F[Sélection des colonnes]
    C -->|4. ORDER BY / LIMIT| G[Tri et restriction]
    C -->|5. LABEL| H[Mise en forme des en-têtes]
    D --> E --> F --> G --> H --> I[Tableau Résultat Projeté]

```

---

## 6. Passerelle Pédagogique : Google Sheets `QUERY` vs Microsoft Excel

Bien que `QUERY` soit exclusive à Google Sheets, il est essentiel de faire le pont avec les fonctionnalités équivalentes sous Microsoft Excel :

| Besoin Pédagogique | Solution Google Sheets (`QUERY`) | Equivalent Microsoft Excel |
| --- | --- | --- |
| **Requête SQL directe dans la feuille** | `=QUERY(...)` | **Power Query** (Onglet *Données > Obtenir des données*) ou requêtes M/SQL. |
| **Filtrage dynamique contextuel** | `=QUERY(A1:E11; "WHERE C='Nord'")` | Fonction **`FILTRE`** (Excel 365) : `=FILTRE(A2:E11; C2:C11="Nord")` |
| **Agrégation dynamique** | `=QUERY(A1:E11; "SELECT B, SUM(E) GROUP BY B")` | **Tableau Croisé Dynamique (TCD)** ou fonctions **`GROUPBY`** / **`PIVOTBY`** (Excel 365 moderne). |

---

## 7. Diagnostic et résolution des erreurs fréquentes

| Erreur affichée | Cause sous-jacente | Action corrective |
| --- | --- | --- |
| **`#VALUE!`** *(Erreur de syntaxe)* | Oubli de guillemets simples autour d'un texte dans le `WHERE` ou faute de frappe dans un nom de clause. | Vérifier la présence des `'` (ex: `WHERE C = 'Nord'`) et l'orthographe des mots-clés SQL. |
| **Données manquantes / masquées** | **Incohérence du type de données.** Si une colonne contient 80% de nombres et 20% de texte, `QUERY` convertit la colonne entière et ignore le type minoritaire. | Nettoyer la colonne source pour s'assurer que chaque cellule ait le même format (100% Nombre ou 100% Texte). |
| **`#REF!`** | Le résultat de la requête essaye d'écraser des cellules préexistantes sous la formule (conflit de débordement). | Libérer l'espace situé en dessous et à droite de la cellule contenant la formule `QUERY`. |

---

## 8. Exercice pratique d'application (Auto-évaluation)

**Consigne :**
À partir du jeu de données fourni au point 1, écrivez la formule `QUERY` permettant d'afficher :

* Le total du Chiffre d'Affaires par **Catégorie**.
* Uniquement pour les montants individuels supérieurs à **500 €**.
* Avec le montant total trié par ordre croissant.
* En renommant l'en-tête calculée sous le nom **`CA Global`**.

```excel
=QUERY(A1:E11; "SELECT D, SUM(E) WHERE E > 500 GROUP BY D ORDER BY SUM(E) ASC LABEL SUM(E) 'CA Global'"; 1)

```