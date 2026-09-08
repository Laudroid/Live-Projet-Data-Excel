### TP : Analyse et Synthèse de Données avec Excel

**Contexte**
Vous disposez d'un jeu de données contenant les ventes d'une entreprise sur le dernier trimestre. Votre mission est d'enrichir ces données à partir d'un référentiel externe et de générer des indicateurs de performance clés (KPI).

**Fichiers fournis**
1. `Ventes.xlsx` : Contient les colonnes *Date, ID_Produit, Quantité, ID_Magasin*.
2. `Referentiel.xlsx` : Contient deux onglets :
   - `Produits` : *ID_Produit, Nom_Produit, Prix_Unitaire*.
   - `Magasins` : *ID_Magasin, Nom_Magasin, Ville, Région*.

---

### Partie 1 : Enrichissement du Dataset (Recherche)
L'objectif est de consolider toutes les informations dans le tableau `Ventes`.

1. **Ajout des informations produits** : Utilisez la fonction `XLOOKUP` (ou `RECHERCHEX`) pour rapatrier le *Nom_Produit* et le *Prix_Unitaire* dans le tableau `Ventes` en vous basant sur l' `ID_Produit`.
2. **Ajout des informations géographiques** : Utilisez `XLOOKUP` pour rapatrier la *Région* du magasin dans le tableau `Ventes` en vous basant sur l' `ID_Magasin`.
3. **Calcul du Chiffre d'Affaires (CA)** : Créez une colonne calculée `CA` = `Quantité` * `Prix_Unitaire`.

---

### Partie 2 : Synthèse et Agrégation
Créez un tableau de bord simple sur une nouvelle feuille nommée "Synthèse" pour répondre aux questions suivantes :

1. **Performance par Région** : Utilisez `SUMIFS` (ou `SOMME.SI.ENS`) pour calculer le CA total généré par chaque région.
2. **Volume de ventes** : Utilisez `COUNTIFS` (ou `NB.SI.ENS`) pour compter le nombre de transactions ayant une quantité supérieure à 10 unités, par région.
3. **Analyse croisée** : Calculez le CA total pour un produit spécifique dans une région spécifique (ex: "Produit A" dans la région "Nord").

---

### Consignes pour l'utilisation de l'IA
L'usage de l'IA est autorisé pour vous aider à structurer vos formules ou déboguer des erreurs. 

*   **Conseil méthodologique** : Si vous demandez une formule à une IA, essayez de comprendre la logique des arguments (matrice de recherche, matrice de retour, mode de correspondance). 
*   **Vérification** : Ne copiez-collez pas aveuglément. Testez vos résultats sur un échantillon de 5 lignes pour vérifier que les montants correspondent à la réalité de vos données.
*   **Documentation** : Si vous utilisez une fonction complexe générée par une IA, ajoutez un commentaire dans votre cellule (clic droit > Insérer un commentaire) expliquant brièvement ce que fait la formule. Cela vous sera utile pour vos futures révisions.

---

### Livrables attendus
*   Le fichier Excel final avec les colonnes enrichies.
*   Le tableau de synthèse avec les fonctions d'agrégation correctement paramétrées.
*   *Auto-évaluation* : Identifiez une situation où `XLOOKUP` est plus avantageux que l'ancien `VLOOKUP` (RECHERCHEV). Notez votre réponse dans une cellule isolée de votre fichier.