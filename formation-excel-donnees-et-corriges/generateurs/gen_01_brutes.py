# -*- coding: utf-8 -*-
"""ventes_brutes.csv -- export systeme volontairement degrade.

Sert aux enonces :
  * Serie A / exercice 1 -- Importer et preparer un dataset reel
  * Serie B / exercice 1 -- Assurer la qualite des donnees importees

Anomalies injectees (et uniquement celles-la) :
  1. encodage : fichier ecrit en UTF-8 sans BOM, donc ouvert en
     Windows-1252 par Excel francais -> les accents s'affichent en mojibake
  2. dates : trois formats textuels concurrents + quelques dates aberrantes
  3. montants : separateur decimal point ou virgule, espaces insecables
     comme separateur de milliers, cellules vides, cellules textuelles
  4. libelles clients : espaces en debut/fin et espaces doubles internes
  5. identifiants clients manquants
  6. lignes entierement vides
"""

import datetime as dt

import gen_core as core
import referentiel as ref

MOIS_FR_COURT = ["janv", "févr", "mars", "avr", "mai", "juin",
                 "juil", "août", "sept", "oct", "nov", "déc"]

NBSP = u"\u00a0"

ENTETES = ["ID_Vente", "Date_Vente", "ID_Client", "Client", "ID_Produit",
           "Produit", "Categorie", "Quantite", "Montant", "ID_Magasin",
           "Magasin", "Ville", "Region", "Vendeur"]


def construire_clients(rng, nombre):
    clients = []
    for i in range(1, nombre + 1):
        prenom = rng.choice(ref.PRENOMS)
        nom = rng.choice(ref.NOMS)
        clients.append(("CLI%03d" % i, "%s %s" % (prenom, nom)))
    return clients


def formater_date(rng, date):
    tirage = rng.random()
    if tirage < 0.60:
        return date.strftime("%d/%m/%Y")
    if tirage < 0.85:
        return "%04d.%02d.%02d" % (date.year, date.month, date.day)
    return "%d-%s-%02d" % (date.day, MOIS_FR_COURT[date.month - 1],
                           date.year % 100)


def formater_montant(rng, montant):
    tirage = rng.random()
    texte = "%.2f" % montant
    if tirage < 0.15:
        # separateur decimal anglo-saxon laisse tel quel
        return texte
    entier, decimales = texte.split(".")
    if len(entier) > 3:
        # l'export applique systematiquement un espace insecable comme
        # separateur de milliers : invisible a l'oeil, bloquant pour Excel
        entier = entier[:-3] + NBSP + entier[-3:]
    return "%s,%s" % (entier, decimales)


def salir_client(rng, nom):
    tirage = rng.random()
    if tirage < 0.10:
        return "  " + nom + " "
    if tirage < 0.16:
        return nom + "   "
    if tirage < 0.21:
        return " " + nom.replace(" ", "  ")
    return nom


def main():
    rng = core.rng_pour("ventes_brutes")
    transactions = core.tirer_transactions(
        rng, dt.date(2023, 1, 1), dt.date(2023, 12, 31), 420,
        croissance_annuelle=0.10)

    clients = construire_clients(rng, 95)

    lignes = []
    for t in transactions:
        id_client, nom_client = rng.choice(clients)
        lignes.append([
            t["id_vente"],
            formater_date(rng, t["date"]),
            id_client,
            salir_client(rng, nom_client),
            t["id_produit"],
            t["produit"],
            t["categorie"],
            str(t["quantite"]),
            formater_montant(rng, t["ca"]),
            t["id_magasin"],
            t["magasin"],
            t["ville"],
            t["region"],
            t["vendeur"],
        ])

    indices = list(range(len(lignes)))
    rng.shuffle(indices)
    curseur = 0

    # 1. montants vides (6 lignes)
    for i in indices[curseur:curseur + 6]:
        lignes[i][8] = ""
    curseur += 6

    # 2. montants textuels (5 lignes)
    textes = ["à valider", "N/A", "erreur import", "-", "NON COMMUNIQUE"]
    for k, i in enumerate(indices[curseur:curseur + 5]):
        lignes[i][8] = textes[k]
    curseur += 5

    # 3. identifiants clients manquants (5 lignes)
    for i in indices[curseur:curseur + 5]:
        lignes[i][2] = ""
    curseur += 5

    # 4. dates aberrantes : trois dates situees dans un futur lointain
    for k, i in enumerate(indices[curseur:curseur + 3]):
        lignes[i][1] = ["12/05/2035", "2041.11.03", "7-févr-38"][k]
    curseur += 3

    # 5. deux lignes entierement vides, inserees a des positions fixes
    lignes.insert(137, [""] * len(ENTETES))
    lignes.insert(298, [""] * len(ENTETES))

    chemin = core.dossier_sortie() + "/ventes_brutes.csv"
    # Ecriture manuelle : pas de guillemets, separateur point-virgule,
    # UTF-8 SANS BOM pour que le mojibake soit authentique dans Excel FR.
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(";".join(ENTETES) + "\r\n")
        for ligne in lignes:
            f.write(";".join(ligne) + "\r\n")

    print("  ecrit : ventes_brutes.csv (%d lignes de donnees)" % len(lignes))


if __name__ == "__main__":
    main()
