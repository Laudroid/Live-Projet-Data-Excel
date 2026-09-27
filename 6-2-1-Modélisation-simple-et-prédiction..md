# 6-2-1 Modélisation simple et prédiction

La modélisation consiste à utiliser des données historiques pour établir une relation mathématique permettant d'estimer des résultats futurs. En entreprise, une modélisation simple suffit souvent à orienter une décision stratégique sans nécessiter d'algorithmes complexes.

## Concepts fondamentaux

*   **Variable cible (Target)** : La valeur que l'on cherche à prédire (ex: chiffre d'affaires du mois prochain).
*   **Variables explicatives (Features)** : Les données utilisées pour effectuer la prédiction (ex: budget marketing, saisonnalité).
*   **Modèle** : La fonction mathématique reliant les variables explicatives à la cible.

## Fonctionnement détaillé

La démarche de modélisation suit une logique de construction progressive :

1.  **Sélection des variables** : Choisir les données ayant une corrélation logique avec la cible.
2.  **Entraînement** : Ajuster les paramètres du modèle sur les données historiques.
3.  **Évaluation** : Mesurer l'écart entre les prédictions du modèle et la réalité observée.
4.  **Prédiction** : Appliquer le modèle aux nouvelles données.

### Exemple : Régression linéaire simple
Pour prédire le temps de réponse d'une API en fonction du nombre de requêtes simultanées :
*   **Variable cible** : Temps de réponse (ms).
*   **Variable explicative** : Nombre de requêtes.
*   **Modèle** : `Temps = (a * Nombre_requêtes) + b`.

## Cas d'usage professionnels

*   **Prévision de ventes** : Estimer les revenus futurs basés sur l'historique et les investissements publicitaires.
*   **Maintenance prédictive** : Prédire la date de défaillance d'un composant matériel en fonction de sa température et de son taux d'utilisation.
*   **Gestion des ressources** : Anticiper le besoin en serveurs cloud selon les pics de trafic saisonniers.

## Comparatif des approches simples

| Modèle | Usage | Avantage |
| :--- | :--- | :--- |
| **Régression Linéaire** | Prédiction de valeurs numériques | Simple à interpréter et expliquer. |
| **Moyenne Mobile** | Lissage de séries temporelles | Idéal pour supprimer le "bruit" saisonnier. |
| **Arbre de décision** | Classification (ex: client fidèle ou non) | Visualisation intuitive des règles. |

## Diagramme de cycle de modélisation

```mermaid
graph LR
    A[Données Historiques] --> B[Entraînement Modèle]
    B --> C[Validation]
    C -->|Erreur élevée| B
    C -->|Erreur acceptable| D[Prédiction sur données futures]
```

## Bonnes pratiques professionnelles

*   **Parcimonie** : Commencez toujours par le modèle le plus simple possible. La complexité n'est pas synonyme de précision.
*   **Séparation des données** : Séparez vos données en deux jeux : un pour l'entraînement (80%) et un pour le test (20%) afin de vérifier la fiabilité du modèle.
*   **Interprétabilité** : Si vous ne pouvez pas expliquer pourquoi le modèle prédit un résultat, il sera difficile de convaincre les décideurs de l'utiliser.

## Erreurs fréquentes à éviter

*   **Sur-apprentissage (Overfitting)** : Créer un modèle qui "apprend par cœur" les données historiques mais échoue totalement sur de nouvelles données.
*   **Extrapolation dangereuse** : Utiliser un modèle pour prédire des valeurs très éloignées de la plage de données utilisée pour l'entraînement.
*   **Négliger les facteurs externes** : Oublier des variables critiques (ex: un changement de réglementation ou une crise économique) qui invalident le modèle.

## Points de vigilance

*   **Qualité des données d'entrée** : Un modèle, aussi sophistiqué soit-il, produira des résultats erronés si les données sources sont biaisées ou incomplètes.
*   **Maintenance** : Un modèle est périssable. Les relations entre variables évoluent avec le temps ; prévoyez un ré-entraînement périodique.

## Sources

*   *Gareth James et al., "An Introduction to Statistical Learning".*
*   *Documentation officielle : Scikit-learn (pour les concepts de base de modélisation).*