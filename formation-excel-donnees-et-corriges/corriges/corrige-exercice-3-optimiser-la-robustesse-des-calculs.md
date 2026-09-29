# Corrigé — Optimiser la robustesse des calculs

**Fichier(s) de données :** `Suivi_Marges.xlsx` (3 onglets : `Catalogue` 33 références, `Saisies` 120 lignes, `Recherche` zone de saisie)
**Durée indicative :** 45 min
**Prérequis :** Maîtrise de RECHERCHEX (XLOOKUP) ou RECHERCHEV (VLOOKUP), notion de gestion d'erreur avec SIERREUR (IFERROR)

---

## 1. Ce que l'exercice évalue réellement

L'exercice évalue la capacité à distinguer les origines d'une erreur Excel et à les traiter sélectivement. Le piège central est le suivant : SIERREUR intercepte toutes les erreurs sans les nommer, ce qui conduit à masquer indistinctement un `#N/A` (code produit absent du catalogue) et un `#DIV/0!` (prix de vente nul ou objectif nul). Or les deux anomalies n'ont pas la même signification métier : la première est une erreur de saisie, la seconde est une donnée en cours de traitement. Un apprenant qui imbrique deux SIERREUR pour « traiter des cas différents » obtient en réalité la même interception que s'il en avait posé un seul. Le point discriminant est la maîtrise de SI.NON.DISP (IFNA), qui intercepte uniquement `#N/A`, combinée à SIERREUR pour le `#DIV/0!`.

---

## 2. Corrigé pas à pas

### Structure du fichier

Les noms exacts des onglets sont `Catalogue`, `Saisies` et `Recherche`. Les tableaux structurés portent les mêmes noms.

Colonnes du tableau `Catalogue` : `Code_Produit`, `Designation`, `Prix_Achat`, `Prix_Vente`.
Colonnes du tableau `Saisies` : `ID_Ligne`, `Date`, `Code_Produit`, `Quantite_Vendue`, `CA_Realise`, `CA_Objectif`, puis trois colonnes vides marquées `(à compléter)` :
- colonne G : `Prix_Vente_Catalogue (à compléter)`
- colonne H : `Marge_Unitaire (à compléter)`
- colonne I : `Taux_Atteinte_Objectif (à compléter)`

### Exercice 1 — Colonne G : rapatrier le prix de vente catalogue (SIERREUR)

Sans protection d'erreur, la formule de base est :

```
=RECHERCHEX([@Code_Produit];
            Catalogue[Code_Produit];
            Catalogue[Prix_Vente])
```

Les 9 lignes portant les codes P777, P812 ou P950 (absents du catalogue) retournent `#N/A`. Pour afficher le message demandé par l'énoncé à la place de l'erreur :

```
=SIERREUR(
    RECHERCHEX([@Code_Produit];
               Catalogue[Code_Produit];
               Catalogue[Prix_Vente]);
    "Code introuvable"
)
```

- L'argument `valeur_si_erreur` de SIERREUR intercepte toute erreur renvoyée par RECHERCHEX, y compris `#N/A`.
- Le résultat pour les 9 lignes orphelines est la chaîne de texte `"Code introuvable"`.
- Les 111 lignes valides affichent le prix numérique issu du catalogue.

**Note pédagogique :** RECHERCHEX dispose aussi d'un argument `si_non_trouve` (quatrième position) qui évite d'imbriquer SIERREUR pour le cas de recherche. La formule équivalente et plus lisible est :

```
=RECHERCHEX([@Code_Produit];
            Catalogue[Code_Produit];
            Catalogue[Prix_Vente];
            "Code introuvable")
```

Les deux formulations sont acceptées au barème.

### Exercice 2 — Colonne H : marge unitaire sécurisée (SIERREUR sur division)

La marge unitaire est le bénéfice brut réalisé par unité vendue : prix de vente effectif moyen (CA réalisé divisé par la quantité vendue) moins le coût d'achat unitaire issu du catalogue.

```
=SIERREUR(
    [@CA_Realise] / [@Quantite_Vendue]
    - RECHERCHEX([@Code_Produit];
                 Catalogue[Code_Produit];
                 Catalogue[Prix_Achat]);
    "Données manquantes"
)
```

Deux sources de `#DIV/0!` dans cette formule :
- Les 7 lignes où `Quantite_Vendue` est nulle ou vide (dénominateur direct).
- Aucun `#DIV/0!` supplémentaire issu du catalogue : la soustraction de `Prix_Achat` ne comporte pas de division.

Les 9 lignes orphelines produisent `#N/A` sur le RECHERCHEX de `Prix_Achat` ; SIERREUR les intercepte également et affiche `"Données manquantes"`. C'est voulu à cette étape : l'apprenant verra la valeur identique pour deux types d'anomalies distincts — c'est précisément ce que le défi de l'exercice 3 cherche à corriger.

**Colonne I — Taux d'atteinte de l'objectif :**

```
=SIERREUR(
    [@CA_Realise] / [@CA_Objectif];
    "Données manquantes"
)
```

Les 6 lignes où `CA_Objectif` est nul ou vide déclenchent `#DIV/0!`, intercepté par SIERREUR.

### Exercice 3 — Onglet Recherche : formules dynamiques avec discrimination des erreurs

L'onglet `Recherche` contient une cellule de saisie `B3` (fond jaune) et trois cellules de résultat à compléter : `B5` (Désignation), `B6` (Prix de vente), `B7` (Taux de marge).

**Cellule B5 — Désignation :**

```
=SIERREUR(
    RECHERCHEX(B3; Catalogue[Code_Produit]; Catalogue[Designation]);
    "Code introuvable"
)
```

**Cellule B6 — Prix de vente :**

```
=SIERREUR(
    RECHERCHEX(B3; Catalogue[Code_Produit]; Catalogue[Prix_Vente]);
    "Code introuvable"
)
```

**Cellule B7 — Taux de marge : c'est ici que se joue le point discriminant**

La formule naïve serait :

```
=SIERREUR(
    SIERREUR(
        (RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente])
         - RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Achat]))
        / RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente]);
        "Taux incalculable (prix nul)"
    );
    "Code introuvable"
)
```

Cette imbrication produit un résultat visuellement différent pour les deux cas, mais elle ne discrimine pas correctement. Voici pourquoi :

- Pour P777 (code absent) : le RECHERCHEX interne retourne `#N/A`. Le SIERREUR interne intercepte `#N/A` et affiche `"Taux incalculable (prix nul)"` — message trompeur, car la vraie cause est l'absence du code.
- Pour P105 (prix de vente = 0) : la division par 0 produit `#DIV/0!`. Le SIERREUR interne intercepte `#DIV/0!` et affiche `"Taux incalculable (prix nul)"` — message exact cette fois.

Les deux situations affichent le même message, ce qui ne permet pas à l'utilisateur de l'onglet Recherche de distinguer une erreur de saisie d'un produit en cours de tarification.

**Formule correcte et discriminante :**

```
=SI.NON.DISP(
    SIERREUR(
        (RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente])
         - RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Achat]))
        / RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente]);
        "Taux incalculable (prix de vente nul)"
    );
    "Code introuvable"
)
```

- SI.NON.DISP (IFNA) n'intercepte que `#N/A`. Si le code est absent du catalogue, les RECHERCHEX retournent `#N/A` ; SI.NON.DISP le capte et affiche `"Code introuvable"`.
- SIERREUR (IFERROR), qui englobe la division, intercepte `#DIV/0!` quand le prix de vente est 0 et affiche `"Taux incalculable (prix de vente nul)"`.
- Pour P003 (cas nominal), aucune erreur n'est levée : le résultat est 34,95 %.

L'alternative sans SIERREUR imbriqué passe par un test explicite du dénominateur :

```
=SI.NON.DISP(
    SI(RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente])=0;
       "Taux incalculable (prix de vente nul)";
       (RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente])
        - RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Achat]))
       / RECHERCHEX(B3;Catalogue[Code_Produit];Catalogue[Prix_Vente]));
    "Code introuvable"
)
```

Cette variante est plus verbeuse mais plus explicite sur la logique ; elle est acceptée au barème avec la même note.

**Sur l'intérêt et les limites de SIERREUR dans un rapport :**

SIERREUR est utile quand on sait qu'une erreur est normale et attendue et qu'on veut présenter un résultat propre à un lecteur final (dashboard, rapport imprimé). Poser SIERREUR sur la cellule d'affichage — en bout de chaîne — est la bonne pratique : l'erreur reste visible dans les cellules intermédiaires, ce qui permet de détecter les anomalies de données lors de la maintenance.

Poser SIERREUR trop en amont, sur une cellule source qui alimente d'autres formules, masque les anomalies avant qu'elles soient détectées. Par exemple, remplacer les `#N/A` de la colonne G (`Prix_Vente_Catalogue`) par 0 dès la recherche fait calculer silencieusement une marge fausse sur les 9 lignes orphelines, sans aucun signal visible.

---

## 3. Valeurs de contrôle

| Contrôle | Valeur attendue |
|---|---|
| Lignes de `Saisies` | 120 |
| Lignes affichant `"Code introuvable"` en colonne G après SIERREUR | 9 (codes P777, P812, P950) |
| Lignes affichant `"Données manquantes"` en colonne H | 16 (9 orphelins + 7 quantités nulles/vides) |
| Lignes affichant `"Données manquantes"` en colonne I | 6 (objectifs nuls ou vides) |
| B5 pour code `P003` | Écran 27 pouces Lumen |
| B6 pour code `P003` | 329,00 € |
| B7 pour code `P003` | 34,95 % |
| B5 pour code `P105` | Étagère modulaire Strate |
| B6 pour code `P105` | 0,00 € |
| B7 pour code `P105` avec formule discriminante | Taux incalculable (prix de vente nul) |
| B5 pour code `P777` avec formule discriminante | Code introuvable |
| B7 pour code `P777` avec formule discriminante | Code introuvable |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| Colonne G affiche 0 au lieu de `"Code introuvable"` pour les orphelins | L'apprenant a utilisé l'argument `si_non_trouve` de RECHERCHEX avec la valeur `0` au lieu du texte | Filtrer la colonne `Code_Produit` sur `P777` : la colonne G doit afficher texte, pas 0 |
| B7 affiche `"Taux incalculable"` pour P777 (code absent) | Le SIERREUR interne intercepte le `#N/A` de la recherche avant SI.NON.DISP — les deux SIERREUR imbriqués ne discriminent pas | Saisir P777 en B3 et lire B7 : le message doit contenir "introuvable", pas "prix nul" |
| B7 affiche `"Code introuvable"` pour P105 (prix = 0) | SI.NON.DISP mal positionné : il capte le `#DIV/0!` parce qu'il englobe toute l'expression | Saisir P105 en B3 : B5 et B6 doivent être renseignés, seul B7 doit afficher le message de prix nul |
| Colonne I affiche erreur au lieu de `"Données manquantes"` | SIERREUR omis sur la division `CA_Realise / CA_Objectif` | Trouver une ligne où `CA_Objectif` est vide (colonne F) et vérifier la cellule I correspondante |
| Formule en B7 refuse de se calculer | Références structurées invalides car le nom du tableau est mal orthographié | Vérifier dans **Formules > Gestionnaire de noms** que les tableaux s'appellent exactement `Catalogue`, `Saisies` |
| Les 9 lignes orphelines ne produisent pas `"Code introuvable"` mais une valeur numérique | L'apprenant a saisi les prix manuellement plutôt que d'utiliser RECHERCHEX | Cliquer sur une cellule G des lignes P777 : la barre de formule doit afficher RECHERCHEX, pas une valeur |

---

## 5. Volet IA

L'exercice demande explicitement de valider les formules générées par une IA et de réfléchir à l'intérêt de SIERREUR dans un rapport.

**Ce qu'on attend dans la copie :**
- Une formule B7 qui produit des messages différents selon que l'erreur est `#N/A` ou `#DIV/0!`. Une copie conforme montrera `"Code introuvable"` pour P777 et `"Taux incalculable (prix de vente nul)"` pour P105.
- Une phrase argumentée sur l'intérêt de SIERREUR — et non une simple paraphrase de l'énoncé. La réponse attendue distingue l'usage en bout de chaîne (protéger le lecteur final) de l'usage en amont (qui masque les anomalies).

**Ce qui distingue l'apprenant qui a compris de celui qui a recopié :** si l'IA a proposé deux SIERREUR imbriqués, la copie d'un apprenant qui n'a pas testé affichera `"Taux incalculable"` pour P777 au lieu de `"Code introuvable"`. C'est l'erreur la plus fréquente produite par les IA génératives sur ce type de question, et elle est facilement détectable en soutenance.

**Question de vérification orale :** « Saisissez P777 en B3 de l'onglet Recherche. Quel message apparaît en B7 ? Maintenant saisissez P105. Le message est-il différent ? Pourquoi doit-il l'être, et quelle fonction avez-vous utilisée pour obtenir ce résultat ? »

Un apprenant qui a utilisé deux SIERREUR sans SI.NON.DISP verra le même message dans les deux cas et ne pourra pas expliquer la distinction.

---

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Colonne G — SIERREUR sur RECHERCHEX, message "Code introuvable" | 3 | Les 9 lignes orphelines affichent la chaîne "Code introuvable" ; les 111 autres affichent un nombre |
| Colonne H — marge unitaire correcte avec SIERREUR sur la division | 3 | Formule visible dans la barre de formule ; 7 lignes à quantité nulle affichent "Données manquantes" |
| Colonne I — taux d'atteinte de l'objectif avec SIERREUR | 2 | 6 lignes à objectif nul affichent "Données manquantes" ; les autres affichent un pourcentage |
| B5 — désignation correcte pour les 3 codes de test | 2 | P003 → Écran 27 pouces Lumen ; P105 → Étagère modulaire Strate ; P777 → "Code introuvable" |
| B6 — prix de vente pour les 3 codes | 2 | P003 → 329,00 € ; P105 → 0,00 € (ou "Code introuvable" accepté si SIERREUR intercepte) ; P777 → "Code introuvable" |
| B7 — taux de marge discriminant (SI.NON.DISP + SIERREUR) | 4 | P003 → 34,95 % ; P105 → message prix nul ; P777 → message "Code introuvable" — les deux messages sont différents |
| Argumentation sur SIERREUR en rapport (exercice 3, question 1) | 2 | La copie distingue l'usage en affichage final de l'usage en amont ; au moins une phrase sur le risque de masquage |
| Qualité et lisibilité des formules | 2 | Pas de valeurs saisies à la main, formules paramétriques sur les tableaux structurés, pas de référence absolue figée inutile |
| **Total** | **20** | |

---

## 7. Prolongements

Ajouter une mise en forme conditionnelle sur les colonnes G, H et I de l'onglet `Saisies` pour colorier en orange toute cellule contenant du texte (règle `=ESTTEXTE(G2)`) : le fichier devient auto-signalant sans modifier les formules.

Remplacer le message texte `"Code introuvable"` par `NA()` dans la colonne G, puis calculer le nombre de lignes en erreur avec `=NB.SI(Saisies[Prix_Vente_Catalogue (à compléter)]; NA())` : cette variante conserve la propagation des erreurs pour un audit ultérieur tout en les rendant comptables.

Créer un deuxième onglet `Contrôle` qui affiche, via SOMME.SI.ENS et NB.SI.ENS, les totaux de CA réalisé par code produit en excluant les lignes en texte d'erreur : c'est une introduction au concept de tableau de bord de qualité de données.
