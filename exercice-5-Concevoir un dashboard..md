### TP : Conception d'un Dashboard de Pilotage sous Excel

**Contexte**
Vous disposez d'un jeu de données (Dashboard_Source.xlsx) contenant 906 lignes. Votre mission est de transformer ces données brutes en un outil d'aide à la décision interactif.

**Objectifs pédagogiques**
*   Structurer et nettoyer des données pour la modélisation.
*   Sélectionner et calculer des KPIs pertinents.
*   Utiliser les segments (slicers) et la chronologie pour l'interactivité.
*   Appliquer les principes de visualisation de données (Data Viz).

---

### Étape 1 : Préparation et Modélisation
1.  **Nettoyage :** Assurez-vous que vos données sont sous forme de tableau Excel (`Ctrl + T`). Vérifiez l'absence de doublons et la cohérence des formats (dates, devises).
2.  **Calculs :** Ajoutez les colonnes calculées nécessaires à vos futurs KPIs (ex: marge unitaire, taux de croissance, catégories de performance).
3.  **IA Assist :** Vous pouvez utiliser l'IA pour générer des formules complexes (ex: `SI` imbriqués, `RECHERCHEV`/`XLOOKUP` ou calculs de ratios) ou pour suggérer des noms de colonnes pertinents. *Veillez à comprendre la logique de la formule générée avant de l'intégrer.*

### Étape 2 : Extraction des KPIs
Identifiez 3 à 5 KPIs stratégiques. Pour chacun, créez un tableau croisé dynamique (TCD) dédié.
*   *Exemple de KPIs :* Chiffre d'affaires total, Panier moyen, Taux de conversion, Évolution mensuelle des ventes.
*   **Conseil :** Ne surchargez pas votre dashboard. Chaque KPI doit répondre à une question métier précise.

### Étape 3 : Design et Interactivité
1.  **Mise en page :** Créez une feuille nommée "Dashboard". Masquez le quadrillage et les en-têtes de lignes/colonnes pour un rendu professionnel.
2.  **Visualisation :** Associez chaque TCD à un graphique adapté (courbes pour les tendances, barres pour les comparaisons, jauges ou cartes pour les KPIs isolés).
3.  **Interactivité :** Insérez au moins deux **Segments (Slicers)** et une **Chronologie** pour permettre le filtrage dynamique de l'ensemble des graphiques.
4.  **Connexion :** Assurez-vous que vos segments sont connectés à tous les TCD de votre dashboard (clic droit sur le segment > "Connexions de rapport").

### Étape 4 : Revue critique (Auto-évaluation)
Répondez aux questions suivantes pour valider votre travail :
*   Si un utilisateur n'a que 10 secondes pour regarder le dashboard, comprend-il immédiatement la performance globale ?
*   Les couleurs utilisées sont-elles cohérentes et lisibles (respect de la charte graphique) ?
*   L'IA a-t-elle été utilisée pour optimiser le temps de traitement ou pour masquer une lacune technique ? (Soyez prêt à expliquer vos choix).

---

**Livrable attendu :**
Un fichier Excel unique contenant :
1.  L'onglet "Données" (propre et structuré).
2.  L'onglet "Calculs" (TCD sources).
3.  L'onglet "Dashboard" (interactif et épuré).

*Note : L'utilisation de l'IA est encouragée pour la rédaction des formules et la recherche d'idées de visualisation. Cependant, la mise en forme et la pertinence des KPIs doivent refléter votre compréhension métier.*