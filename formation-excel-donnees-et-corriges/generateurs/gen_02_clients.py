# -*- coding: utf-8 -*-
"""clients_brut.xlsx -- extraction CRM degradee.

Sert a l'enonce : Serie A / exercice 2 -- Nettoyer un dataset complet.

Anomalies injectees :
  1. colonne Nom : casse heterogene, espaces en debut/fin, espaces doubles
  2. colonne Adresse : code postal et ville concatenes, avec des villes
     composees (Aix-en-Provence, Boulogne-Billancourt, Le Havre) pour que
     l'extraction naive par =DROITE() echoue
  3. doublons : 15 au total. 8 sont injectes comme doublons "masques"
     (meme personne, meme email, orthographe du nom differente) et 7
     comme doublons stricts. A la mesure, 8 lignes ressortent d'une
     detection sur les colonnes BRUTES et 7 n'apparaissent qu'apres
     normalisation du nom : l'une des variantes "masquees" a tire par
     hasard la meme forme que son original. Les valeurs de reference
     recalculees dans corriges/valeurs-de-reference.md sont la source de
     verite, pas ces intentions de calibrage.
  4. colonne Telephone : cellules vides, cinq formats concurrents,
     zero initial perdu
"""

import datetime as dt
import unicodedata

import gen_core as core
import referentiel as ref


def sans_accent(texte):
    decompose = unicodedata.normalize("NFKD", texte)
    return "".join(c for c in decompose if not unicodedata.combining(c))


def email_de(prenom, nom, domaine):
    base = "%s.%s" % (sans_accent(prenom).lower().replace(" ", "-"),
                      sans_accent(nom).lower().replace(" ", "-"))
    return "%s@%s" % (base.replace("'", ""), domaine)


def nom_sali(rng, prenom, nom, variante=None):
    """Retourne le nom tel qu'il a ete saisi dans le CRM."""
    forme = variante if variante is not None else rng.random()
    complet = "%s %s" % (nom, prenom)
    if forme < 0.20:
        return complet.upper()
    if forme < 0.38:
        return "  %s  %s " % (nom.lower(), prenom.lower())
    if forme < 0.52:
        return "%s %s " % (nom.upper(), prenom)
    if forme < 0.66:
        return " %s %s" % (nom.lower(), prenom.upper())
    if forme < 0.80:
        return "%s  %s" % (nom, prenom)
    return complet


def telephone(rng, index):
    numero = "0%d%02d%02d%02d%02d" % (
        rng.choice([1, 2, 3, 4, 5, 6, 6, 7, 7]),
        rng.randint(0, 99), rng.randint(0, 99),
        rng.randint(0, 99), rng.randint(0, 99))
    tirage = rng.random()
    if tirage < 0.09:
        return ""
    if tirage < 0.13:
        return "non renseigné"
    if tirage < 0.45:
        return numero
    if tirage < 0.66:
        return "%s %s %s %s %s" % (numero[0:2], numero[2:4], numero[4:6],
                                   numero[6:8], numero[8:10])
    if tirage < 0.80:
        return "%s.%s.%s.%s.%s" % (numero[0:2], numero[2:4], numero[4:6],
                                   numero[6:8], numero[8:10])
    if tirage < 0.92:
        return "+33 %s" % numero[1:]
    # zero initial perdu a l'export : la valeur est numerique
    return int(numero)


def main():
    rng = core.rng_pour("clients_brut")

    base = []
    utilises = set()
    while len(base) < 180:
        prenom = rng.choice(ref.PRENOMS)
        nom = rng.choice(ref.NOMS)
        if (prenom, nom) in utilises:
            continue
        utilises.add((prenom, nom))
        cp, ville = rng.choice(ref.VILLES_CP)
        base.append({
            "prenom": prenom,
            "nom": nom,
            "email": email_de(prenom, nom, rng.choice(ref.DOMAINES_MAIL)),
            "rue": "%d %s" % (rng.randint(1, 148), rng.choice(ref.RUES)),
            "adresse": "%s %s" % (cp, ville),
            "segment": rng.choice(ref.SEGMENTS),
            "date": dt.date(rng.randint(2019, 2024), rng.randint(1, 12),
                            rng.randint(1, 28)),
            "ca": round(rng.uniform(120, 24000), 2),
        })

    lignes = []
    for personne in base:
        lignes.append({
            "nom_saisi": nom_sali(rng, personne["prenom"], personne["nom"]),
            "source": personne,
            "tel": telephone(rng, 0),
        })

    # --- doublons masques : meme email, orthographe du nom differente
    indices_masques = rng.sample(range(len(base)), 8)
    for i in indices_masques:
        personne = base[i]
        lignes.append({
            "nom_saisi": nom_sali(rng, personne["prenom"], personne["nom"],
                                  variante=0.30),
            "source": dict(personne, segment=rng.choice(ref.SEGMENTS)),
            "tel": telephone(rng, 0),
        })

    # --- doublons stricts : ligne recopiee a l'identique sauf identifiant
    candidats = [i for i in range(len(base)) if i not in indices_masques]
    for i in rng.sample(candidats, 7):
        original = lignes[i]
        lignes.append({
            "nom_saisi": original["nom_saisi"],
            "source": original["source"],
            "tel": original["tel"],
        })

    rng.shuffle(lignes)

    donnees = []
    for i, ligne in enumerate(lignes, start=1):
        p = ligne["source"]
        donnees.append([
            "CLI%04d" % i,
            ligne["nom_saisi"],
            p["email"],
            p["rue"],
            p["adresse"],
            ligne["tel"],
            p["segment"],
            p["date"],
            p["ca"],
        ])

    wb = core.nouveau_classeur("Clients")
    core.ecrire_feuille(
        wb["Clients"],
        ["ID_Client", "Nom", "Email", "Rue", "Adresse", "Telephone",
         "Segment", "Date_Creation", "CA_Cumule"],
        donnees,
        formats={8: "DD/MM/YYYY", 9: "# ##0.00"},
        largeurs={1: 12, 2: 26, 3: 34, 4: 28, 5: 26, 6: 18, 7: 16, 8: 15,
                  9: 14},
        nom_tableau="Clients",
    )
    core.enregistrer(wb, "clients_brut.xlsx")
    print("     %d lignes dont 15 doublons (8 masques, 7 stricts)"
          % len(donnees))


if __name__ == "__main__":
    main()
