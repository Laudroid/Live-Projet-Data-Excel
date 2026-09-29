# -*- coding: utf-8 -*-
"""ventes_2023.csv -- jeu du cas metier de synthese.

Sert aux enonces :
  * Serie A / exercice 6 -- Resoudre un probleme data metier
  * Serie B / exercice 6 -- Presenter les resultats (reprend les memes
    conclusions pour construire la narration)

Colonnes de l'enonce : Date, ID_Produit, Categorie, Vendeur, Quantite,
Prix_Unitaire, Region. Une colonne Cout_Unitaire est ajoutee : sans elle,
la question Q2 sur la marge brute serait insoluble. Une colonne Produit
est egalement ajoutee pour que le top 3 soit lisible sans jointure.

Defauts injectes, en lien direct avec la consigne 1 de l'enonce
(doublons, formats de date, valeurs aberrantes) :
  * 22 doublons stricts de transaction
  * 180 dates au format ISO texte (2023-03-05) au milieu de dates
    francaises (05/03/2023)
  * 6 quantites aberrantes (9 999 et 4 500 unites)
  * 4 prix unitaires aberrants (0,01 EUR)
  * 3 lignes de quantite negative (retours mal saisis)
"""

import datetime as dt

import gen_core as core


def main():
    rng = core.rng_pour("ventes_2023")
    transactions = core.tirer_transactions(
        rng, dt.date(2023, 1, 1), dt.date(2023, 12, 31), 1500,
        croissance_annuelle=0.16)

    entetes = ["Date", "ID_Produit", "Produit", "Catégorie", "Vendeur",
               "Quantité", "Prix_Unitaire", "Cout_Unitaire", "Région"]

    lignes = []
    for t in transactions:
        lignes.append([
            t["date"].strftime("%d/%m/%Y"),
            t["id_produit"],
            t["produit"],
            t["categorie"],
            t["vendeur"],
            str(t["quantite"]),
            ("%.2f" % t["prix_unitaire"]).replace(".", ","),
            ("%.2f" % t["cout_unitaire"]).replace(".", ","),
            t["region"],
            t["date"],  # conserve pour le reformatage, retire a l'ecriture
        ])

    indices = list(range(len(lignes)))
    rng.shuffle(indices)

    # dates au format ISO texte
    for i in indices[0:180]:
        lignes[i][0] = lignes[i][9].strftime("%Y-%m-%d")

    # quantites aberrantes
    for k, i in enumerate(indices[180:186]):
        lignes[i][5] = "9999" if k % 2 == 0 else "4500"

    # prix unitaires aberrants
    for i in indices[186:190]:
        lignes[i][6] = "0,01"

    # retours mal saisis : quantites negatives
    for i in indices[190:193]:
        lignes[i][5] = "-%s" % lignes[i][5]

    # doublons stricts
    for i in rng.sample(indices[193:], 22):
        lignes.append(list(lignes[i]))

    rng.shuffle(lignes)

    chemin = core.dossier_sortie() + "/ventes_2023.csv"
    with open(chemin, "w", encoding="utf-8-sig", newline="") as f:
        f.write(";".join(entetes) + "\r\n")
        for ligne in lignes:
            f.write(";".join(str(v) for v in ligne[:9]) + "\r\n")

    print("  ecrit : ventes_2023.csv (%d lignes dont 22 doublons)"
          % len(lignes))


if __name__ == "__main__":
    main()
