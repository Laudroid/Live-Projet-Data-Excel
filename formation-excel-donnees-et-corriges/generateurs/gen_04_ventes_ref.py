# -*- coding: utf-8 -*-
"""Ventes.xlsx + Referentiel.xlsx -- couple transactionnel / referentiel.

Sert a l'enonce : Serie A / exercice 3 -- Analyser les donnees avec des
fonctions complexes (RECHERCHEX, SOMME.SI.ENS, NB.SI.ENS).

Ventes.xlsx ne contient QUE les colonnes de l'enonce (Date, ID_Produit,
Quantite, ID_Magasin) : le nom du produit, le prix et la region doivent
etre rapatries depuis Referentiel.xlsx.

Quelques identifiants orphelins (produits et magasins absents du
referentiel) sont injectes volontairement : ils produisent des #N/A et
obligent l'apprenant a controler ses resultats plutot qu'a faire confiance
au glissement de formule.
"""

import datetime as dt

import gen_core as core
import referentiel as ref

PRODUITS_ORPHELINS = ["P512", "P998"]
MAGASINS_ORPHELINS = ["MAG21"]


def main():
    rng = core.rng_pour("ventes_referentiel")
    # dernier trimestre du referentiel commun
    transactions = core.tirer_transactions(
        rng, dt.date(2024, 10, 1), dt.date(2024, 12, 31), 260,
        croissance_annuelle=0.0)

    lignes = []
    for t in transactions:
        lignes.append([t["date"], t["id_produit"], t["quantite"],
                       t["id_magasin"]])

    # identifiants orphelins : 4 produits inconnus, 3 magasins inconnus
    indices = rng.sample(range(len(lignes)), 7)
    for k, i in enumerate(indices[:4]):
        lignes[i][1] = PRODUITS_ORPHELINS[k % len(PRODUITS_ORPHELINS)]
    for i in indices[4:]:
        lignes[i][3] = MAGASINS_ORPHELINS[0]

    wb = core.nouveau_classeur("Ventes")
    core.ecrire_feuille(
        wb["Ventes"],
        ["Date", "ID_Produit", "Quantité", "ID_Magasin"],
        lignes,
        formats={1: "DD/MM/YYYY"},
        largeurs={1: 13, 2: 13, 3: 11, 4: 13},
        nom_tableau="Ventes",
    )
    core.enregistrer(wb, "Ventes.xlsx")

    # ------------------------------------------------------ referentiel
    wb2 = core.nouveau_classeur("Produits")
    core.ecrire_feuille(
        wb2["Produits"],
        ["ID_Produit", "Nom_Produit", "Prix_Unitaire"],
        [[p[0], p[1], p[3]] for p in ref.PRODUITS],
        formats={3: "# ##0.00 €"},
        largeurs={1: 13, 2: 34, 3: 15},
        nom_tableau="Produits",
    )
    wb2.create_sheet("Magasins")
    core.ecrire_feuille(
        wb2["Magasins"],
        ["ID_Magasin", "Nom_Magasin", "Ville", "Région"],
        [[m[0], ref.MAGASINS_ACC[m[0]][0], ref.MAGASINS_ACC[m[0]][1],
          ref.REGIONS_ACC[m[3]]] for m in ref.MAGASINS],
        largeurs={1: 13, 2: 30, 3: 16, 4: 16},
        nom_tableau="Magasins",
    )
    core.enregistrer(wb2, "Referentiel.xlsx")
    print("     Ventes.xlsx : %d lignes dont 7 a identifiant orphelin"
          % len(lignes))


if __name__ == "__main__":
    main()
