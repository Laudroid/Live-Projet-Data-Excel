# -*- coding: utf-8 -*-
"""Univers metier partage par tous les jeux de donnees de la formation.

Entreprise fictive : ATELIER NORDIQUE, distributeur retail francais
d'equipement de bureau et de petit electromenager.
"""

SEED = 20260905

REGIONS = ["Nord", "Sud", "Est", "Ouest", "Ile-de-France", "Centre"]
REGIONS_ACC = {
    "Nord": "Nord",
    "Sud": "Sud",
    "Est": "Est",
    "Ouest": "Ouest",
    "Ile-de-France": "Île-de-France",
    "Centre": "Centre",
}

# ---------------------------------------------------------------- magasins
# (id, nom, ville, region)
MAGASINS = [
    ("MAG01", "Atelier Lille Grand Place", "Lille", "Nord"),
    ("MAG02", "Atelier Amiens Rivery", "Amiens", "Nord"),
    ("MAG03", "Atelier Marseille Prado", "Marseille", "Sud"),
    ("MAG04", "Atelier Toulouse Capitole", "Toulouse", "Sud"),
    ("MAG05", "Atelier Strasbourg Krutenau", "Strasbourg", "Est"),
    ("MAG06", "Atelier Dijon Darcy", "Dijon", "Est"),
    ("MAG07", "Atelier Nantes Graslin", "Nantes", "Ouest"),
    ("MAG08", "Atelier Rennes Sainte-Anne", "Rennes", "Ouest"),
    ("MAG09", "Atelier Paris Reaumur", "Paris", "Ile-de-France"),
    ("MAG10", "Atelier Creteil Soleil", "Creteil", "Ile-de-France"),
    ("MAG11", "Atelier Orleans Martroi", "Orleans", "Centre"),
    ("MAG12", "Atelier Tours Nationale", "Tours", "Centre"),
]

MAGASINS_ACC = {
    "MAG01": ("Atelier Lille Grand Place", "Lille"),
    "MAG02": ("Atelier Amiens Rivery", "Amiens"),
    "MAG03": ("Atelier Marseille Prado", "Marseille"),
    "MAG04": ("Atelier Toulouse Capitole", "Toulouse"),
    "MAG05": ("Atelier Strasbourg Krutenau", "Strasbourg"),
    "MAG06": ("Atelier Dijon Darcy", "Dijon"),
    "MAG07": ("Atelier Nantes Graslin", "Nantes"),
    "MAG08": ("Atelier Rennes Sainte-Anne", "Rennes"),
    "MAG09": ("Atelier Paris Réaumur", "Paris"),
    "MAG10": ("Atelier Créteil Soleil", "Créteil"),
    "MAG11": ("Atelier Orléans Martroi", "Orléans"),
    "MAG12": ("Atelier Tours Nationale", "Tours"),
}

# ---------------------------------------------------------------- produits
# (id, nom, categorie, prix_vente, cout_achat)
PRODUITS = [
    # Electronique -- pic en novembre/decembre
    ("P001", "Casque Bluetooth Aria", "Électronique", 89.90, 51.30),
    ("P002", "Enceinte nomade Volta", "Électronique", 129.00, 74.80),
    ("P003", "Écran 27 pouces Lumen", "Électronique", 329.00, 214.00),
    ("P004", "Clavier mécanique Frappe", "Électronique", 119.50, 68.90),
    ("P005", "Souris ergonomique Galet", "Électronique", 49.90, 26.40),
    ("P006", "Webcam HD Regard", "Électronique", 79.00, 44.20),
    ("P007", "Disque SSD 1 To Silex", "Électronique", 109.00, 72.10),
    ("P008", "Chargeur USB-C Foudre", "Électronique", 34.90, 16.80),
    # Mobilier -- panier eleve, volumes faibles
    ("P101", "Chaise de bureau Assise", "Mobilier", 249.00, 158.00),
    ("P102", "Bureau réglable Altitude", "Mobilier", 549.00, 371.00),
    ("P103", "Caisson à roulettes Tiroir", "Mobilier", 179.00, 112.00),
    ("P104", "Lampe d'architecte Faisceau", "Mobilier", 94.50, 52.00),
    ("P105", "Étagère modulaire Strate", "Mobilier", 139.00, 86.50),
    ("P106", "Fauteuil visiteur Accueil", "Mobilier", 189.00, 121.00),
    # Papeterie -- pic de rentree (aout/septembre)
    ("P201", "Carnet A5 Feuillet", "Papeterie", 6.90, 2.80),
    ("P202", "Stylo roller Encre", "Papeterie", 4.50, 1.60),
    ("P203", "Ramette A4 Blancheur", "Papeterie", 8.90, 5.20),
    ("P204", "Classeur à levier Dossier", "Papeterie", 5.40, 2.10),
    ("P205", "Bloc-notes adhésif Repère", "Papeterie", 3.90, 1.40),
    ("P206", "Marqueur effaçable Ardoise", "Papeterie", 2.80, 0.95),
    ("P207", "Agrafeuse Attache", "Papeterie", 14.90, 7.30),
    # Electromenager -- pic estival (ventilateur) et hivernal (bouilloire)
    ("P301", "Bouilloire Vapeur", "Électroménager", 44.90, 24.60),
    ("P302", "Machine à café Arôme", "Électroménager", 219.00, 143.00),
    ("P303", "Micro-ondes Onde", "Électroménager", 149.00, 98.50),
    ("P304", "Réfrigérateur d'appoint Fraîcheur", "Électroménager", 279.00, 191.00),
    ("P305", "Ventilateur colonne Brise", "Électroménager", 89.00, 47.50),
    ("P306", "Aspirateur balai Souffle", "Électroménager", 199.00, 128.00),
    # Telephonie -- pic en decembre
    ("P401", "Smartphone Signal", "Téléphonie", 449.00, 331.00),
    ("P402", "Coque renforcée Carapace", "Téléphonie", 24.90, 8.40),
    ("P403", "Batterie externe Réserve", "Téléphonie", 39.90, 19.70),
    ("P404", "Casque filaire Fil", "Téléphonie", 19.90, 8.90),
    ("P405", "Support voiture Cardan", "Téléphonie", 29.90, 12.60),
    ("P406", "Câble tressé Lien", "Téléphonie", 14.90, 5.10),
]

CATEGORIES = ["Électronique", "Mobilier", "Papeterie", "Électroménager", "Téléphonie"]

# Poids de saisonnalite par categorie, index 0 = janvier
SAISON = {
    "Électronique":   [0.85, 0.80, 0.90, 0.90, 0.95, 0.90, 0.85, 0.90, 1.05, 1.10, 1.35, 1.55],
    "Mobilier":       [0.95, 0.90, 1.05, 1.05, 1.00, 0.90, 0.70, 0.95, 1.30, 1.20, 1.05, 0.85],
    "Papeterie":      [0.85, 0.80, 0.90, 0.85, 0.85, 0.75, 0.80, 1.45, 1.60, 1.05, 0.95, 0.85],
    "Électroménager": [0.90, 0.85, 0.90, 0.95, 1.10, 1.35, 1.45, 1.20, 0.95, 0.85, 0.90, 1.10],
    "Téléphonie":     [0.90, 0.85, 0.90, 0.95, 0.95, 0.95, 0.90, 0.95, 1.05, 1.05, 1.25, 1.50],
}

# Coefficient de poids commercial par region (part de marche interne)
POIDS_REGION = {
    "Nord": 1.00,
    "Sud": 1.15,
    "Est": 0.80,
    "Ouest": 0.95,
    "Ile-de-France": 1.45,
    "Centre": 0.70,
}

# Amplitude de saisonnalite propre a la region : le Sud est le plus
# saisonnier (tourisme estival), l'Ile-de-France le plus stable.
AMPLITUDE_REGION = {
    "Nord": 1.00,
    "Sud": 1.60,
    "Est": 1.05,
    "Ouest": 1.10,
    "Ile-de-France": 0.55,
    "Centre": 0.90,
}

# ---------------------------------------------------------------- vendeurs
# (nom, region de rattachement, indice de performance, volume relatif)
# Les deux derniers sont des vendeurs saisonniers a tres faible volume :
# ils servent a rendre la clause HAVING du TP QUERY non triviale.
VENDEURS = [
    ("Camille Fournier", "Ile-de-France", 1.25, 1.00),
    ("Hugo Marchand", "Ile-de-France", 1.05, 0.95),
    ("Léa Bonnet", "Sud", 1.20, 1.00),
    ("Samir Haddad", "Sud", 0.95, 0.90),
    ("Nora Lefèvre", "Nord", 1.10, 1.00),
    ("Thomas Girard", "Nord", 0.85, 0.95),
    ("Inès Moreau", "Ouest", 1.15, 0.95),
    ("Yanis Perrot", "Est", 0.90, 0.90),
    ("Claire Vasseur", "Centre", 1.00, 0.85),
    ("Malik Benali", "Ouest", 0.95, 0.90),
    ("Sofia Renard", "Centre", 0.80, 0.06),
    ("Bastien Roux", "Est", 0.75, 0.05),
]

VENDEURS_FAIBLE_VOLUME = ["Sofia Renard", "Bastien Roux"]

# ---------------------------------------------------------------- clients
PRENOMS = [
    "Camille", "Hugo", "Léa", "Samir", "Nora", "Thomas", "Inès", "Yanis",
    "Claire", "Malik", "Sofia", "Bastien", "Amandine", "Karim", "Élodie",
    "Julien", "Fatima", "Grégoire", "Chloé", "Idriss", "Marion", "Océane",
    "Pierre-Yves", "Sarah", "Vincent", "Naïma", "Étienne", "Lucie",
    "Mehdi", "Anaïs",
]

NOMS = [
    "Dupont", "Lefebvre", "Moreau", "Garnier", "Chevalier", "Rousseau",
    "Blanchard", "Mercier", "Dumas", "Faure", "Guérin", "Leroy",
    "Marchal", "Nguyen", "Ollivier", "Pichon", "Quintin", "Renaud",
    "Sabatier", "Thibault", "Vaillant", "Weber", "Ziani", "Aubert",
    "Bertrand", "Caron", "Delaunay", "Estève", "Fontaine", "Gaillard",
    "Hébert", "Imbert", "Jacquet", "Klein", "Lambert", "Masson",
    "Noël", "Ozanne", "Perrier", "Riviere",
]

# Villes de facturation : plusieurs noms composes pour que l'extraction
# naive par =DROITE() echoue et impose TEXTEAPRES / STXT.
VILLES_CP = [
    ("59000", "Lille"),
    ("59100", "Roubaix"),
    ("80000", "Amiens"),
    ("13008", "Marseille"),
    ("13100", "Aix-en-Provence"),
    ("31000", "Toulouse"),
    ("67000", "Strasbourg"),
    ("21000", "Dijon"),
    ("44000", "Nantes"),
    ("35000", "Rennes"),
    ("75002", "Paris"),
    ("75011", "Paris"),
    ("94000", "Créteil"),
    ("92100", "Boulogne-Billancourt"),
    ("45000", "Orléans"),
    ("37000", "Tours"),
    ("76600", "Le Havre"),
    ("42000", "Saint-Étienne"),
    ("69003", "Lyon"),
    ("33000", "Bordeaux"),
    ("29200", "Brest"),
    ("87000", "Limoges"),
    ("57000", "Metz"),
    ("64000", "Pau"),
    ("14000", "Caen"),
]

RUES = [
    "rue des Lilas", "avenue Jean Jaurès", "boulevard de la Liberté",
    "place du Marché", "impasse des Tilleuls", "chemin du Moulin",
    "rue Victor Hugo", "allée des Peupliers", "quai de la Gare",
    "rue de l'Église", "cours Mirabeau", "route de Bretagne",
]

SEGMENTS = ["Grand compte", "PME", "TPE", "Administration", "Particulier"]

MODES_PAIEMENT = ["Carte bancaire", "Virement", "Prélèvement", "Chèque", "Espèces"]

DOMAINES_MAIL = [
    "example.com", "mail-test.fr", "societe-demo.fr", "atelier-nordique.fr",
    "courriel-demo.net",
]


def produits_par_id():
    return {p[0]: p for p in PRODUITS}


def magasins_par_id():
    return {m[0]: m for m in MAGASINS}


def produits_de_categorie(cat):
    return [p for p in PRODUITS if p[2] == cat]
