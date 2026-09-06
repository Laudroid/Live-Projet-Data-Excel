### TP : Importation et Exploration de Données avec Excel

**Matériel requis :**
*   Fichier source : `ventes_brutes.csv` (téléchargeable sur la plateforme).
*   Logiciel : Microsoft Excel (version 2016 ou ultérieure).

---

#### Étape 1 : Importation des données
L'objectif est d'intégrer le fichier CSV sans altérer les données sources.

1.  Ouvrez un classeur Excel vierge.
2.  Allez dans l'onglet **Données** > **Obtenir des données** > **À partir d'un fichier** > **À partir d'un fichier texte/CSV**.
3.  Sélectionnez `ventes_brutes.csv`.
4.  Dans la fenêtre de prévisualisation, vérifiez la détection du délimiteur (généralement la virgule ou le point-virgule).
5.  Cliquez sur **Transformer les données** pour ouvrir l'éditeur Power Query.

#### Étape 2 : Nettoyage et typage (Power Query)
Avant toute analyse, assurez-vous que les données sont exploitables.

1.  **Typage :** Vérifiez que chaque colonne possède le bon format (Date, Nombre décimal, Texte). Modifiez les types si nécessaire via l'icône à gauche du nom de la colonne.
2.  **Suppression des erreurs :** Identifiez les lignes vides ou les cellules contenant des erreurs (`Error`) et filtrez-les.
3.  **Renommage :** Renommez les colonnes pour qu'elles soient explicites (ex: `Date_Vente` au lieu de `Col1`).
4.  Cliquez sur **Fermer et charger**.

#### Étape 3 : Exploration structurelle
Une fois les données chargées dans une feuille Excel, répondez aux questions suivantes pour valider la qualité du dataset :

1.  **Volume :** Combien de lignes et de colonnes comporte le jeu de données ?
2.  **Intégrité :** Y a-t-il des valeurs manquantes dans les colonnes clés (ex: `ID_Client` ou `Montant`) ? Utilisez la mise en forme conditionnelle pour les mettre en évidence.
3.  **Distribution :** Créez un tableau croisé dynamique rapide pour afficher le nombre de ventes par catégorie de produit.
4.  **Cohérence :** La plage de dates est-elle logique (ex: pas de dates dans le futur) ?

---

#### Note sur l'utilisation de l'IA
Vous êtes encouragés à utiliser des outils d'IA (ChatGPT, Claude, Copilot) pour vous assister. Si vous rencontrez une erreur de formatage ou si vous cherchez une formule spécifique pour nettoyer vos données :
*   **Formulez votre prompt avec précision :** Précisez la structure de vos colonnes et le résultat attendu.
*   **Vérifiez les suggestions :** L'IA peut parfois proposer des solutions basées sur des versions d'Excel différentes de la vôtre. Testez toujours la logique proposée avant de l'appliquer massivement à votre dataset.
*   **Documentez :** Si vous utilisez une formule complexe générée par une IA, ajoutez un commentaire dans votre cellule pour expliquer sa fonction. Cela facilitera la maintenance de votre projet.

**Livrable attendu :**
Un fichier Excel propre, avec une feuille "Données" (issue de Power Query) et une feuille "Exploration" contenant vos observations sur la structure du dataset.