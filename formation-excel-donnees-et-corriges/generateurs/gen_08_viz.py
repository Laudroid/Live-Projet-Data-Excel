# -*- coding: utf-8 -*-
"""Ventes_Nettoyees.xlsx -- jeu propre et enrichi.

Sert a l'enonce : Serie A / exercice 5 -- Creer des visualisations
pertinentes. L'enonce parle d'un "jeu de donnees nettoye et structure,
issu des sessions precedentes" : ce fichier represente donc l'etat du
dataset apres les TP de nettoyage et d'indicateurs derives (colonnes
temporelles deja creees).

Trois patterns sont reellement presents dans les donnees, pour que les
graphiques demandes aient quelque chose a montrer :
  1. saisonnalite marquee (pic de rentree en papeterie, pic de fin d'annee
     en electronique et telephonie, pic estival en electromenager)
  2. ecart de volume net entre regions (Ile-de-France > Sud > Nord > ...)
  3. correlation negative entre prix unitaire et quantite vendue,
     exploitable en nuage de points
"""

import datetime as dt

import gen_core as core

MOIS_FR = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
           "août", "septembre", "octobre", "novembre", "décembre"]


def main():
    rng = core.rng_pour("ventes_nettoyees")
    transactions = core.tirer_transactions(
        rng, dt.date(2023, 1, 1), dt.date(2024, 12, 31), 820,
        croissance_annuelle=0.13)

    lignes = []
    for t in transactions:
        date = t["date"]
        marge = round(t["ca"] - t["cout_total"], 2)
        lignes.append([
            t["id_vente"],
            date,
            date.year,
            date.month,
            MOIS_FR[date.month - 1],
            "%04d-%02d" % (date.year, date.month),
            t["categorie"],
            t["produit"],
            t["region"],
            t["vendeur"],
            t["quantite"],
            t["prix_unitaire"],
            t["ca"],
            marge,
            round(marge / t["ca"], 4) if t["ca"] else None,
        ])

    wb = core.nouveau_classeur("Données")
    core.ecrire_feuille(
        wb["Données"],
        ["ID_Vente", "Date", "Année", "Mois", "Nom_Mois", "Mois_Année",
         "Catégorie", "Produit", "Région", "Vendeur", "Quantité",
         "Prix_Unitaire", "Chiffre_Affaires", "Marge", "Taux_Marge"],
        lignes,
        formats={2: "DD/MM/YYYY", 12: "# ##0.00 €", 13: "# ##0.00 €",
                 14: "# ##0.00 €", 15: "0.0 %"},
        largeurs={1: 11, 2: 12, 3: 9, 4: 8, 5: 13, 6: 13, 7: 17, 8: 32,
                  9: 16, 10: 19, 11: 11, 12: 14, 13: 17, 14: 13, 15: 12},
        nom_tableau="DonneesNettoyees",
    )
    core.enregistrer(wb, "Ventes_Nettoyees.xlsx")
    print("     %d lignes, colonnes temporelles deja derivees" % len(lignes))


if __name__ == "__main__":
    main()
