# Gabarit imposé pour les corrigés

Document de travail interne. Chaque corrigé suit cette structure, dans cet
ordre, sans section supplémentaire ni manquante.

---

## Structure

```markdown
# Corrigé — <titre exact de l'exercice>

**Fichier(s) de données :** `<nom>` (<n> lignes, <n> colonnes)
**Durée indicative :** <n> min
**Prérequis :** <ce que l'apprenant doit déjà savoir faire>

---

## 1. Ce que l'exercice évalue réellement

Deux ou trois phrases. La compétence visée, et surtout le piège central que
le jeu de données a été construit pour révéler. Pas de paraphrase de
l'énoncé.

## 2. Corrigé pas à pas

Une sous-section `### Étape n — <intitulé de l'énoncé>` par étape de
l'énoncé, dans l'ordre de l'énoncé. Pour chaque étape :

* la manipulation exacte (chemin de menu complet en gras pour l'interface) ;
* la ou les formules, en syntaxe française, dans un bloc de code ;
* quand la formule est longue, une ligne d'explication par argument ;
* la variante Power Query lorsqu'elle est plus robuste que la formule, avec
  le code M si la transformation n'est pas atteignable par l'interface.

## 3. Valeurs de contrôle

Tableau des résultats numériques attendus. Reprendre les valeurs de
`corriges/valeurs-de-reference.md` telles quelles — jamais de valeur
recalculée de tête ni arrondie différemment.

## 4. Erreurs fréquentes

Tableau à trois colonnes : `Symptôme dans la copie` | `Cause` |
`Comment le vérifier en 10 secondes`. Cinq à huit lignes. Ce sont les
erreurs que CE jeu de données provoque, pas des généralités.

## 5. Volet IA

Ce qu'on attend dans la copie au titre des consignes IA de l'énoncé, et
comment distinguer un apprenant qui a compris d'un apprenant qui a
recopié. Une question de vérification orale, précise, à poser en soutenance.

## 6. Barème indicatif

Tableau `Critère` | `Points` | `Observable`. Total sur 20. La colonne
observable décrit un fait vérifiable dans le fichier rendu, pas une
impression.

## 7. Prolongements

Deux ou trois pistes pour les apprenants rapides. Une phrase chacune.
```

---

## Règles de rédaction

1. **Français, texte brut, aucun emoji.** Pas de tutoiement des apprenants
   dans un document destiné au formateur : on parle de « l'apprenant ».
2. **Syntaxe française des formules**, séparateur d'arguments `;` :
   `SOMME.SI.ENS`, `NB.SI.ENS`, `RECHERCHEX`, `SIERREUR`, `SUPPRESPACE`,
   `NOMPROPRE`, `TEXTEAVANT`, `TEXTEAPRES`, `SI.NON.DISP`, `ANNEE`, `MOIS`,
   `TEXTE`, `CNUM`, `DATEVAL`, `SUBSTITUE`, `MEDIANE`.
   Donner l'équivalent anglais entre parenthèses à la première occurrence
   d'une fonction dans le document : `RECHERCHEX` (XLOOKUP).
3. **Aucune valeur inventée.** Tout chiffre cité vient de
   `corriges/valeurs-de-reference.md`. En cas de doute, recalculer avec
   pandas sur le fichier livré plutôt que d'estimer.
4. **Formules testées mentalement sur les vraies colonnes.** Les noms de
   colonnes, d'onglets et de tableaux structurés doivent correspondre
   exactement au fichier de données livré. Vérifier avec pandas avant
   d'écrire une référence structurée du type `Ventes[Date_Vente]`.
5. **Pas de solution unique imposée** quand plusieurs voies se valent
   (formule / Power Query / TCD) : donner la voie recommandée, puis
   mentionner l'alternative acceptable en une ligne. Préciser laquelle est
   attendue au barème.
6. **QUERY est une fonction Google Sheets.** Elle n'existe pas dans Excel :
   le corrigé concerné doit le dire explicitement et rappeler que le
   séparateur d'arguments dépend des paramètres régionaux du classeur.
7. **Longueur cible : 200 à 320 lignes** par corrigé. Dense, pas bavard.
8. Ne jamais modifier les fichiers d'énoncé ni les fichiers de données.
