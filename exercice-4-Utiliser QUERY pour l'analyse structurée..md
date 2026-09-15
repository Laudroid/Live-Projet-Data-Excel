### TP : Analyse de données avec QUERY

**Contexte**
Vous disposez d'un jeu de données de ventes (onglet `Data_Ventes`) contenant les colonnes suivantes :
*   **Date** (A)
*   **Catégorie** (B)
*   **Produit** (C)
*   **Vendeur** (D)
*   **Montant** (E)
*   **Région** (F)

**Objectif**
Maîtriser la syntaxe SQL intégrée à Google Sheets pour filtrer, trier et agréger des données sans utiliser de tableaux croisés dynamiques.

---

### Exercice 1 : Filtrage multi-critères
Dans un nouvel onglet, utilisez la fonction `QUERY` pour extraire uniquement les lignes répondant aux conditions suivantes :
1.  La catégorie est "Électronique".
2.  Le montant est supérieur à 500 €.
3.  La région est "Nord" ou "Sud".

*Conseil : Soyez attentifs à la syntaxe des guillemets simples et doubles dans votre clause `WHERE`.*

### Exercice 2 : Agrégation et tri
Générez un tableau récapitulatif qui affiche :
1.  Le nom du **Vendeur**.
2.  La **somme des montants** par vendeur.
3.  Le résultat doit être trié par ordre décroissant du chiffre d'affaires total.
4.  Excluez les vendeurs dont le total est inférieur à 1 000 €.

*Indice : Utilisez les clauses `GROUP BY`, `SUM()` et `HAVING`.*

### Exercice 3 : Analyse dynamique
Créez deux cellules de saisie (ex: `H1` pour la catégorie et `H2` pour la région). Modifiez votre formule `QUERY` pour qu'elle utilise ces cellules comme variables de filtrage.

*Note : Pour concaténer une référence de cellule dans une requête, utilisez la syntaxe : `"... WHERE B = '"&H1&"' ..."`.*

---

### Consignes pour l'utilisation de l'IA
L'usage de l'IA est autorisé pour vous aider à déboguer vos erreurs de syntaxe. Si vous soumettez votre code à une IA :
*   **Ne copiez-collez pas simplement la réponse.**
*   Demandez-lui d'expliquer pourquoi une clause spécifique (ex: `LABEL` ou `FORMAT`) est nécessaire.
*   Si votre requête renvoie une erreur `#VALUE!`, essayez d'isoler la partie de la clause `WHERE` qui pose problème avant de demander une correction.

**Livrable attendu :**
Un fichier Sheets contenant vos trois requêtes fonctionnelles. Ajoutez un commentaire sur la cellule de chaque résultat expliquant brièvement la logique de votre clause `SELECT`.