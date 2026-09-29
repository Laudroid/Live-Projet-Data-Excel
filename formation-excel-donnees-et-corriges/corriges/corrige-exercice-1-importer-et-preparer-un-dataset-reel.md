# Corrigé — Importation et Exploration de Données avec Excel

**Fichier(s) de données :** `ventes_brutes.csv` (422 lignes de données dont 2 lignes entièrement vides, 14 colonnes)
**Durée indicative :** 45 min
**Prérequis :** Savoir naviguer dans le ruban Excel ; avoir déjà ouvert l'éditeur Power Query au moins une fois.

---

## 1. Ce que l'exercice évalue réellement

L'exercice teste la capacité à importer un CSV réel sans en altérer le contenu, en comprenant pourquoi le double-clic sur le fichier produit des caractères illisibles. Le piège central est double : l'encodage UTF-8 sans BOM interprété en Windows-1252, et la colonne `Montant` dont les espaces insécables et les décimales mixtes empêchent toute reconnaissance automatique comme nombre. L'exploration structurelle en étape 3 permet de mesurer si l'apprenant a réellement nettoyé les données ou s'il a simplement cliqué sur « Fermer et charger ».

---

## 2. Corrigé pas à pas

### Étape 1 — Importation des données

**Pourquoi le double-clic échoue.** Lorsqu'Excel ouvre un fichier CSV par double-clic, il applique l'encodage Windows-1252 (page de code 1252, encodage historique Windows pour l'Europe occidentale). Le fichier `ventes_brutes.csv` est écrit en UTF-8 sans BOM (Byte Order Mark). Sans BOM, Excel n'a aucun signal lui indiquant l'encodage réel et bascule vers son défaut régional. Les octets UTF-8 représentant les caractères accentués (é = 0xC3 0xA9 en UTF-8) sont alors décodés deux à deux comme des caractères Windows-1252 distincts, ce qui produit des séquences illisibles : « é » devient « Ã© », « à » devient « Ã  », etc. On appelle ce phénomène le mojibake.

**Manipulation correcte.**

**Données** > **Obtenir des données** > **À partir d'un fichier** > **À partir d'un fichier texte/CSV** > sélectionner `ventes_brutes.csv`.

Dans la fenêtre de prévisualisation Power Query :

- **Origine du fichier :** choisir `65001 : Unicode (UTF-8)`. C'est ce paramètre qui force la lecture en UTF-8 et corrige le mojibake.
- **Délimiteur :** vérifier que `Point-virgule` est détecté (le fichier utilise `;` comme séparateur, non la virgule).
- **Détection du type de données :** laisser sur « En fonction des 200 premières lignes » pour l'instant.

Cliquer sur **Transformer les données** pour ouvrir l'éditeur Power Query avant de charger.

### Étape 2 — Nettoyage et typage (Power Query)

**2a. Suppression des lignes vides.**

Le fichier contient 2 lignes entièrement vides (aux positions 138 et 299 dans la numérotation originale). Dans le ruban Power Query : **Accueil** > **Supprimer les lignes** > **Supprimer les lignes vides**. Résultat : 420 lignes exploitables.

**2b. Vérification des types de colonnes.**

Cliquer sur l'icône de type à gauche de chaque en-tête :

| Colonne | Type attendu | Remarque |
|---|---|---|
| `ID_Vente` | Texte | Identifiant alphanumérique |
| `Date_Vente` | Texte pour l'instant | Trois formats coexistent — voir 2c |
| `ID_Client` | Texte | Peut être vide |
| `Client` | Texte | Espaces parasites — voir 2d |
| `ID_Produit` | Texte | |
| `Produit` | Texte | |
| `Categorie` | Texte | |
| `Quantite` | Nombre entier | |
| `Montant` | Texte pour l'instant | Caractères spéciaux — voir 2e |
| `ID_Magasin` à `Vendeur` | Texte | |

**2c. Typage de la colonne `Date_Vente`.**

Trois formats coexistent dans la même colonne :

- `JJ/MM/AAAA` (ex. `04/01/2023`) — 257 lignes
- `AAAA.MM.JJ` (ex. `2023.01.09`) — 108 lignes
- `J-mmm-AA` (ex. `14-janv-23`) — 55 lignes

**Solution recommandée : colonne personnalisée en M.**

Dans **Accueil** > **Éditeur avancé**, ajouter une étape après la suppression des lignes vides :

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
    Etape = Table.TransformColumns(
        #"Lignes vides supprimées",
        {{"Date_Vente", ParseDate, type nullable date}}
    )
in
    Etape
```

**Avertissement sur le format `J-mmm-AA`.** La branche `d-MMM-yy` avec la culture `fr-FR` dépend des abréviations de mois reconnues par la bibliothèque .NET embarquée dans Power Query. Si des valeurs restent à `null` après conversion, vérifier dans un filtre : les abréviations du fichier (« janv », « févr », sans point final) peuvent différer de celles attendues par `fr-FR`. En dernier recours, ajouter un remplacement `Text.Replace(t, "-", " ")` et une table de correspondance mois → numéro avant d'appeler `Date.FromText`.

**Solution par formule (alternative, moins robuste).** À utiliser uniquement si la colonne est déjà chargée en texte dans Excel, dans une colonne auxiliaire :

```excel
=SI(ESTNUM(CHERCHE("/";A2));
    DATEVAL(A2);
    SI(ESTNUM(CHERCHE(".",A2));
        DATE(GAUCHE(A2;4);STXT(A2;6;2);DROITE(A2;2));
        "Voir note"))
```

- `DATEVAL` (DATEVALUE) reconnaît `JJ/MM/AAAA` sur Excel configuré en fr-FR.
- `DATE` + `GAUCHE` + `STXT` + `DROITE` reconstruit une date depuis `AAAA.MM.JJ`.
- Le format `J-mmm-AA` n'est pas traitable de façon fiable par `DATEVAL` sur toutes les configurations régionales : la présence d'une abréviation de mois en texte et d'une année à deux chiffres rend la formule fragile. La solution Power Query est préférable pour ce format.

**2d. Nettoyage de `Client` dans Power Query.**

Clic droit sur la colonne `Client` > **Transformer** > **Supprimer les espaces**. Cette opération supprime les espaces de début, de fin et réduit les espaces internes multiples. 83 libellés sont concernés.

**2e. Conversion de `Montant` en nombre.**

La colonne `Montant` présente trois obstacles cumulables :

1. Espace insécable (U+00A0, `CAR(160)` en formule Excel) utilisé comme séparateur de milliers sur 22 lignes — invisible dans la cellule, bloquant pour toute conversion numérique.
2. Point décimal anglophone sur 59 lignes (`239.60` au lieu de `239,60`).
3. 6 cellules vides et 5 cellules textuelles (valeurs : `à valider`, `N/A`, `erreur import`, `-`, `NON COMMUNIQUE`).

**Solution Power Query (recommandée).**

Ajouter une colonne personnalisée avant de changer le type :

```m
= Table.AddColumn(
    Source,
    "Montant_num",
    each
        let
            brut   = Text.Trim([Montant]),
            sans_nbsp = Text.Replace(brut, Character.FromNumber(160), ""),
            virgule   = Text.Replace(sans_nbsp, ".", ",")
        in
            if brut = "" or brut = null then null
            else try Number.FromText(virgule, "fr-FR") otherwise null,
    type nullable number
)
```

Supprimer ensuite l'ancienne colonne `Montant` et renommer `Montant_num`.

**2f. Chargement.**

**Fermer et charger dans…** > choisir **Tableau** dans la feuille existante. Nommer le tableau structuré `Ventes`. Le résultat attendu est un tableau de 420 lignes × 14 colonnes.

### Étape 3 — Exploration structurelle

**Volume.** La feuille Données doit afficher 420 lignes (2 lignes vides retirées en Power Query) et 14 colonnes : `ID_Vente`, `Date_Vente`, `ID_Client`, `Client`, `ID_Produit`, `Produit`, `Categorie`, `Quantite`, `Montant`, `ID_Magasin`, `Magasin`, `Ville`, `Region`, `Vendeur`.

Formule de contrôle en feuille Exploration :

```excel
=LIGNES(Ventes[ID_Vente])
```

Résultat attendu : **420**.

**Intégrité.** Deux colonnes clés à vérifier :

```excel
=NB.SI(Ventes[ID_Client];"")
```

Résultat attendu : **5** (ID_Client manquants).

```excel
=NBVAL(Ventes[Montant])-NB(Ventes[Montant])
```

Résultat attendu : **11** (6 vides + 5 textuels ; si la conversion en nombre a été faite, cette formule compte les cellules non numériques, c'est-à-dire les `null` issus des deux types d'anomalies).

La mise en forme conditionnelle sur `ID_Client` : **Accueil** > **Mise en forme conditionnelle** > **Règles de mise en surbrillance des cellules** > **Égal à** > laisser vide.

**Distribution.** Créer un TCD depuis le tableau `Ventes` : lignes = `Categorie`, valeurs = `NB de ID_Vente`. Les valeurs ci-dessous correspondent aux lignes dont le Montant est exploitable (après typage) :

| Catégorie | Nb de ventes | CA |
|---|---|---|
| Électroménager | 72 | 47 926,70 € |
| Électronique | 88 | 47 325,40 € |
| Téléphonie | 86 | 37 663,60 € |
| Mobilier | 44 | 32 200,00 € |
| Papeterie | 119 | 23 207,10 € |

Si la colonne `Montant` n'a pas encore été convertie en nombre, le TCD affiche des comptes légèrement supérieurs (jusqu'à 120 pour Papeterie) car les lignes à Montant textuel sont comptées.

**Cohérence des dates.** Trois dates sont situées dans le futur lointain : `12/05/2035`, `2041.11.03`, `7-févr-38`. La plage normale est du 04/01/2023 au 31/12/2023. Après chargement des dates au format Date, un filtre sur `Date_Vente` > **Filtres de dates** > **Après** > `31/12/2023` les révèle. Ou en formule :

```excel
=NB.SI.ENS(Ventes[Date_Vente];">"&DATE(2025;12;31))
```

Résultat attendu : **3**.

---

## 3. Valeurs de contrôle

| Indicateur | Valeur attendue |
|---|---|
| Lignes de données brutes (y compris lignes vides) | 422 |
| Lignes exploitables après suppression des lignes vides | 420 |
| Colonnes | 14 |
| `ID_Client` manquants | 5 |
| Montants vides | 6 |
| Montants textuels | 5 |
| Lignes à montant exploitable | 409 |
| CA total (409 lignes) | 188 322,80 € |
| Montant médian | 387,00 € |
| Dates aberrantes (année > 2025) | 3 |
| Plage de dates normale | 04/01/2023 au 31/12/2023 |

---

## 4. Erreurs fréquentes

| Symptôme dans la copie | Cause | Comment le vérifier en 10 secondes |
|---|---|---|
| Accents illisibles (« Ã© » à la place de « é ») | Fichier ouvert par double-clic ou encodage non réglé à 65001 dans Power Query | Vérifier la colonne `Client` : « Léa » doit s'afficher correctement |
| 422 lignes au lieu de 420 | Lignes vides non supprimées en Power Query | Filtrer sur `ID_Vente` = vide : 2 résultats |
| Montant affiché comme texte aligné à gauche | Espace insécable non retiré, ou type non modifié | `=ESTERREUR(CNUM(C2))` renvoie VRAI sur une cellule Montant textuelle |
| DATEVAL retourne #VALEUR! sur certaines dates | Format `J-mmm-AA` non reconnu | Filtrer `Date_Vente` : identifier les cellules en erreur après conversion |
| TCD des catégories affiche 422 ou 420 ventes au total | Montant non converti → les 11 lignes problématiques sont comptées | Sommer la colonne `Montant` dans le TCD : si elle affiche 0 ou erreur, la conversion n'est pas faite |
| 3 aberrantes non détectées | Dates non converties en type Date, filtre sur texte impossible | Changer le type de `Date_Vente` en Date, puis filtrer `> 31/12/2025` |
| Délimiteur détecté comme virgule | Power Query a parfois du mal avec les CSV régionaux | Vérifier dans l'aperçu : si toutes les colonnes s'affichent en une seule, changer le délimiteur en Point-virgule |

---

## 5. Volet IA

L'énoncé encourage l'utilisation de l'IA pour les formules complexes ou les scripts Power Query. On attend dans la copie :

- Un prompt comportant un exemple de ligne du fichier (encodage, format de date ou de montant), la version d'Excel utilisée et le résultat souhaité.
- Une vérification explicite du résultat : l'apprenant doit noter si la formule ou le code M proposé a fonctionné sans modification ou s'il a dû l'adapter.
- Un commentaire de cellule ou une note dans la feuille Exploration expliquant la logique de la formule.

**Comment distinguer la compréhension de la recopie.** Un apprenant qui a compris peut expliquer pourquoi `SUBSTITUE(A1;" ";"")` ne suffit pas pour retirer l'espace insécable (la touche espace produit U+0020, pas U+00A0). Un apprenant qui a recopié sans comprendre proposera souvent cette formule insuffisante.

**Question de vérification orale.** « Vous avez utilisé `CAR(160)` dans votre formule. Qu'est-ce que ce nombre représente, et comment auriez-vous trouvé ce code si l'IA ne vous l'avait pas donné ? »

---

## 6. Barème indicatif

| Critère | Points | Observable |
|---|---|---|
| Import via Power Query avec encodage 65001 | 3 | La colonne `Client` affiche les accents correctement |
| Délimiteur point-virgule correctement détecté | 1 | 14 colonnes distinctes dans le tableau chargé |
| Lignes vides supprimées | 1 | Tableau de 420 lignes exactement |
| Colonne `Date_Vente` convertie en type Date | 3 | Cellules alignées à droite ; filtre de dates disponible |
| Dates aberrantes identifiées (3) | 2 | Cellule dans la feuille Exploration avec le résultat 3 |
| Colonne `Montant` convertie en nombre | 3 | Somme du TCD = 188 322,80 € |
| Valeurs manquantes `ID_Client` signalées (5) | 1 | Formule ou mise en forme conditionnelle visible |
| TCD de distribution par catégorie correct | 3 | Valeurs conformes au tableau de la section 3 |
| Note sur l'utilisation de l'IA (prompt + vérification) | 3 | Commentaire ou cellule explicative présent dans le fichier |
| **Total** | **20** | |

---

## 7. Prolongements

Ajouter un segment sur le TCD de distribution pour filtrer par région et observer si la répartition des catégories varie selon la région de vente.

Créer une colonne calculée `Mois_Vente` avec `=TEXTE([@Date_Vente];"mmm-aaaa")` et construire un TCD mensuel pour visualiser l'évolution du CA sur l'année 2023.

Connecter le fichier à une source actualisable (SharePoint ou dossier réseau) pour que le tableau se mette à jour automatiquement à chaque actualisation Power Query, sans réimporter manuellement.
