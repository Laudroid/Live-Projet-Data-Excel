### TP : Nettoyage et Normalisation de Données sous Excel

**Contexte**
Vous disposez d'un fichier `ventes_brutes.csv` issu d'un export système. Ce fichier contient des incohérences de saisie, des problèmes d'encodage (caractères spéciaux) et des formats de données non exploitables pour une analyse croisée.

**Objectif**
Transformer ce jeu de données "sale" en une base propre, prête pour la modélisation et les tableaux croisés dynamiques.

---

### Étape 1 : Diagnostic et Nettoyage de l'encodage
1. Ouvrez le fichier. Si les accents (é, à, ç) apparaissent sous forme de symboles étranges (ex: `Ã©`), fermez le fichier et importez-le via l'onglet **Données > Obtenir des données > À partir d'un fichier texte/CSV**.
2. Choisissez l'origine du fichier **65001 : Unicode (UTF-8)** pour corriger l'encodage.

### Étape 2 : Normalisation des formats
Utilisez les outils de votre choix (formules, Power Query ou IA) pour traiter les colonnes suivantes :

*   **Dates :** La colonne `Date_Vente` est stockée en format texte (ex: "12/05/2023", "2023.05.12", "12-mai-23"). Harmonisez le tout au format `Date` standard d'Excel.
*   **Nombres :** La colonne `Montant` contient des espaces insécables ou des points à la place des virgules. Supprimez ces caractères et convertissez la colonne en format `Nombre` avec deux décimales.
*   **Texte :** La colonne `Client` comporte des espaces inutiles en début ou fin de cellule. Utilisez la fonction `=SUPPRESPACE()` pour nettoyer ces entrées.

### Étape 3 : Détection des erreurs
1. Identifiez les lignes où le `Montant` est vide ou contient du texte.
2. Utilisez la **Mise en forme conditionnelle** pour mettre en évidence les cellules contenant des erreurs (`#VALEUR!`, `#N/A`).
3. Proposez une méthode pour traiter ces lignes (suppression ou imputation par la médiane).

---

### Consignes pour l'utilisation de l'IA
Vous êtes encouragés à utiliser l'IA pour générer les formules complexes ou les scripts Power Query nécessaires. 

**Pour obtenir une aide pertinente, votre prompt doit inclure :**
*   Un échantillon représentatif de vos données (copier-coller 3-4 lignes).
*   Le résultat attendu (ex: "Je veux que cette colonne devienne une date au format JJ/MM/AAAA").
*   Le contexte technique (ex: "Je travaille sur Excel 365, je préfère utiliser Power Query plutôt que des formules").

**Attention :** L'IA peut parfois proposer des solutions qui ne fonctionnent pas sur votre version spécifique d'Excel. Vérifiez toujours le résultat final : une donnée mal normalisée faussera vos futurs calculs (sommes, moyennes, graphiques).

---

**Livrable attendu :**
Un fichier Excel propre, sans aucune erreur de format, accompagné d'une brève note (3 lignes) expliquant la méthode utilisée pour corriger les dates.