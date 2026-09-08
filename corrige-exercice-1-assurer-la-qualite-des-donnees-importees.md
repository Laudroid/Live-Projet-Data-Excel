# Corrigé — Nettoyage et Normalisation de Données sous Excel

**Fichier(s) de données :** `ventes_brutes.csv` (422 lignes de données dont 2 lignes entièrement vides, 14 colonnes)

---

## 1. Ce que l'exercice évalue réellement

L'exercice mesure la capacité à identifier et traiter trois familles d'anomalies dans un export système réel : encodage, hétérogénéité des formats et valeurs non exploitables. Le piège le plus discriminant est la colonne `Montant` : un espace insécable (U+00A0) est visuellement identique à un espace ordinaire mais n'est pas ciblé par `SUBSTITUE(A1;" ";"")`, ce qui rend invisible l'erreur à l'apprenant non averti. L'exercice teste également le sens critique sur le choix entre suppression et imputation des valeurs manquantes.

---

## 2. Corrigé pas à pas

### Étape 1 — Diagnostic et nettoyage de l'encodage

**Mécanisme du mojibake.** Le fichier est encodé en UTF-8 sans BOM (Byte Order Mark). Sous Windows, Excel français applique par défaut l'encodage Windows-1252 à tout CSV ouvert par double-clic. Or les octets UTF-8 qui représentent un caractère accentué (par exemple, « é » = 0xC3 0xA9) sont décodés séparément en Windows-1252, ce qui produit deux caractères parasites : « Ã » et « © ». Ce phénomène — le mojibake — est systématique et reproductible : il se corrige uniquement en forçant la lecture en UTF-8.

**Manipulation correcte.**

**Données** > **Obtenir des données** > **À partir d'un fichier** > **À partir d'un fichier texte/CSV** > sélectionner `ventes_brutes.csv`.

Dans la fenêtre de prévisualisation :

- **Origine du fichier :** sélectionner `65001 : Unicode (UTF-8)`. L'aperçu doit immédiatement afficher « Léa », « Étienne », « Île-de-France » correctement.
- **Délimiteur :** vérifier que `Point-virgule` est sélectionné (le fichier utilise `;`, non la virgule).

Cliquer sur **Transformer les données**.

**Contrôle immédiat.** Si la colonne `Client` ou `Categorie` contient encore des séquences comme « Ã© », l'origine du fichier n'est pas correctement réglée.

### Étape 2 — Normalisation des formats

#### 2a. Dates — harmonisation des trois formats

La colonne `Date_Vente` contient trois formats textuels distincts sur les 420 lignes exploitables :

| Format | Exemple | Nb de lignes |
|---|---|---|
| `JJ/MM/AAAA` | `04/01/2023` | 257 |
| `AAAA.MM.JJ` | `2023.01.09` | 108 |
| `J-mmm-AA` | `14-janv-23` | 55 |

**Solution recommandée : Power Query (M).**

Dans l'éditeur Power Query, remplacer l'étape de détection automatique du type sur `Date_Vente` par une colonne personnalisée :

```m
let
    ParseDate = (t as text) as nullable date =>
        if Text.Contains(t, "/") then
            try Date.FromText(t, [Format="dd/MM/yyyy", Culture="fr-FR"])
            otherwise null
        else if Text.Contains(t, ".") then
            try Date.FromText(t, [Format="yyyy.MM.dd"])
            otherwise null
        else
            try Date.FromText(t, [Format="d-MMM-yy", Culture="fr-FR"])
            otherwise null,
    Resultat = Table.TransformColumns(
        Source,
        {{"Date_Vente", ParseDate, type nullable date}}
    )
in
    Resultat
```

La branche `d-MMM-yy` avec la culture `fr-FR` fonctionne si les abréviations de mois du fichier (« janv », « févr », sans point final) correspondent aux formes reconnues par .NET. En cas d'échec partiel, identifier les lignes converties en `null` par un filtre sur `Date_Vente = null`, puis traiter par une table de correspondance explicite.

**Solution par formule (alternative acceptable, mais incomplète).**

Dans une colonne auxiliaire `Date_calculee` sur la feuille Excel, après chargement brut :

```excel
=SI(ESTNUM(CHERCHE("/";[@Date_Vente]));
    DATEVAL([@Date_Vente]);
    SI(ESTNUM(CHERCHE(".";[@Date_Vente]));
        DATE(GAUCHE([@Date_Vente];4);STXT([@Date_Vente];6;2);DROITE([@Date_Vente];2));
        "Non traité"))
```

- `DATEVAL` (DATEVALUE) convertit `JJ/MM/AAAA` en numéro de série Excel sur une configuration régionale fr-FR.
- `DATE` + `GAUCHE` (LEFT) + `STXT` (MID) + `DROITE` (RIGHT) reconstruit une date depuis `AAAA.MM.JJ`.
- **Le format `J-mmm-AA` n'est pas traitable de façon fiable par `DATEVAL`.** La fonction interprète les abréviations de mois selon la locale du système, et une année à deux chiffres (`23`) peut être rattachée à 1923 ou 2023 selon la configuration. La valeur « Non traité » ci-dessus est intentionnelle : ne pas proposer une formule qui échoue silencieusement. La solution Power Query est la seule garantie sur l'ensemble des 55 lignes concernées.

**Détection des dates aberrantes.** Après conversion, trois dates tombent hors de la plage normale 2023 :

```excel
=NB.SI.ENS(Ventes[Date_Vente];">"&DATE(2025;12;31))
```

Résultat attendu : **3** (les valeurs `12/05/2035`, `2041.11.03` et `7-févr-38`). Ces trois lignes portent les identifiants figurant dans le fichier `valeurs-de-reference.md`. Elles ne doivent pas être supprimées sans décision explicite, mais écartées du calcul ou signalées.

#### 2b. Montant — suppression des caractères bloquants et conversion

La colonne `Montant` cumule trois problèmes :

**Problème 1 : espace insécable U+00A0 comme séparateur de milliers.**
Sur 22 lignes, le montant est formaté avec un espace insécable entre le groupe de milliers et le reste (ex. : `1 253,00` où l'espace est U+00A0). Cet espace est invisible à l'œil nu et est ignoré par `SUBSTITUE(A1;" ";"")` car cette formule cible U+0020 (espace ordinaire), pas U+00A0. Il faut viser explicitement le caractère 160 :

```excel
=SUBSTITUE([@Montant];CAR(160);"")
```

`CAR` (CHAR) renvoie le caractère correspondant au code Unicode/ASCII spécifié. `CAR(160)` produit l'espace insécable U+00A0.

**Problème 2 : point décimal au lieu de virgule.**
Sur 59 lignes, le séparateur décimal est un point anglophone (`239.60`). En Excel français, `CNUM` (VALUE) et les opérations numériques attendent une virgule. Après suppression de l'espace insécable, remplacer le point par une virgule :

```excel
=SUBSTITUE(SUBSTITUE([@Montant];CAR(160);"");".";"," )
```

**Formule complète de normalisation du Montant (colonne auxiliaire).**

```excel
=SIERREUR(
    CNUM(SUBSTITUE(SUBSTITUE([@Montant];CAR(160);"");".";"," ));
    "")
```

- `SIERREUR` (IFERROR) intercepte les cas où la cellule est vide ou contient un texte non convertible.
- Le résultat est vide (`""`) pour les 11 cellules non exploitables ; on les traite à l'étape 3.
- Cette formule suppose que le point est toujours un séparateur décimal dans ce fichier, jamais un séparateur de milliers — hypothèse confirmée par la structure du générateur.

**Solution Power Query équivalente (recommandée pour l'automatisation) :**

```m
= Table.AddColumn(
    Source,
    "Montant_num",
    each
        let
            brut      = Text.Trim([Montant]),
            sans_nbsp = Text.Replace(brut, Character.FromNumber(160), ""),
            virgule   = Text.Replace(sans_nbsp, ".", ",")
        in
            if brut = "" or brut = null then null
            else try Number.FromText(virgule, "fr-FR") otherwise null,
    type nullable number
)
```

**Problème 3 : cellules vides et textuelles.** Traité à l'étape 3.

#### 2c. Texte — nettoyage de la colonne `Client`

83 libellés comportent des espaces parasites en début, en fin ou des doubles espaces internes (ex. : `  Étienne Quintin `, `Karim Lambert   `).

**Solution formule :**

```excel
=SUPPRESPACE([@Client])
```

`SUPPRESPACE` (TRIM) supprime les espaces de début et de fin, et réduit les espaces internes multiples à un seul espace. Elle ne modifie pas les espaces insécables éventuels dans les noms, mais la colonne `Client` n'en contient pas dans ce fichier.

**Solution Power Query :** clic droit sur la colonne `Client` > **Transformer** > **Supprimer les espaces**. Cette opération équivaut à `Text.Trim` + `Text.Combine(Text.Split(...))` dans M.

### Étape 3 — Détection et traitement des erreurs

**Identification des lignes problématiques.**

Après normalisation de `Montant` en nombre (étape 2b), les cellules non converties sont vides ou en erreur. On compte 11 lignes au total : 6 montants vides et 5 montants textuels (`à valider`, `N/A`, `erreur import`, `-`, `NON COMMUNIQUE`).

Formule de détection dans une colonne `Statut_Montant` :

```excel
=SI([@Montant]="";"Vide";
    SI(ESTERREUR(CNUM([@Montant]));"Textuel";"OK"))
```

Mise en forme conditionnelle sur la colonne `Montant_num` :

**Accueil** > **Mise en forme conditionnelle** > **Nouvelle règle** > **Mettre en forme les cellules qui contiennent** > **Valeur de la cellule** > **Égale à** > laisser vide (pour les cellules vides). Couleur de fond : orange.

Pour les erreurs `#VALEUR!` (si `CNUM` a été appliqué sans `SIERREUR`) : **Mise en forme conditionnelle** > **Nouvelle règle** > **Utiliser une formule** > `=ESTERREUR(B2)`.

**Choix entre suppression et imputation par la médiane.**

Les 11 lignes problématiques représentent 11/420 = 2,6 % du dataset.

- **Suppression** : acceptable si les lignes n'apportent aucune autre information utile. Avantage : dataset propre, sans valeur imputée. Inconvénient : perte de 11 transactions (identifiant, date, client, produit restent exploitables même sans Montant).
- **Imputation par la médiane** : remplacer les montants manquants par le montant médian de l'ensemble, soit **387,00 €**. Avantage : conservation des lignes pour les analyses non monétaires (comptage de ventes, distribution catégorielle). Inconvénient : la médiane est une valeur centrale qui ne reflète pas le montant réel de ces transactions.

La décision dépend de l'usage : pour un calcul de CA, l'imputation est trompeuse ; pour un comptage de ventes par client ou par produit, conserver les lignes avec montant imputé est justifiable. **Il n'y a pas de réponse unique** : l'apprenant doit argumenter son choix.

Formule d'imputation conditionnelle (si l'apprenant choisit de garder les 11 lignes) :

```excel
=SI(OUESTVIDE([@Montant_num]);MEDIANE(Ventes[Montant_num]);[@Montant_num])
```

`MEDIANE` (MEDIAN) ignore les cellules vides dans son calcul, ce qui donne **387,00 €** sur les 409 valeurs exploitables.

---

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Lignes exploitables après suppression des lignes vides | 420 |
| Montants vides | 6 |
| Montants textuels | 5 |
| Montants avec espace insécable | 22 |
| Montants à point décimal | 59 |
| Lignes à montant exploitable | 409 |
| CA total (409 lignes) | 188 322,80 € |
| Montant médian (pour imputation) | 387,00 € |
| Montant moyen | 460,45 € |
| Libellés `Client` à nettoyer | 83 |
| Dates aberrantes (année > 2025) | 3 |
| `ID_Client` manquants | 5 |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| `Montant` reste textuel après `SUBSTITUE(A1;" ";"")` | L'espace ciblé est U+0020, pas U+00A0 | `=CODE(STXT(C4;2;1))` sur une cellule à 4 chiffres : renvoie 160 si l'espace est insécable, 32 sinon |
| `CNUM` renvoie `#VALEUR!` sur des montants apparemment corrects | Espace insécable encore présent après SUBSTITUE insuffisant | Insérer `=CAR(160)` dans une cellule, puis chercher ce caractère avec Ctrl+H |
| `DATEVAL` renvoie `#VALEUR!` sur les dates `J-mmm-AA` | Format non reconnu par la locale ou ambiguïté de l'année à 2 chiffres | Filtrer `Date_Vente` contenant `-` : toutes les cellules en erreur sont du format `J-mmm-AA` |
| CA total erroné après nettoyage | Montants avec point décimal non remplacés par une virgule | `=SOMME(Ventes[Montant_num])` doit donner 188 322,80 € ; un écart signale des lignes encore en texte |
| Encodage toujours incorrect malgré la sélection de 65001 | L'apprenant a modifié le paramètre après avoir déjà ajouté des étapes, qui ont figé les valeurs | Supprimer toutes les étapes et recommencer l'import depuis le début |
| Médiane calculée sur 420 lignes au lieu de 409 | `MEDIANE` appliquée avant nettoyage, incluant les 11 valeurs à 0 | Vérifier que la plage exclut les cellules vides : `MEDIANE` les ignore automatiquement, mais vérifier si des 0 ont été saisis à la place des vides |
| Lignes vides encore présentes | Oubli de l'étape **Supprimer les lignes vides** dans Power Query | Compter les lignes : 422 au lieu de 420 est le signal |

---

## 5. Volet IA

L'énoncé demande d'utiliser l'IA pour générer les formules complexes ou les scripts Power Query. On attend dans la copie :

- Un prompt contenant un extrait de données réel (au moins 3 lignes du CSV, y compris une avec espace insécable et une avec format `J-mmm-AA`), la version d'Excel, et le résultat souhaité.
- Une note sur ce qui a fonctionné ou échoué dans la suggestion de l'IA : par exemple, l'IA propose-t-elle `SUBSTITUE(A1;" ";"")` (insuffisant) ou `SUBSTITUE(A1;CAR(160);"")` (correct) ?
- La note de 3 lignes sur la méthode de correction des dates, demandée dans le livrable.

**Comment distinguer la compréhension de la recopie.** L'apprenant qui comprend peut expliquer pourquoi la médiane (387,00 €) est préférable à la moyenne (460,45 €) pour l'imputation : la moyenne est sensible aux valeurs extrêmes (montants élevés), la médiane est robuste. Un apprenant qui recopie ne fait pas cette distinction.

**Question de vérification orale.** « Votre formule utilise `SUBSTITUE(A1;CAR(160);"")`. Si ce caractère avait été U+202F (espace fine insécable) au lieu de U+00A0, qu'auriez-vous changé, et comment l'auriez-vous détecté ? »

---

## 7. Prolongements

Automatiser la détection des anomalies avec une colonne `Qualite` calculant pour chaque ligne un score de complétude (0 à 4 selon le nombre de champs renseignés parmi `ID_Client`, `Montant`, `Date_Vente`, `Produit`), afin de prioriser les lignes à traiter manuellement.

Construire un rapport de qualité synthétique dans une feuille dédiée : une ligne par type d'anomalie, avec le nombre de lignes concernées et le pourcentage du dataset — modèle directement réutilisable sur un autre export du même système.

Explorer la piste Power Query avancée : fusionner une table de correspondance mois → numéro (janv → 1, févr → 2, …) pour rendre la conversion `J-mmm-AA` robuste même si les abréviations changent d'un export à l'autre.
