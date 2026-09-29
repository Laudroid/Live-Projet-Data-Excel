# -*- coding: utf-8 -*-
"""Controle des jeux de donnees et calcul des valeurs de reference.

Ce script fait deux choses :
  1. il verifie que chaque anomalie annoncee est bien presente dans le
     fichier livre, et que les filtres des enonces renvoient des
     resultats non vides ;
  2. il calcule toutes les valeurs numeriques attendues, exercice par
     exercice, et les ecrit dans corriges/valeurs-de-reference.md.

Usage : python3 verifier_donnees.py
"""

import datetime as dt
import io
import os
import re
import unicodedata

import pandas as pd

DONNEES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "donnees")
CORRIGES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "corriges")

MOIS_FR_COURT = {"janv": 1, "févr": 2, "mars": 3, "avr": 4, "mai": 5,
                 "juin": 6, "juil": 7, "août": 8, "sept": 9, "oct": 10,
                 "nov": 11, "déc": 12}

sortie = []
alertes = []


def titre(niveau, texte):
    sortie.append("\n%s %s\n" % ("#" * niveau, texte))


def ligne(texte=""):
    sortie.append(texte)


def tableau(entetes, lignes):
    sortie.append("| " + " | ".join(entetes) + " |")
    sortie.append("|" + "|".join(["---"] * len(entetes)) + "|")
    for l in lignes:
        sortie.append("| " + " | ".join(str(v) for v in l) + " |")
    sortie.append("")


def eur(valeur):
    return ("%0.2f" % valeur).replace(".", ",").replace(" ", " ")


def eur_espace(valeur):
    entier, dec = ("%0.2f" % valeur).split(".")
    groupes = []
    while len(entier) > 3:
        groupes.insert(0, entier[-3:])
        entier = entier[:-3]
    groupes.insert(0, entier)
    return "%s,%s" % (" ".join(groupes), dec)


def verifier(condition, message):
    if condition:
        print("  OK   %s" % message)
    else:
        print("  KO   %s" % message)
        alertes.append(message)


def parser_date_mixte(valeur):
    valeur = (valeur or "").strip()
    if not valeur:
        return None
    m = re.match(r"^(\d{2})/(\d{2})/(\d{4})$", valeur)
    if m:
        return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    m = re.match(r"^(\d{4})\.(\d{2})\.(\d{2})$", valeur)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"^(\d{1,2})-([^-]+)-(\d{2})$", valeur)
    if m and m.group(2) in MOIS_FR_COURT:
        annee = int(m.group(3))
        annee += 2000 if annee < 70 else 1900
        return dt.date(annee, MOIS_FR_COURT[m.group(2)], int(m.group(1)))
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})$", valeur)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return "INVALIDE"


def parser_montant(valeur):
    valeur = (valeur or "").strip()
    if not valeur:
        return None
    nettoye = valeur.replace(" ", "").replace(" ", "").replace(",", ".")
    try:
        return float(nettoye)
    except ValueError:
        return "INVALIDE"


def sans_accent(t):
    d = unicodedata.normalize("NFKD", str(t))
    return "".join(c for c in d if not unicodedata.combining(c))


# =====================================================================
def bloc_ventes_brutes():
    print("\n[1] ventes_brutes.csv")
    chemin = os.path.join(DONNEES, "ventes_brutes.csv")
    brut = io.open(chemin, encoding="utf-8").read()

    verifier(not brut.startswith("﻿"),
             "aucun BOM (le mojibake sera authentique dans Excel FR)")
    verifier("Électronique" in brut, "accents presents dans les libelles")

    df = pd.read_csv(chemin, sep=";", dtype=str, keep_default_na=False)
    lignes_vides = int((df.apply(lambda r: all(v == "" for v in r),
                                 axis=1)).sum())
    verifier(lignes_vides == 2, "2 lignes entierement vides")

    plein = df[df["ID_Vente"] != ""].copy()
    plein["date_parsee"] = plein["Date_Vente"].map(parser_date_mixte)
    plein["montant_parse"] = plein["Montant"].map(parser_montant)

    fmt_slash = int(plein["Date_Vente"].str.match(r"^\d{2}/\d{2}/\d{4}$").sum())
    fmt_point = int(plein["Date_Vente"].str.match(r"^\d{4}\.\d{2}\.\d{2}$").sum())
    fmt_mois = len(plein) - fmt_slash - fmt_point
    verifier(min(fmt_slash, fmt_point, fmt_mois) > 20,
             "trois formats de date presents en nombre significatif")

    futures = plein[plein["date_parsee"].map(
        lambda d: d != "INVALIDE" and d is not None and d.year > 2025)]
    verifier(len(futures) == 3, "3 dates aberrantes dans le futur")

    montant_vide = int((plein["Montant"] == "").sum())
    montant_texte = int((plein["montant_parse"] == "INVALIDE").sum())
    verifier(montant_vide == 6, "6 montants vides")
    verifier(montant_texte == 5, "5 montants textuels")

    nbsp = int(plein["Montant"].str.contains(" ").sum())
    point = int(plein["Montant"].str.match(r"^\d+\.\d{2}$").sum())
    verifier(nbsp >= 15, "%d montants avec espace insecable" % nbsp)
    verifier(point > 30, "montants a separateur decimal anglo-saxon presents")

    espaces = int(plein["Client"].map(
        lambda v: v != v.strip() or "  " in v).sum())
    verifier(espaces > 60, "libelles clients avec espaces parasites")

    id_client_vide = int((plein["ID_Client"] == "").sum())
    verifier(id_client_vide == 5, "5 identifiants clients manquants")

    valides = plein[plein["montant_parse"].map(
        lambda v: isinstance(v, float))].copy()
    dates_ok = plein[plein["date_parsee"].map(
        lambda d: isinstance(d, dt.date) and d.year == 2023)]

    ca_total = float(valides["montant_parse"].sum())
    mediane = float(valides["montant_parse"].median())
    par_cat = valides.groupby("Categorie")["montant_parse"].agg(
        ["count", "sum"]).sort_values("sum", ascending=False)

    titre(2, "Exercices A1 et B1 — `ventes_brutes.csv`")
    ligne("Fichier livre en UTF-8 **sans BOM**, separateur `;`, "
          "%d lignes d'en-tete + %d lignes de donnees dont "
          "%d lignes entierement vides." % (1, len(df), lignes_vides))
    ligne()
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes de donnees (y compris lignes vides)", len(df)],
        ["Lignes exploitables (ID_Vente renseigne)", len(plein)],
        ["Colonnes", len(df.columns)],
        ["Lignes entierement vides", lignes_vides],
        ["Dates au format `JJ/MM/AAAA`", fmt_slash],
        ["Dates au format `AAAA.MM.JJ`", fmt_point],
        ["Dates au format `J-mmm-AA`", fmt_mois],
        ["Dates aberrantes (annee > 2025)", "%d (%s)" % (
            len(futures), ", ".join(futures["Date_Vente"].tolist()))],
        ["Montants vides", montant_vide],
        ["Montants textuels", "%d (%s)" % (montant_texte, ", ".join(
            sorted(plein[plein["montant_parse"] == "INVALIDE"]["Montant"])))],
        ["Montants avec espace insecable", nbsp],
        ["Montants a point decimal", point],
        ["Libelles `Client` a nettoyer", espaces],
        ["`ID_Client` manquants", id_client_vide],
        ["Clients distincts (hors vides)",
         plein[plein["ID_Client"] != ""]["ID_Client"].nunique()],
        ["Plage de dates plausible",
         "%s au %s" % (min(dates_ok["date_parsee"]).strftime("%d/%m/%Y"),
                       max(dates_ok["date_parsee"]).strftime("%d/%m/%Y"))],
    ])
    ligne("**Valeurs de controle apres nettoyage** (les 11 lignes a montant "
          "vide ou textuel etant exclues du calcul) :")
    ligne()
    tableau(["Indicateur", "Valeur"], [
        ["Lignes a montant exploitable", len(valides)],
        ["CA total", eur_espace(ca_total) + " €"],
        ["Montant median (pour imputation)", eur(mediane) + " €"],
        ["Montant moyen", eur(float(valides["montant_parse"].mean())) + " €"],
    ])
    ligne("Repartition par categorie (etape « distribution » de l'exercice A1) :")
    ligne()
    tableau(["Categorie", "Nb de ventes", "CA"],
            [[c, int(r["count"]), eur_espace(r["sum"]) + " €"]
             for c, r in par_cat.iterrows()])

    ids_anomalies = sorted(
        plein[(plein["Montant"] == "") |
              (plein["montant_parse"] == "INVALIDE") |
              (plein["ID_Client"] == "") |
              (plein["date_parsee"].map(
                  lambda d: isinstance(d, dt.date) and d.year > 2025))
              ]["ID_Vente"].tolist())
    ligne("Identifiants des lignes porteuses d'au moins une anomalie "
          "(hors format de date ou d'espace) : `%s`." % "`, `".join(ids_anomalies))


# =====================================================================
def bloc_clients():
    print("\n[2] clients_brut.xlsx")
    df = pd.read_excel(os.path.join(DONNEES, "clients_brut.xlsx"),
                       dtype={"Telephone": object})

    verifier(len(df) == 195, "195 lignes")
    nom_sale = int(df["Nom"].map(
        lambda v: v != v.strip() or "  " in v).sum())
    verifier(nom_sale > 60, "noms avec espaces parasites")

    df["nom_normalise"] = df["Nom"].map(
        lambda v: " ".join(str(v).split()).title())
    df["cle"] = df["nom_normalise"] + "|" + df["Email"].str.lower()

    doublons = int(df.duplicated("cle").sum())
    verifier(doublons == 15, "15 doublons apres normalisation du nom")

    doublons_bruts = int(df.duplicated(["Nom", "Email"]).sum())
    verifier(doublons_bruts < doublons,
             "les doublons masques echappent a une detection sans nettoyage "
             "(%d detectes sur les donnees brutes)" % doublons_bruts)

    tel = df["Telephone"].fillna("")
    vides = int((tel.astype(str).str.strip() == "").sum())
    non_renseigne = int((tel.astype(str) == "non renseigné").sum())
    numeriques = int(tel.map(lambda v: isinstance(v, (int, float))
                             and str(v) != "nan").sum())
    verifier(vides >= 10, "cellules Telephone vides presentes")

    villes_composees = int(df["Adresse"].map(
        lambda v: "-" in str(v).split(" ", 1)[1]).sum())
    verifier(villes_composees > 10,
             "villes composees presentes (l'extraction par DROITE echoue)")

    cp_ok = int(df["Adresse"].str.match(r"^\d{5} .+$").sum())
    verifier(cp_ok == len(df), "toutes les adresses au format 'CP Ville'")

    titre(2, "Exercice A2 — `clients_brut.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes", len(df)],
        ["Colonnes", len(df.columns) - 2],
        ["Clients reellement distincts", df["cle"].nunique()],
        ["Doublons a supprimer", doublons],
        ["dont doublons detectables sans nettoyage prealable",
         doublons_bruts],
        ["dont doublons masques par la casse ou les espaces",
         doublons - doublons_bruts],
        ["Noms a nettoyer (espaces parasites)", nom_sale],
        ["Noms en capitales integrales",
         int(df["Nom"].map(lambda v: str(v).strip().isupper()).sum())],
        ["Telephones vides", vides],
        ["Telephones a « non renseigné »", non_renseigne],
        ["Telephones numeriques (zero initial perdu)", numeriques],
        ["Adresses a ville composee (tiret)", villes_composees],
        ["Codes postaux distincts", df["Adresse"].str.slice(0, 5).nunique()],
    ])
    ligne("**Point de vigilance pedagogique.** Sur les %d doublons, seuls %d "
          "sont visibles si l'apprenant applique `Supprimer les doublons` "
          "directement sur les colonnes brutes. Les %d autres ne se "
          "revelent qu'apres `NOMPROPRE(SUPPRESPACE(...))` : c'est ce qui "
          "justifie l'ordre des etapes de l'enonce."
          % (doublons, doublons_bruts, doublons - doublons_bruts))
    ligne()
    emails_doublons = df[df.duplicated("cle", keep=False)].sort_values("cle")
    ligne("Couples en doublon (a verifier lors de la correction) :")
    ligne()
    tableau(["ID_Client", "Nom saisi", "Email"],
            [[r["ID_Client"], r["Nom"], r["Email"]]
             for _, r in emails_doublons.iterrows()])


# =====================================================================
def bloc_projet():
    print("\n[3] Ventes_Projet.xlsx")
    df = pd.read_excel(os.path.join(DONNEES, "Ventes_Projet.xlsx"))
    verifier(len(df) == 600, "600 lignes")
    verifier(pd.api.types.is_datetime64_any_dtype(df["Date_Vente"]),
             "Date_Vente est un vrai type date")
    verifier("Année" not in df.columns and "Mois" not in df.columns,
             "aucune colonne temporelle derivee (a creer par l'apprenant)")

    df["Annee"] = df["Date_Vente"].dt.year
    df["Mois"] = df["Date_Vente"].dt.month
    df["Cle"] = df["Annee"] * 100 + df["Mois"]
    par_mois = df.groupby("Cle")["Chiffre_Affaires"].sum()
    verifier(len(par_mois) == 24, "24 mois couverts")

    titre(2, "Exercice B2 — `Ventes_Projet.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes", len(df)],
        ["Colonnes fournies", len(df.columns) - 3],
        ["Tableau structure", "oui, nomme `Ventes`"],
        ["Plage", "%s au %s" % (df["Date_Vente"].min().strftime("%d/%m/%Y"),
                                df["Date_Vente"].max().strftime("%d/%m/%Y"))],
        ["Mois distincts", len(par_mois)],
        ["CA total", eur_espace(float(df["Chiffre_Affaires"].sum())) + " €"],
        ["CA 2023", eur_espace(float(
            df[df["Annee"] == 2023]["Chiffre_Affaires"].sum())) + " €"],
        ["CA 2024", eur_espace(float(
            df[df["Annee"] == 2024]["Chiffre_Affaires"].sum())) + " €"],
    ])
    croissance = (df[df["Annee"] == 2024]["Chiffre_Affaires"].sum() /
                  df[df["Annee"] == 2023]["Chiffre_Affaires"].sum() - 1)
    ligne("Croissance 2024 vs 2023 : **%s %%**."
          % eur(croissance * 100))
    ligne()
    ligne("CA par cle `Mois-Annee` (resultat attendu du TCD) :")
    ligne()
    noms = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
            "août", "sept.", "oct.", "nov.", "déc."]
    lignes_tcd = []
    for cle, valeur in par_mois.items():
        annee, mois = divmod(int(cle), 100)
        lignes_tcd.append(["%s-%d" % (noms[mois - 1], annee),
                           int(cle), eur_espace(float(valeur)) + " €"])
    tableau(["Mois-Annee (`TEXTE(...;\"mmm-aaaa\")`)",
             "Cle de tri (`ANNEE*100+MOIS`)", "CA"], lignes_tcd)
    meilleur = par_mois.idxmax()
    a, m = divmod(int(meilleur), 100)
    ligne("Mois le plus performant : **%s %d** avec %s €."
          % (noms[m - 1], a, eur_espace(float(par_mois.max()))))
    ligne()
    ligne("Ordre alphabetique trompeur : trie comme du texte, la cle "
          "`mmm-aaaa` place `avr.-2023` avant `janv.-2023`. C'est "
          "exactement le piege que la colonne d'index `ANNEE*100+MOIS` "
          "resout.")


# =====================================================================
def bloc_ventes_ref():
    print("\n[4] Ventes.xlsx + Referentiel.xlsx")
    ventes = pd.read_excel(os.path.join(DONNEES, "Ventes.xlsx"))
    produits = pd.read_excel(os.path.join(DONNEES, "Referentiel.xlsx"),
                             sheet_name="Produits")
    magasins = pd.read_excel(os.path.join(DONNEES, "Referentiel.xlsx"),
                             sheet_name="Magasins")

    verifier(list(ventes.columns) == ["Date", "ID_Produit", "Quantité",
                                      "ID_Magasin"],
             "Ventes.xlsx ne contient que les 4 colonnes de l'enonce")
    verifier(list(produits.columns) == ["ID_Produit", "Nom_Produit",
                                        "Prix_Unitaire"],
             "onglet Produits conforme a l'enonce")
    verifier(list(magasins.columns) == ["ID_Magasin", "Nom_Magasin", "Ville",
                                        "Région"],
             "onglet Magasins conforme a l'enonce")

    orphelins_p = sorted(set(ventes["ID_Produit"]) - set(produits["ID_Produit"]))
    orphelins_m = sorted(set(ventes["ID_Magasin"]) - set(magasins["ID_Magasin"]))
    nb_op = int(ventes["ID_Produit"].isin(orphelins_p).sum())
    nb_om = int(ventes["ID_Magasin"].isin(orphelins_m).sum())
    verifier(nb_op == 4, "4 lignes a produit orphelin")
    verifier(nb_om == 3, "3 lignes a magasin orphelin")

    df = ventes.merge(produits, on="ID_Produit", how="left") \
               .merge(magasins, on="ID_Magasin", how="left")
    df["CA"] = df["Quantité"] * df["Prix_Unitaire"]
    complet = df.dropna(subset=["Prix_Unitaire", "Région"])

    par_region = complet.groupby("Région")["CA"].sum().sort_values(
        ascending=False)
    nb_gt10 = complet[complet["Quantité"] > 10].groupby("Région").size()

    titre(2, "Exercice A3 — `Ventes.xlsx` + `Referentiel.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes de `Ventes.xlsx`", len(ventes)],
        ["Plage", "%s au %s" % (ventes["Date"].min().strftime("%d/%m/%Y"),
                                ventes["Date"].max().strftime("%d/%m/%Y"))],
        ["References au catalogue Produits", len(produits)],
        ["Magasins au referentiel", len(magasins)],
        ["Lignes a produit orphelin",
         "%d (codes %s)" % (nb_op, ", ".join(orphelins_p))],
        ["Lignes a magasin orphelin",
         "%d (code %s)" % (nb_om, ", ".join(orphelins_m))],
        ["Lignes en `#N/A` sur au moins une recherche", nb_op + nb_om],
        ["CA total, lignes orphelines exclues",
         eur_espace(float(complet["CA"].sum())) + " €"],
        ["CA total si les `#N/A` sont neutralises a 0",
         eur_espace(float(df["CA"].fillna(0).sum())) + " €"],
    ])
    ligne("**Partie 2, question 1** — CA par region (`SOMME.SI.ENS`) :")
    ligne()
    tableau(["Region", "CA"],
            [[r, eur_espace(float(v)) + " €"] for r, v in par_region.items()])
    ligne("**Partie 2, question 2** — nombre de transactions de plus de "
          "10 unites (`NB.SI.ENS`) :")
    ligne()
    tableau(["Region", "Nb de transactions > 10 unites"],
            [[r, int(v)] for r, v in nb_gt10.items()])
    ligne("Total sur l'ensemble des regions : **%d transactions** de plus de "
          "10 unites, sur %d lignes exploitables."
          % (int(nb_gt10.sum()), len(complet)))
    ligne()
    ligne("**Partie 2, question 3** — analyse croisee produit x region. "
          "Trois couples utilisables comme consigne de correction :")
    ligne()
    croise = complet.groupby(["Nom_Produit", "Région"])["CA"].agg(
        ["count", "sum"]).reset_index()
    croise = croise[croise["count"] >= 3].sort_values("sum", ascending=False)
    tableau(["Produit", "Region", "Nb de lignes", "CA"],
            [[r["Nom_Produit"], r["Région"], int(r["count"]),
              eur_espace(float(r["sum"])) + " €"]
             for _, r in croise.head(6).iterrows()])


# =====================================================================
def bloc_marges():
    print("\n[5] Suivi_Marges.xlsx")
    cat = pd.read_excel(os.path.join(DONNEES, "Suivi_Marges.xlsx"),
                        sheet_name="Catalogue")
    sai = pd.read_excel(os.path.join(DONNEES, "Suivi_Marges.xlsx"),
                        sheet_name="Saisies")

    inconnus = sai[~sai["Code_Produit"].isin(cat["Code_Produit"])]
    verifier(len(inconnus) == 9, "9 lignes a code produit introuvable")

    qte_nulle = sai[(sai["Quantite_Vendue"].isna()) |
                    (sai["Quantite_Vendue"] == 0)]
    verifier(len(qte_nulle) == 7, "7 quantites nulles ou vides")

    obj_nul = sai[(sai["CA_Objectif"].isna()) | (sai["CA_Objectif"] == 0)]
    verifier(len(obj_nul) == 6, "6 objectifs nuls ou vides")

    prix_zero = cat[cat["Prix_Vente"] == 0]
    verifier(len(prix_zero) == 2, "2 references a prix de vente nul")

    colonnes_vides = [c for c in sai.columns if "compléter" in c]
    verifier(all(sai[c].isna().all() for c in colonnes_vides),
             "les 3 colonnes « a completer » sont bien vides")

    p003 = cat[cat["Code_Produit"] == "P003"].iloc[0]
    taux = (p003["Prix_Vente"] - p003["Prix_Achat"]) / p003["Prix_Vente"]

    titre(2, "Exercice B3 — `Suivi_Marges.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Onglets", "`Catalogue`, `Saisies`, `Recherche`"],
        ["References au catalogue", len(cat)],
        ["Lignes de saisie", len(sai)],
        ["Colonnes a completer",
         ", ".join("`%s`" % c for c in colonnes_vides)],
        ["Lignes generant `#N/A` (code introuvable)",
         "%d (codes %s)" % (len(inconnus),
                            ", ".join(sorted(set(inconnus["Code_Produit"]))))],
        ["Lignes generant `#DIV/0!` sur la marge unitaire", len(qte_nulle)],
        ["Lignes generant `#DIV/0!` sur le taux d'atteinte", len(obj_nul)],
        ["References a prix de vente nul",
         "%d (%s)" % (len(prix_zero),
                      ", ".join(prix_zero["Code_Produit"]))],
        ["Total de cellules en erreur avant traitement",
         "%d" % (len(inconnus) + len(qte_nulle) + len(obj_nul))],
    ])
    ligne("**Onglet `Recherche`** — valeurs attendues pour les trois codes "
          "de test :")
    ligne()
    lignes_test = [
        ["`P003`", p003["Designation"], eur(float(p003["Prix_Vente"])) + " €",
         "%s %%" % eur(taux * 100), "cas nominal"],
    ]
    for code in ["P105", "P777"]:
        sous = cat[cat["Code_Produit"] == code]
        if len(sous):
            r = sous.iloc[0]
            lignes_test.append(["`%s`" % code, r["Designation"],
                                eur(float(r["Prix_Vente"])) + " €",
                                "`#DIV/0!` a intercepter",
                                "prix de vente a 0"])
        else:
            lignes_test.append(["`%s`" % code, "`#N/A` a intercepter",
                                "`#N/A` a intercepter",
                                "`#N/A` a intercepter",
                                "code absent du catalogue"])
    tableau(["Code saisi en B3", "Designation", "Prix de vente",
             "Taux de marge", "Cas teste"], lignes_test)


# =====================================================================
def bloc_globales():
    print("\n[6] Ventes_Globales.xlsx")
    df = pd.read_excel(os.path.join(DONNEES, "Ventes_Globales.xlsx"))
    verifier(len(df) == 1600, "1600 lignes")
    verifier(pd.api.types.is_datetime64_any_dtype(df["Date"]),
             "colonne Date en vrai format date (groupement par mois possible)")

    df["Mois"] = df["Date"].dt.month
    ca = "Chiffre d'affaires (CA)"

    par_region = df.groupby("Région")[ca].sum().sort_values(ascending=False)
    par_cat = df.groupby("Catégorie de produit").agg(
        CA=(ca, "sum"), Qte_moy=("Quantité vendue", "mean")).sort_values(
        "CA", ascending=False)
    par_vendeur = df.groupby("Vendeur")[ca].sum().sort_values(ascending=False)

    # saisonnalite : coefficient de variation du CA mensuel par region
    pivot = df.pivot_table(index="Région", columns="Mois", values=ca,
                           aggfunc="sum").fillna(0)
    cv = (pivot.std(axis=1) / pivot.mean(axis=1)).sort_values(ascending=False)
    verifier(float(cv.iloc[0]) - float(cv.iloc[1]) > 0.15,
             "la region la plus saisonniere (%s, %.1f %%) se detache "
             "nettement de la suivante (%s, %.1f %%)"
             % (cv.index[0], cv.iloc[0] * 100, cv.index[1],
                cv.iloc[1] * 100))

    titre(2, "Exercice A4 — `Ventes_Globales.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes", len(df)],
        ["Colonnes", len(df.columns) - 1],
        ["Forme livree", "plage simple — le `Ctrl+T` est a la charge de "
                         "l'apprenant"],
        ["Plage", "%s au %s" % (df["Date"].min().strftime("%d/%m/%Y"),
                                df["Date"].max().strftime("%d/%m/%Y"))],
        ["CA total", eur_espace(float(df[ca].sum())) + " €"],
        ["Regions", df["Région"].nunique()],
        ["Categories", df["Catégorie de produit"].nunique()],
        ["Vendeurs", df["Vendeur"].nunique()],
    ])
    ligne("**TCD 1 — saisonnalite par region.** Coefficient de variation du "
          "CA mensuel (ecart-type / moyenne, 24 mois cumules par mois "
          "calendaire) : plus il est eleve, plus la region est saisonniere.")
    ligne()
    tableau(["Region", "CA total", "Coefficient de variation mensuel"],
            [[r, eur_espace(float(par_region[r])) + " €", "%s %%" % eur(
                float(cv[r]) * 100)] for r in cv.index])
    ligne("Reponse attendue : **%s** est la region la plus saisonniere, "
          "**%s** la plus stable." % (cv.index[0], cv.index[-1]))
    ligne()
    ligne("**TCD 2 — performance par categorie**, trie decroissant sur le CA :")
    ligne()
    tableau(["Categorie", "CA", "Quantite moyenne"],
            [[c, eur_espace(float(r["CA"])) + " €",
              eur(float(r["Qte_moy"]))] for c, r in par_cat.iterrows()])
    ligne("**TCD 3 — analyse des vendeurs** (sans filtre de region ni de "
          "categorie) :")
    ligne()
    tableau(["Vendeur", "CA"],
            [[v, eur_espace(float(x)) + " €"] for v, x in par_vendeur.items()])

    pic = pivot.loc[cv.index[0]]
    mois_noms = ["janvier", "février", "mars", "avril", "mai", "juin",
                 "juillet", "août", "septembre", "octobre", "novembre",
                 "décembre"]
    ligne("Detail du profil mensuel de la region la plus saisonniere "
          "(%s), cumul des deux annees :" % cv.index[0])
    ligne()
    tableau(["Mois", "CA cumule"],
            [[mois_noms[int(m) - 1], eur_espace(float(v))+" €"]
             for m, v in pic.items()])


# =====================================================================
def bloc_query():
    print("\n[7] Data_Ventes.csv")
    chemin = os.path.join(DONNEES, "Data_Ventes.csv")
    df = pd.read_csv(chemin, encoding="utf-8-sig")
    verifier(list(df.columns) == ["Date", "Catégorie", "Produit", "Vendeur",
                                 "Montant", "Région"],
             "ordre des colonnes conforme (A..F)")
    verifier(pd.api.types.is_integer_dtype(df["Montant"]),
             "Montant en entier (import Sheets insensible a la locale)")

    ex1 = df[(df["Catégorie"] == "Électronique") & (df["Montant"] > 500) &
             (df["Région"].isin(["Nord", "Sud"]))]
    verifier(len(ex1) >= 10,
             "le filtre de l'exercice 1 renvoie %d lignes" % len(ex1))

    par_vendeur = df.groupby("Vendeur")["Montant"].sum().sort_values(
        ascending=False)
    retenus = par_vendeur[par_vendeur > 1000]
    exclus = par_vendeur[par_vendeur <= 1000]
    verifier(len(exclus) >= 1 and len(retenus) >= 5,
             "la clause HAVING > 1000 exclut %d vendeur(s) sur %d"
             % (len(exclus), len(par_vendeur)))

    titre(2, "Exercice B4 — `Data_Ventes.csv` (Google Sheets)")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes", len(df)],
        ["Colonnes", "A Date, B Catégorie, C Produit, D Vendeur, "
                     "E Montant, F Région"],
        ["Encodage", "UTF-8 avec BOM, separateur virgule"],
        ["Montants", "euros entiers, sans decimale"],
        ["Plage", "%s au %s" % (
            min(df["Date"].map(parser_date_mixte)).strftime("%d/%m/%Y"),
            max(df["Date"].map(parser_date_mixte)).strftime("%d/%m/%Y"))],
        ["CA total", eur_espace(float(df["Montant"].sum())) + " €"],
        ["Categories", ", ".join(sorted(df["Catégorie"].unique()))],
        ["Regions", ", ".join(sorted(df["Région"].unique()))],
        ["Vendeurs", df["Vendeur"].nunique()],
    ])
    ligne("**Exercice 1 — filtrage multi-criteres.** Categorie "
          "« Électronique », montant strictement superieur a 500, region "
          "« Nord » ou « Sud » :")
    ligne()
    tableau(["Indicateur", "Valeur"], [
        ["Lignes renvoyees", len(ex1)],
        ["Somme des montants", eur_espace(float(ex1["Montant"].sum())) + " €"],
        ["Montant minimum renvoye", int(ex1["Montant"].min())],
        ["Montant maximum renvoye", int(ex1["Montant"].max())],
        ["dont region Nord", int((ex1["Région"] == "Nord").sum())],
        ["dont region Sud", int((ex1["Région"] == "Sud").sum())],
    ])
    ligne("**Exercice 2 — agregation, tri et `HAVING`.** Total par vendeur, "
          "trie decroissant :")
    ligne()
    tableau(["Vendeur", "Somme des montants", "Retenu par `HAVING > 1000` ?"],
            [[v, eur_espace(float(x)) + " €", "oui" if x > 1000 else "**non**"]
             for v, x in par_vendeur.items()])
    ligne("La requete de l'exercice 2 doit donc renvoyer **%d lignes** : "
          "%s %s exclu%s par la clause `HAVING`."
          % (len(retenus), " et ".join(exclus.index.tolist()),
             "sont" if len(exclus) > 1 else "est",
             "s" if len(exclus) > 1 else ""))
    ligne()
    ligne("**Exercice 3 — filtrage dynamique.** Combinaisons categorie x "
          "region a proposer comme jeu de test, avec le nombre de lignes "
          "attendu :")
    ligne()
    croise = df.pivot_table(index="Catégorie", columns="Région",
                            values="Montant", aggfunc="count").fillna(0)
    entetes = ["Categorie"] + list(croise.columns)
    tableau(entetes,
            [[c] + [int(v) for v in r] for c, r in croise.iterrows()])


# =====================================================================
def bloc_viz():
    print("\n[8] Ventes_Nettoyees.xlsx")
    df = pd.read_excel(os.path.join(DONNEES, "Ventes_Nettoyees.xlsx"))
    verifier(len(df) == 820, "820 lignes")
    verifier(df.isna().sum().sum() == 0, "aucune valeur manquante")

    correlation = df["Prix_Unitaire"].corr(df["Quantité"])
    verifier(correlation < -0.4,
             "correlation prix/quantite negative et exploitable (r = %.2f)"
             % correlation)

    par_mois = df.groupby("Mois_Année")["Chiffre_Affaires"].sum()
    par_cat = df.groupby("Catégorie")["Chiffre_Affaires"].sum().sort_values(
        ascending=False)
    par_region = df.groupby("Région")["Chiffre_Affaires"].sum().sort_values(
        ascending=False)
    saison_cat = df.pivot_table(index="Mois", columns="Catégorie",
                                values="Chiffre_Affaires", aggfunc="sum")

    titre(2, "Exercice A5 — `Ventes_Nettoyees.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes", len(df)],
        ["Colonnes", len(df.columns)],
        ["Tableau structure", "oui, nomme `DonneesNettoyees`"],
        ["Valeurs manquantes", 0],
        ["Colonnes temporelles deja derivees",
         "`Année`, `Mois`, `Nom_Mois`, `Mois_Année`"],
        ["CA total", eur_espace(float(df["Chiffre_Affaires"].sum())) + " €"],
        ["Marge totale", eur_espace(float(df["Marge"].sum())) + " €"],
        ["Taux de marge global",
         "%s %%" % eur(float(df["Marge"].sum() /
                             df["Chiffre_Affaires"].sum() * 100))],
    ])
    ligne("**Pattern 1 — saisonnalite.** CA par mois calendaire, cumul des "
          "deux annees, par categorie. Le pic de rentree de la papeterie "
          "(aout-septembre), le pic de fin d'annee de l'electronique et de "
          "la telephonie et le pic estival de l'electromenager sont "
          "reellement dans les donnees.")
    ligne()
    mois_noms = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.",
                 "août", "sept.", "oct.", "nov.", "déc."]
    tableau(["Mois"] + list(saison_cat.columns),
            [[mois_noms[int(m) - 1]] + [eur_espace(float(v)) for v in r]
             for m, r in saison_cat.iterrows()])
    ligne("**Pattern 2 — ecart entre regions.** CA par region :")
    ligne()
    tableau(["Region", "CA", "Part du total"],
            [[r, eur_espace(float(v)) + " €",
              "%s %%" % eur(float(v) / float(df["Chiffre_Affaires"].sum())
                            * 100)] for r, v in par_region.items()])
    ligne("**Pattern 3 — correlation prix / quantite.** Coefficient de "
          "Pearson : **r = %s** sur %d points. La relation est "
          "decroissante et non lineaire : plus le prix unitaire monte, plus "
          "les quantites par transaction chutent. Un nuage de points "
          "`Prix_Unitaire` en X et `Quantité` en Y le montre nettement ; "
          "une echelle logarithmique sur X ameliore encore la lecture."
          % (eur(float(correlation)), len(df)))
    ligne()
    ligne("Repartition par categorie (pour l'histogramme de comparaison) :")
    ligne()
    tableau(["Categorie", "CA", "Nb de transactions"],
            [[c, eur_espace(float(v)), int((df["Catégorie"] == c).sum())]
             for c, v in par_cat.items()])
    ligne("Serie mensuelle complete (pour la courbe d'evolution), %d points :"
          % len(par_mois))
    ligne()
    tableau(["Mois_Année", "CA"],
            [[m, eur_espace(float(v)) + " €"] for m, v in par_mois.items()])


# =====================================================================
def bloc_dashboard():
    print("\n[9] Dashboard_Source.xlsx")
    df = pd.read_excel(os.path.join(DONNEES, "Dashboard_Source.xlsx"))
    verifier(len(df) >= 500, "%d lignes (minimum de 500 respecte)" % len(df))

    doublons = int(df.duplicated().sum())
    verifier(doublons == 6, "6 doublons stricts")

    dates_texte = int(df["Date"].map(lambda v: isinstance(v, str)).sum())
    verifier(dates_texte == 10, "10 dates saisies en texte")

    region_sale = int(df["Région"].map(lambda v: v != str(v).strip()).sum())
    verifier(region_sale == 8, "8 libelles de region avec espace parasite")

    remises_vides = int(df["Remise"].isna().sum())
    verifier(remises_vides == 5, "5 remises manquantes")

    propre = df.drop_duplicates().copy()
    propre["Région"] = propre["Région"].str.strip()
    propre["Date"] = pd.to_datetime(propre["Date"], dayfirst=True,
                                    format="mixed")
    propre["Mois"] = propre["Date"].dt.to_period("M").astype(str)

    ca = float(propre["CA_Net"].sum())
    marge = float(propre["Marge"].sum())
    panier = ca / len(propre)

    titre(2, "Exercice B5 — `Dashboard_Source.xlsx`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes livrees", len(df)],
        ["Colonnes", len(df.columns)],
        ["Forme livree", "plage simple — le `Ctrl+T` est a la charge de "
                         "l'apprenant"],
        ["Doublons stricts a supprimer", doublons],
        ["Dates saisies en texte (bloquent le groupement du TCD)",
         dates_texte],
        ["Libelles `Région` a nettoyer (espace parasite)", region_sale],
        ["Remises manquantes", remises_vides],
        ["Lignes apres dedoublonnage", len(propre)],
    ])
    ligne("**KPI de reference apres nettoyage** (doublons supprimes, "
          "regions detassees, dates converties) :")
    ligne()
    tableau(["KPI", "Valeur"], [
        ["CA net total", eur_espace(ca) + " €"],
        ["Marge totale", eur_espace(marge) + " €"],
        ["Taux de marge", "%s %%" % eur(marge / ca * 100)],
        ["Panier moyen", eur(panier) + " €"],
        ["Nombre de commandes", len(propre)],
        ["Quantite totale vendue", int(propre["Quantité"].sum())],
        ["Remise moyenne accordee",
         "%s %%" % eur(float(propre["Remise"].mean()) * 100)],
    ])
    for libelle, colonne in [("region", "Région"), ("categorie", "Catégorie"),
                             ("magasin", "Magasin"),
                             ("segment client", "Segment_Client")]:
        agg = propre.groupby(colonne)["CA_Net"].sum().sort_values(
            ascending=False)
        ligne("CA net par %s :" % libelle)
        ligne()
        tableau([colonne, "CA net"],
                [[k, eur_espace(float(v)) + " €"] for k, v in agg.items()])
    mensuel = propre.groupby("Mois")["CA_Net"].sum()
    ligne("Serie mensuelle du CA net (12 points, pour la courbe de "
          "tendance du dashboard) :")
    ligne()
    tableau(["Mois", "CA net"],
            [[m, eur_espace(float(v)) + " €"] for m, v in mensuel.items()])


# =====================================================================
def bloc_ventes2023():
    print("\n[10] ventes_2023.csv")
    chemin = os.path.join(DONNEES, "ventes_2023.csv")
    df = pd.read_csv(chemin, sep=";", encoding="utf-8-sig", dtype=str)
    verifier(list(df.columns) == ["Date", "ID_Produit", "Produit",
                                 "Catégorie", "Vendeur", "Quantité",
                                 "Prix_Unitaire", "Cout_Unitaire", "Région"],
             "colonnes conformes (Produit et Cout_Unitaire ajoutes)")

    doublons = int(df.duplicated().sum())
    verifier(doublons >= 22,
             "%d doublons stricts (22 injectes + doublons naturels)"
             % doublons)

    iso = int(df["Date"].str.match(r"^\d{4}-\d{2}-\d{2}$").sum())
    verifier(iso == 180, "180 dates au format ISO texte")

    df["qte"] = df["Quantité"].astype(int)
    df["pu"] = df["Prix_Unitaire"].str.replace(",", ".").astype(float)
    df["cu"] = df["Cout_Unitaire"].str.replace(",", ".").astype(float)

    aberrantes_qte = df[df["qte"].abs() > 1000]
    negatives = df[df["qte"] < 0]
    prix_aberrant = df[df["pu"] <= 0.01]
    verifier(len(aberrantes_qte) >= 6, "quantites aberrantes presentes")
    verifier(len(negatives) == 3, "3 quantites negatives")
    verifier(len(prix_aberrant) == 4, "4 prix unitaires aberrants")

    propre = df.drop_duplicates().copy()
    propre = propre[(propre["qte"] > 0) & (propre["qte"] <= 1000) &
                    (propre["pu"] > 0.01)]
    propre["date"] = propre["Date"].map(parser_date_mixte)
    propre["mois"] = propre["date"].map(lambda d: d.month)
    propre["trimestre"] = propre["mois"].map(lambda m: (m - 1) // 3 + 1)
    propre["CA"] = propre["qte"] * propre["pu"]
    propre["marge"] = propre["qte"] * (propre["pu"] - propre["cu"])

    titre(2, "Exercices A6 et B6 — `ventes_2023.csv`")
    tableau(["Controle", "Valeur attendue"], [
        ["Lignes livrees", len(df)],
        ["Doublons stricts", doublons],
        ["Dates au format `AAAA-MM-JJ` (texte)", iso],
        ["Dates au format `JJ/MM/AAAA`", len(df) - iso],
        ["Quantites aberrantes (9 999 / 4 500)", len(aberrantes_qte)],
        ["Quantites negatives (retours mal saisis)", len(negatives)],
        ["Prix unitaires aberrants (0,01 €)", len(prix_aberrant)],
        ["Lignes retenues apres nettoyage", len(propre)],
        ["Lignes ecartees", len(df) - len(propre)],
        ["CA total apres nettoyage",
         eur_espace(float(propre["CA"].sum())) + " €"],
        ["Marge brute totale",
         eur_espace(float(propre["marge"].sum())) + " €"],
    ])

    ligne("**Q1 — tendance mensuelle du CA par categorie.**")
    ligne()
    pivot = propre.pivot_table(index="mois", columns="Catégorie",
                               values="CA", aggfunc="sum").fillna(0)
    pivot["Total"] = pivot.sum(axis=1)
    mois_noms = ["janvier", "février", "mars", "avril", "mai", "juin",
                 "juillet", "août", "septembre", "octobre", "novembre",
                 "décembre"]
    tableau(["Mois"] + list(pivot.columns),
            [[mois_noms[int(m) - 1]] + [eur_espace(float(v)) for v in r]
             for m, r in pivot.iterrows()])
    meilleur = int(pivot["Total"].idxmax())
    ligne("Mois le plus performant, toutes categories confondues : "
          "**%s** avec %s €. Par categorie, le mois de pointe differe : %s."
          % (mois_noms[meilleur - 1], eur_espace(float(pivot["Total"].max())),
             " ; ".join("%s en %s" % (c, mois_noms[int(pivot[c].idxmax()) - 1])
                        for c in pivot.columns if c != "Total")))
    ligne()

    ligne("**Q2 — top 3 des produits les plus rentables par region** "
          "(marge brute = quantite x (prix de vente - cout d'achat)).")
    ligne()
    for region in sorted(propre["Région"].unique()):
        sous = propre[propre["Région"] == region]
        top = sous.groupby("Produit")["marge"].sum().sort_values(
            ascending=False).head(3)
        ligne("Region **%s** :" % region)
        ligne()
        tableau(["Rang", "Produit", "Marge brute"],
                [[i + 1, p, eur_espace(float(v)) + " €"]
                 for i, (p, v) in enumerate(top.items())])

    ligne("**Q3 — performance des vendeurs par region.** Chaque vendeur "
          "n'opere que sur une region : la question de l'enonce est un piege "
          "methodologique, il n'y a pas de correlation a mesurer mais un "
          "effet de structure a identifier. Le CA d'un vendeur est d'abord "
          "determine par le poids commercial de sa region.")
    ligne()
    vend = propre.groupby(["Région", "Vendeur"]).agg(
        CA=("CA", "sum"), Lignes=("CA", "count")).reset_index()
    vend["CA_moyen"] = vend["CA"] / vend["Lignes"]
    vend = vend.sort_values("CA", ascending=False)
    tableau(["Region", "Vendeur", "CA", "Nb de lignes", "Panier moyen"],
            [[r["Région"], r["Vendeur"], eur_espace(float(r["CA"])) + " €",
              int(r["Lignes"]), eur(float(r["CA_moyen"])) + " €"]
             for _, r in vend.iterrows()])

    ligne("**Q4 — taux de croissance du CA entre le premier et le dernier "
          "trimestre.**")
    ligne()
    par_trim = propre.groupby("trimestre")["CA"].sum()
    croissance = par_trim[4] / par_trim[1] - 1
    tableau(["Trimestre", "CA"],
            [["T%d" % t, eur_espace(float(v)) + " €"]
             for t, v in par_trim.items()])
    ligne("Taux de croissance T4 / T1 : **+%s %%** "
          "(%s € contre %s €)."
          % (eur(croissance * 100), eur_espace(float(par_trim[4])),
             eur_espace(float(par_trim[1]))))
    ligne()
    ligne("Sensibilite au nettoyage : si les valeurs aberrantes ne sont PAS "
          "retirees, le CA total passe a %s € et le taux T4/T1 a %s %%. "
          "L'ecart justifie a lui seul l'etape 1 de l'enonce."
          % (eur_espace(float((df["qte"] * df["pu"]).sum())),
             eur(_croissance_brute(df) * 100)))


def _croissance_brute(df):
    brut = df.copy()
    brut["date"] = brut["Date"].map(parser_date_mixte)
    brut["trimestre"] = brut["date"].map(lambda d: (d.month - 1) // 3 + 1)
    brut["CA"] = brut["qte"] * brut["pu"]
    par_trim = brut.groupby("trimestre")["CA"].sum()
    return par_trim[4] / par_trim[1] - 1


# =====================================================================
def main():
    if not os.path.isdir(CORRIGES):
        os.makedirs(CORRIGES)

    titre(1, "Valeurs de reference — jeux de donnees de la formation Excel")
    ligne("Document **formateur**, non distribue aux apprenants.")
    ligne()
    ligne("Toutes les valeurs ci-dessous sont recalculees directement depuis "
          "les fichiers livres par `python3 verifier_donnees.py`. Elles "
          "servent a corriger sans refaire le TP, et a detecter qu'un "
          "apprenant a saute une etape de nettoyage : les ecarts de CA sont "
          "signes.")

    bloc_ventes_brutes()
    bloc_clients()
    bloc_projet()
    bloc_ventes_ref()
    bloc_marges()
    bloc_globales()
    bloc_query()
    bloc_viz()
    bloc_dashboard()
    bloc_ventes2023()

    chemin = os.path.join(CORRIGES, "valeurs-de-reference.md")
    with io.open(chemin, "w", encoding="utf-8") as f:
        f.write("\n".join(sortie).replace("\n\n\n", "\n\n") + "\n")

    print("\n" + "=" * 60)
    if alertes:
        print("%d CONTROLE(S) EN ECHEC :" % len(alertes))
        for a in alertes:
            print("  - %s" % a)
    else:
        print("Tous les controles sont passes.")
    print("Valeurs de reference ecrites dans corriges/valeurs-de-reference.md")


if __name__ == "__main__":
    main()
