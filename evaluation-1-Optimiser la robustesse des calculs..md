### TP : Fiabilisation des calculs et gestion des erreurs

#### Contexte
Dans un projet Data, la qualité des résultats dépend de la robustesse des formules. Les fonctions de recherche (`RECHERCHEV`, `XLOOKUP`) ou les calculs arithmétiques (divisions) renvoient souvent des erreurs (`#N/A`, `#DIV/0!`) lorsque les données sources sont incomplètes ou manquantes. L'objectif est de rendre vos tableaux "propres" et exploitables pour un utilisateur final.

#### Prérequis
*   Un fichier Excel contenant un jeu de données (ex: une liste de ventes avec des prix et des quantités).
*   Une zone de recherche utilisant `RECHERCHEV` ou `XLOOKUP`.

---

#### Exercice 1 : Nettoyage des recherches
1.  Créez une formule de recherche qui renvoie le prix d'un produit à partir d'un code saisi dans une cellule.
2.  Testez la formule avec un code inexistant. Vous obtenez une erreur `#N/A`.
3.  **Consigne :** Enveloppez votre formule dans une fonction `SIERREUR` (ou `IFERROR`) pour afficher le message "Code introuvable" au lieu de l'erreur système.

#### Exercice 2 : Sécurisation des calculs arithmétiques
1.  Calculez un taux de variation ou une marge unitaire (division).
2.  Provoquez une erreur `#DIV/0!` en saisissant une valeur nulle ou vide dans le dénominateur.
3.  **Consigne :** Modifiez votre formule pour que, en cas d'erreur, Excel affiche "0%" ou "Données manquantes" au lieu du code erreur.

#### Exercice 3 : Analyse critique (Utilisation de l'IA)
Vous avez probablement utilisé une IA pour générer ou corriger vos formules. Pour valider votre compréhension :
1.  Expliquez, en une phrase, pourquoi il est préférable d'utiliser `SIERREUR` plutôt que de laisser les erreurs apparentes dans un rapport de données.
2.  Si l'IA vous propose une formule complexe, vérifiez si elle est bien imbriquée (ex: `SIERREUR(RECHERCHEV(...); "Message")`). 
3.  **Défi :** Pouvez-vous imbriquer deux `SIERREUR` pour traiter des cas d'erreurs différents (ex: une erreur de recherche vs une erreur de calcul) ?

---

#### Livrable attendu
1/ Un fichier Excel propre où aucune cellule ne contient de code erreur (`#N/A`, `#VALEUR!`, `#DIV/0!`). 

2/ Un fichier `USAGE-IA.md` ou `USAGE-IA.txt`
L'usage d'un assistant d'IA générative est autorisé et n'a pas à être dissimulé. Il doit en revanche être documenté. Tout rendu sans ce fichier est incomplet, y compris si aucune IA n'a été utilisée : dans ce cas, le fichier le déclare explicitement.
Le fichier doit permettre à un relecteur de comprendre où s'arrête votre production et où commence celle de la machine. Une entrée par sollicitation significative, dans l'ordre chronologique :
```markdown
# USAGE-IA — TP 2 — <Nom Prénom>

Outil(s) utilisé(s) : <nom et version/modèle>
Déclaration : [ ] je n'ai utilisé aucune IA sur ce TP  /  [x] entrées ci-dessous

## Entrée 1
- Date et heure :
- Partie du TP concernée :
- Pourquoi j'ai sollicité l'IA : (blocage, gain de temps, exploration d'alternatives,
  relecture, génération de données de test...)
- Ce que j'ai demandé (résumé de la requête, pas nécessairement le prompt intégral) :
- Ce que j'ai obtenu :
- Décision : acceptée telle quelle / acceptée après correction / refusée
- Si refusée ou corrigée, pourquoi : (API inexistante ou obsolète, erreur de compilation,
  hors périmètre du TP, solution inutilement complexe, mauvaise gestion d'un cas limite,
  code non conforme aux consignes, incompréhension de ma part...)
- Correction apportée et vérification faite :

## Entrée 2
...
