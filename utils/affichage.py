from turtle import mode
from Requirement.fltk import *
from utils.constantes import *
from utils.outils import *
from utils.lecture_csv import *
from utils.donnees import associer_numero_nom_departements

def determiner_remplissage(donnees, code_dep, stats):
    if code_dep not in donnees:
        return "grey"

    valeur = donnees[code_dep]

    if code_dep in DEPARTEMENTS_OUTRE_MER:
        borne_min, borne_max = stats['dom']
    else:
        borne_min, borne_max = stats['metro']

    valeur_norm = convertir(valeur, borne_max, borne_min)
    valeur_norm = max(0, min(1, valeur_norm))

    (r0, g0, b0) = stats["couleur_min"]
    (r1, g1, b1) = stats["couleur_max"]

    r = int(r0 + (r1 - r0) * valeur_norm)
    g = int(g0 + (g1 - g0) * valeur_norm)
    b = int(b0 + (b1 - b0) * valeur_norm)

    return rgb_to_hex(r, g, b)

def dessiner_metropole(formes_metro, donnees, stats, params):
    for forme, code in formes_metro:
        points = forme.points
        parties = list(forme.parts) + [len(points)]
        couleur = determiner_remplissage(donnees, code, stats)
        
        for i in range(len(forme.parts)):
            poly_pts = []
            for p in points[parties[i]:parties[i+1]]:
                xm, ym = convert_to_mercator((p[0], p[1]))
                
                x = (xm - params['centre_geo_x']) * params['echelle'] + params['centre_ecran_x']
                y = -(ym - params['centre_geo_y']) * params['echelle'] + params['centre_ecran_y']
                poly_pts.append((x, y))
            
            polygone(tuple(poly_pts), couleur="black", remplissage=couleur, tag=str(code))

def dessiner_dom(formes_dom, donnees, stats, params_dom):
    for forme, code in formes_dom:
        if code not in params_dom: continue
        
        p_data = params_dom[code]
        points = forme.points
        parties = list(forme.parts) + [len(points)]
        couleur = determiner_remplissage(donnees, code, stats)
        
        for i in range(len(forme.parts)):
            poly_pts = []
            for p in points[parties[i]:parties[i+1]]:
                xm, ym = convert_to_mercator((p[0], p[1]))
                
                x = (xm - p_data['centre_geo_x']) * p_data['echelle'] + p_data['centre_ecran_x']
                y = -(ym - p_data['centre_geo_y']) * p_data['echelle'] + p_data['centre_ecran_y']
                poly_pts.append((x, y))
            
            polygone(tuple(poly_pts), couleur="black", remplissage=couleur, tag=str(code))

def dessiner_ile_de_france(forme_idf, donnees, stats, params_idf):
    for forme, code in forme_idf:
        points = forme.points
        parties = list(forme.parts) + [len(points)]
        couleur = determiner_remplissage(donnees, code, stats)
        
        for i in range(len(forme.parts)):
            poly_pts = []
            for p in points[parties[i]:parties[i+1]]:
                xm, ym = convert_to_mercator((p[0], p[1]))
                
                x = (xm - params_idf['centre_geo_x']) * params_idf['echelle'] + params_idf['centre_ecran_x']
                y = -(ym - params_idf['centre_geo_y']) * params_idf['echelle'] + params_idf['centre_ecran_y']
                poly_pts.append((x, y))
            
            polygone(tuple(poly_pts), couleur="black", remplissage=couleur, tag=str(code))

def dessiner_centroides(chefs_lieux, params_metro, params_dom, params_idf):

    for code_dep, data in chefs_lieux.items():
        try:
            lat = float(data['lat'])
            lon = float(data['lon'])
        except Exception:
            continue 

        xm, ym = convert_to_mercator((lon, lat))

        if code_dep in params_dom:
            params = params_dom[code_dep]
        elif code_dep in DEPARTEMENTS_ILE_DE_FRANCE:
            params = params_idf
        else:
            params = params_metro

        x = (xm - params['centre_geo_x']) * params['echelle'] + params['centre_ecran_x']
        y = -(ym - params['centre_geo_y']) * params['echelle'] + params['centre_ecran_y']

        image(x,y,"image/mairi.png",largeur=20, hauteur=15,tag="prefecture")

def dessiner_legende(donnees, stats, marge=10, largeur_case=100, hauteur_legende=20, espacement=8):
    y1 = marge
    y2 = marge + hauteur_legende
    nb_cases = 5

    for i in range(nb_cases):
        x1 = (LARGEUR_FENETRE//2 - (nb_cases * (largeur_case + espacement))//2) + i * (largeur_case + espacement)
        x2 = x1 + largeur_case

        couleur_case = determiner_remplissage_legende(donnees, i, nb_cases, stats)

        # pourcentage affiché : calcul approximatif linéaire
        mini = key_of_min(donnees)
        maxi = key_of_max(donnees)
        valeur = mini + (maxi - mini) * (i / (nb_cases - 1))
        pourcentage = valeur * 100
        tag = f"{pourcentage:.1f}%"

        rectangle(x1, y1, x2, y2,
                  couleur="black",
                  remplissage=couleur_case,
                  epaisseur=1,
                  tag=tag)


def determiner_remplissage_legende(donnees, index_case, nb_cases, stats):
    
    if nb_cases > 1:
        t = index_case / (nb_cases - 1)
    else:
        t = 0

    r0, g0, b0 = stats["couleur_max"] 
    r1, g1, b1 = stats["couleur_min"]

    r = int(r0 + (r1 - r0) * t)
    g = int(g0 + (g1 - g0) * t)
    b = int(b0 + (b1 - b0) * t)

    return rgb_to_hex(r, g, b)

def determiner_tag_legende(donnees, valeur, nb_cases):

    valeur = valeur / (nb_cases)

    mini = key_of_min(donnees)
    maxi = key_of_max(donnees)

    valeur_norm = convertir(valeur, maxi, mini)
    valeur_norm = max(0, min(1, valeur_norm))

    pourcentage = (1 - valeur_norm) * 100
    
    return "{:.1f}%".format(pourcentage)


def dessiner_survol(donnees, code_survole, mode):
    x = abscisse_souris()
    y = ordonnee_souris()

    nom_departement = associer_numero_nom_departements().get(code_survole, 'Inconnu')

    TAILLE_RECTANGLE = 220 + (len(nom_departement) * 7)

    if x + TAILLE_RECTANGLE > LARGEUR_FENETRE:
        x = LARGEUR_FENETRE - TAILLE_RECTANGLE - 5
    if y - 40 < 0:
            y = 45
                
    rectangle(x + 5, y - 40, x + TAILLE_RECTANGLE, y,
        couleur="black",
        remplissage="white",
        tag="info")
    
    
    
    if "%" in code_survole:
        valeur = code_survole
        texte(x + 15, y - 15,
            f"Proportion de {mode} : {valeur}",
            couleur="black",
            taille=12,
            tag="info",
            ancrage="sw")
    elif code_survole is not None:
        valeur = donnees[code_survole] * 100
        texte(x + 15, y - 15,
            f" {nom_departement} ({code_survole}) | {mode} : {valeur:.2f}%",
            couleur="black",
            taille=12,
            tag="info",
            ancrage="sw")

def dessiner_contexte(liste_mode, code_departement, donnees_csv):
    efface("contexte")
    x1 = 10
    x2 = 215
    y1 = 10
    y2 = 255

    dico_inscrits_votants = lire_inscrits_votants(CHEMIN_CSV)
    noms_departements = associer_numero_nom_departements()
    nom_commune = CHEFS_LIEUX.get(code_departement, {}).get('commune', 'Inconnu')
        
    texte((x1 + x2)//2, y1 + 20,
        f"{noms_departements.get(code_departement, code_departement)} ({code_departement})",
        couleur="black",
        taille=12,
        tag="contexte",
        ancrage="n")

    texte((x1 + x2)//2, y1 + 50,
        f"{nom_commune}",
        couleur="black",
        taille=12,
        tag="contexte",
        ancrage="n")

    for i, m in enumerate(liste_mode):
        valeur_m = donnees_csv[m].get(code_departement, 0) * 100
        texte((x1 + x2)//2, y1 + 85 + i * 30,
            f"{m} : {valeur_m:.2f}%",
            couleur="black",
            taille=12,
            tag="contexte",
            ancrage="n")

    rectangle(x1, y1, x2, y2,
              couleur="black",
              remplissage="",
              epaisseur=2,
              tag="contexte")
    
    texte((x1 + x2)//2, y2 - 60,
        f"Inscrits : {dico_inscrits_votants['inscrits'].get(code_departement, 0)}",
        couleur="black",
        taille=12,
        tag="contexte",
        ancrage="n")
    
    texte((x1 + x2)//2, y2 - 30,
        f"Votants : {dico_inscrits_votants['votants'].get(code_departement, 0)}",
        couleur="black",
        taille=12,
        tag="contexte",
        ancrage="n")



def dessiner_titre(modes):

    if modes == "abstention":
        texte(500, 950,"CARTE DE FRANCE DU POURCENTAGE D'ABSTENTION" , police="Inter ExtraBold",couleur="black", taille=15, tag="titre", ancrage="s")
    elif modes == "blancs":
        texte(500, 950,"CARTE DE FRANCE DU POURCENTAGE DE VOTE BLANC" , police="Inter ExtraBold",couleur="black", taille=15, tag="titre", ancrage="s")
    elif modes == "nuls":
        texte(500, 950,"CARTE DE FRANCE DU POURCENTAGE DE VOTE NUL" , police="Inter ExtraBold",couleur="black", taille=15, tag="titre", ancrage="s")
