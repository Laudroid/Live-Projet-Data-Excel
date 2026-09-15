### TP : Analyse multidimensionnelle avec les Tableaux Croisés Dynamiques (TCD)

#### 1. Contexte et Données
Vous disposez d’un fichier Excel nommé `Ventes_Globales.xlsx`. Il contient un historique de transactions avec les colonnes suivantes : 
*   `Date`
*   `Région`
*   `Catégorie de produit`
*   `Vendeur`
*   `Chiffre d'affaires (CA)`
*   `Quantité vendue`

#### 2. Objectifs
Maîtriser la synthèse de données volumineuses pour extraire des indicateurs de performance (KPI) sans modifier la base source.

#### 3. Travail à réaliser

**Étape 1 : Préparation**
*   Transformez votre plage de données en **Tableau Excel** (raccourci : `Ctrl + L` ou `Ctrl + T`). Nommez ce tableau `DonnéesVentes`.
*   *Note :* L'utilisation d'un tableau structuré permet à vos TCD de se mettre à jour automatiquement si vous ajoutez de nouvelles lignes.

**Étape 2 : Création des vues analytiques**
Créez trois feuilles distinctes pour les analyses suivantes :

1.  **Analyse géographique et temporelle :**
    *   Lignes : `Région`
    *   Colonnes : `Date` (groupez les dates par "Mois").
    *   Valeurs : Somme du `Chiffre d'affaires`.
    *   *Question :* Quelle région affiche la plus forte saisonnalité ?

2.  **Performance par catégorie :**
    *   Lignes : `Catégorie de produit`
    *   Valeurs : Somme du `Chiffre d'affaires` et Moyenne de la `Quantité vendue`.
    *   *Action :* Appliquez un tri décroissant sur le CA.

3.  **Analyse des vendeurs :**
    *   Lignes : `Vendeur`
    *   Filtre : `Région`
    *   Valeurs : Somme du `Chiffre d'affaires`.
    *   *Action :* Insérez un **Slicer (Segment)** sur la colonne `Catégorie de produit` pour filtrer dynamiquement les résultats.

#### 4. Utilisation de l'IA
Vous êtes encouragés à utiliser des outils d'IA (ChatGPT, Claude, Copilot) pour :
*   **Optimiser vos formules :** Si vous devez créer des champs calculés complexes dans le TCD.
*   **Interprétation :** Copiez un tableau de résultats et demandez à l'IA d'identifier les 3 tendances majeures ou les anomalies (ex: "Quelles sont les régions sous-performantes en mars ?").
*   **Dépannage :** Si vous rencontrez une erreur de type `#VALEUR!` ou un problème de groupement de dates, décrivez le problème à l'IA en précisant le format de vos données.

*Attention :* L'IA peut parfois suggérer des solutions basées sur des versions d'Excel différentes de la vôtre. Vérifiez toujours la cohérence des résultats obtenus avec les données sources.

#### 5. Livrable
Un fichier Excel contenant :
1.  La feuille "Données" propre.
2.  Les trois feuilles de TCD nommées explicitement.
3.  Une courte note (3-4 lignes) sur la conclusion principale que vous tirez de l'analyse croisée "Région / Mois".