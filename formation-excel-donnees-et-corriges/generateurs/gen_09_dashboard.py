# -*- coding: utf-8 -*-
"""Dashboard_Source.xlsx -- jeu de pilotage de plus de 500 lignes.

Sert a l'enonce : Serie B / exercice 5 -- Concevoir un dashboard.

L'enonce impose au minimum 500 lignes et demande, en etape 1, de verifier
l'absence de doublons et la coherence des formats. Le fichier contient
donc quelques defauts a reperer, mais reste globalement propre : le coeur
du TP est la modelisation et le design, pas le nettoyage.

Defauts injectes :
  * 6 doublons stricts de commande
  * 10 dates saisies en texte (bloquent le groupement par mois du TCD)
  * 8 libelles de region avec espace parasite
  * 5 remises manquantes
Livre en PLAGE SIMPLE : l'apprenant doit faire Ctrl+T lui-meme.
"""

import datetime as dt

import gen_core as core


def main():
    rng = core.rng_pour("dashboard_source")
    transactions = core.tirer_transactions(
        rng, dt.date(2024, 1, 1), dt.date(2024, 12, 31), 900,
        croissance_annuelle=0.15)

    lignes = []
    for i, t in enumerate(transactions, start=1):
        remise = rng.choice([0, 0, 0, 0.05, 0.05, 0.10, 0.15])
        ca_brut = t["ca"]
        ca_net = round(ca_brut * (1 - remise), 2)
        lignes.append([
            "CMD%05d" % i,
            t["date"],
            t["magasin"],
            t["region"],
            t["vendeur"],
            t["categorie"],
            t["produit"],
            t["quantite"],
            t["prix_unitaire"],
            t["cout_unitaire"],
            remise,
            ca_net,
            round(ca_net - t["cout_total"], 2),
            rng.choice(["Grand compte", "PME", "TPE", "Administration",
                        "Particulier"]),
            rng.choice(["Carte bancaire", "Virement", "Prélèvement",
                        "Chèque", "Espèces"]),
        ])

    indices = list(range(len(lignes)))
    rng.shuffle(indices)

    # dates saisies en texte
    for i in indices[0:10]:
        lignes[i][1] = lignes[i][1].strftime("%d/%m/%Y")

    # libelles de region avec espace parasite
    for i in indices[10:18]:
        lignes[i][3] = " %s " % lignes[i][3]

    # remises manquantes
    for i in indices[18:23]:
        lignes[i][10] = None

    # doublons stricts (la ligne entiere est recopiee, identifiant inclus)
    for i in rng.sample(indices[23:], 6):
        lignes.append(list(lignes[i]))

    rng.shuffle(lignes)

    wb = core.nouveau_classeur("Données")
    core.ecrire_feuille(
        wb["Données"],
        ["ID_Commande", "Date", "Magasin", "Région", "Vendeur", "Catégorie",
         "Produit", "Quantité", "Prix_Unitaire", "Cout_Unitaire", "Remise",
         "CA_Net", "Marge", "Segment_Client", "Mode_Paiement"],
        lignes,
        formats={2: "DD/MM/YYYY", 9: "# ##0.00 €", 10: "# ##0.00 €",
                 11: "0 %", 12: "# ##0.00 €", 13: "# ##0.00 €"},
        largeurs={1: 13, 2: 12, 3: 28, 4: 16, 5: 19, 6: 17, 7: 32, 8: 10,
                  9: 14, 10: 14, 11: 10, 12: 14, 13: 13, 14: 17, 15: 16},
        nom_tableau=None,  # volontairement une plage simple
    )
    core.enregistrer(wb, "Dashboard_Source.xlsx")
    print("     %d lignes dont 6 doublons stricts" % len(lignes))


if __name__ == "__main__":
    main()
