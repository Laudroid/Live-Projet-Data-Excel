# -*- coding: utf-8 -*-
"""Ventes_Projet.xlsx -- jeu propre, pret pour les colonnes calculees.

Sert a l'enonce : Serie B / exercice 2 -- Creer des indicateurs derives.

Le fichier est volontairement SANS colonne temporelle derivee : l'apprenant
doit creer Annee, Mois, Nom du Mois et Mois-Annee. La plage couvre 24 mois
(2023-2024) pour que le tri chronologique du TCD pose reellement probleme
si la cle Mois-Annee est traitee comme du texte.
"""

import datetime as dt

import gen_core as core


def main():
    rng = core.rng_pour("ventes_projet")
    transactions = core.tirer_transactions(
        rng, dt.date(2023, 1, 1), dt.date(2024, 12, 31), 600,
        croissance_annuelle=0.14)

    lignes = []
    for t in transactions:
        lignes.append([
            t["id_vente"],
            t["date"],
            t["id_produit"],
            t["produit"],
            t["categorie"],
            t["region"],
            t["vendeur"],
            t["quantite"],
            t["prix_unitaire"],
            t["ca"],
        ])

    wb = core.nouveau_classeur("Ventes")
    core.ecrire_feuille(
        wb["Ventes"],
        ["ID_Vente", "Date_Vente", "ID_Produit", "Produit", "Categorie",
         "Region", "Vendeur", "Quantite", "Prix_Unitaire",
         "Chiffre_Affaires"],
        lignes,
        formats={2: "DD/MM/YYYY", 9: "# ##0.00 €", 10: "# ##0.00 €"},
        largeurs={1: 11, 2: 13, 3: 12, 4: 32, 5: 17, 6: 16, 7: 19, 8: 10,
                  9: 14, 10: 17},
        nom_tableau="Ventes",
    )
    core.enregistrer(wb, "Ventes_Projet.xlsx")
    print("     %d lignes, du %s au %s" % (
        len(lignes), lignes[0][1].strftime("%d/%m/%Y"),
        lignes[-1][1].strftime("%d/%m/%Y")))


if __name__ == "__main__":
    main()
