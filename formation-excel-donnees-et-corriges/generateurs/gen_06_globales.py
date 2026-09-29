# -*- coding: utf-8 -*-
"""Ventes_Globales.xlsx -- historique pour l'analyse par TCD.

Sert a l'enonce : Serie A / exercice 4 -- Explorer les donnees via les TCD.

Le fichier est livre en PLAGE SIMPLE, pas en tableau structure : la
premiere etape de l'enonce demande justement a l'apprenant de faire
Ctrl+T et de nommer le tableau DonneesVentes.

La question de l'enonce "quelle region affiche la plus forte
saisonnalite ?" impose un profil mensuel PROPRE A LA REGION, injecte ici
via SAISON_REGION. Amplifier la saisonnalite des categories ne suffit
pas : leurs pics tombent a des mois differents et s'annulent une fois
agreges par region, si bien que le classement des regions ne refletait
que le bruit d'echantillonnage.

Avec ce profil, le Sud culmine nettement en juin-aout (activite
touristique) et l'Ile-de-France reste plate. Sur les 1600 lignes
livrees, le coefficient de variation du CA mensuel place le Sud tres
au-dessus des autres regions et l'Ile-de-France tres en dessous : la
reponse est lisible dans le TCD Region x Mois et robuste au changement
d'indicateur.
"""

import datetime as dt

import gen_core as core

# Profil mensuel par region, index 0 = janvier.
SAISON_REGION = {
    "Sud":           [0.50, 0.50, 0.65, 0.85, 1.20, 1.65, 2.05, 1.95, 1.05,
                      0.70, 0.55, 0.55],
    "Ouest":         [0.85, 0.85, 0.95, 1.00, 1.10, 1.25, 1.35, 1.30, 1.00,
                      0.90, 0.85, 0.85],
    "Nord":          [1.05, 1.00, 1.00, 0.95, 0.95, 0.90, 0.90, 0.95, 1.05,
                      1.05, 1.10, 1.10],
    "Est":           [1.00] * 12,
    "Centre":        [1.00] * 12,
    "Ile-de-France": [1.00] * 12,
}


def main():
    rng = core.rng_pour("ventes_globales")
    transactions = core.tirer_transactions(
        rng, dt.date(2023, 1, 1), dt.date(2024, 12, 31), 1600,
        croissance_annuelle=0.12, saison_region=SAISON_REGION)

    lignes = []
    for t in transactions:
        lignes.append([
            t["date"],
            t["region"],
            t["categorie"],
            t["vendeur"],
            t["ca"],
            t["quantite"],
        ])

    wb = core.nouveau_classeur("Données")
    core.ecrire_feuille(
        wb["Données"],
        ["Date", "Région", "Catégorie de produit", "Vendeur",
         "Chiffre d'affaires (CA)", "Quantité vendue"],
        lignes,
        formats={1: "DD/MM/YYYY", 5: "# ##0.00 €"},
        largeurs={1: 13, 2: 16, 3: 22, 4: 20, 5: 22, 6: 16},
        nom_tableau=None,  # volontairement une plage simple
    )
    core.enregistrer(wb, "Ventes_Globales.xlsx")
    print("     %d lignes sur 24 mois" % len(lignes))


if __name__ == "__main__":
    main()
