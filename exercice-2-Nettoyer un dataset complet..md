### TP : Nettoyage et fiabilisation d'un jeu de données client

**Contexte**
Vous disposez d'un fichier `clients_brut.xlsx` contenant des données extraites d'un CRM. Ce fichier présente des incohérences de saisie, des doublons et des cellules vides. Votre mission est de transformer ces données en une base propre et exploitable.

**Consignes générales**
*   Vous êtes autorisés à utiliser des outils d'IA pour générer vos formules ou déboguer vos scripts.
*   **Important :** Si vous utilisez l'IA, commentez brièvement dans votre rendu la logique de la formule obtenue pour démontrer votre compréhension.

---

#### Étape 1 : Standardisation des données textuelles
Le fichier contient des noms et des adresses saisis de manière hétérogène (majuscules/minuscules, espaces inutiles).

1.  **Nettoyage des noms :** Utilisez les fonctions `NOMPROPRE` et `SUPPRESPACE` pour harmoniser la colonne "Nom" (ex: "  dupont  jean " doit devenir "Dupont Jean").
2.  **Extraction d'informations :** Dans la colonne "Adresse", le code postal et la ville sont concaténés (ex: "75001 Paris"). Utilisez les fonctions `GAUCHE`, `DROITE`, `STXT` ou `TEXTEAVANT`/`TEXTEAPRES` pour séparer ces deux éléments dans deux colonnes distinctes.

#### Étape 2 : Gestion des doublons
Certains clients apparaissent plusieurs fois suite à des erreurs de saisie.

1.  Identifiez les doublons basés sur la combinaison "Nom" + "Email".
2.  Utilisez l'outil **Données > Supprimer les doublons**.
3.  *Réflexion :* Avant de supprimer, créez une colonne "Statut" et utilisez une formule `NB.SI` pour marquer les lignes en doublon. Pourquoi est-il préférable de marquer les données avant de les supprimer définitivement ?

#### Étape 3 : Traitement des valeurs manquantes
La colonne "Téléphone" comporte des cellules vides ou des formats invalides.

1.  Identifiez les cellules vides à l'aide de la **Mise en forme conditionnelle**.
2.  Remplacez les valeurs manquantes par la mention "Non renseigné" en utilisant la fonction `SI` ou `SI.NON.DISP`.
3.  Appliquez un format de cellule personnalisé pour forcer l'affichage des numéros de téléphone sur 10 chiffres (ex: 01 23 45 67 89).

---

### Livrables attendus
1.  Le fichier Excel final nettoyé.
2.  Un court document (ou commentaire dans le fichier) listant les fonctions principales utilisées pour chaque étape.
3.  Si vous avez utilisé l'IA pour une formule complexe, copiez-collez le prompt que vous avez utilisé et expliquez pourquoi cette solution est la plus adaptée.

**Critères d'évaluation**
*   **Fiabilité :** Absence d'espaces superflus et cohérence des formats.
*   **Méthodologie :** Utilisation pertinente des fonctions Excel plutôt que de la saisie manuelle.
*   **Esprit critique :** Capacité à expliquer les choix techniques effectués, même avec l'aide de l'IA.