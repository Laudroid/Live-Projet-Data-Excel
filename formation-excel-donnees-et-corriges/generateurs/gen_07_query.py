# -*- coding: utf-8 -*-
"""Data_Ventes.csv -- jeu a importer dans Google Sheets pour QUERY.

Sert a l'enonce : Serie B / exercice 4 -- Utiliser QUERY pour l'analyse
structuree. Attention : QUERY est une fonction Google Sheets, elle n'existe
pas dans Excel.

L'ordre des colonnes respecte strictement l'enonce, car les requetes
designent les colonnes par leur lettre :
  A Date | B Categorie | C Produit | D Vendeur | E Montant | F Region

Calibrage des filtres de l'enonce (verifie par verifier_donnees.py) :
  * exercice 1 : Categorie = "Électronique" ET Montant > 500 ET
    Region dans ("Nord", "Sud") -> resultat non vide, une vingtaine de lignes
  * exercice 2 : la clause HAVING SUM(E) > 1000 doit exclure des vendeurs
    sans les exclure tous -> deux vendeurs saisonniers a tres faible volume
    (Sofia Renard, Bastien Roux) sont presents dans le referentiel commun

Le fichier est ecrit en UTF-8 avec BOM : ici l'encodage n'est pas le sujet
du TP, l'import dans Sheets doit etre propre.

La colonne Montant est en euros entiers, sans decimales. C'est un choix
delibere : un CSV a separateur virgule contenant des decimales pointees
s'importe en TEXTE dans un classeur Sheets configure en locale francaise,
et les clauses SUM() renverraient alors silencieusement 0.
"""

import datetime as dt

import gen_core as core


def main():
    rng = core.rng_pour("data_ventes_query")
    transactions = core.tirer_transactions(
        rng, dt.date(2024, 1, 1), dt.date(2024, 12, 31), 320,
        croissance_annuelle=0.08)

    entetes = ["Date", "Catégorie", "Produit", "Vendeur", "Montant",
               "Région"]
    lignes = []
    for t in transactions:
        lignes.append([
            t["date"].strftime("%d/%m/%Y"),
            t["categorie"],
            t["produit"],
            t["vendeur"],
            "%d" % int(round(t["ca"])),
            t["region"],
        ])

    chemin = core.dossier_sortie() + "/Data_Ventes.csv"
    with open(chemin, "w", encoding="utf-8-sig", newline="") as f:
        f.write(",".join(entetes) + "\n")
        for ligne in lignes:
            # les libelles ne contiennent pas de virgule : pas de guillemets
            f.write(",".join(ligne) + "\n")

    print("  ecrit : Data_Ventes.csv (%d lignes)" % len(lignes))


if __name__ == "__main__":
    main()
