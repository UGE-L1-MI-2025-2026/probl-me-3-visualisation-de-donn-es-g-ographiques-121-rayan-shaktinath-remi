from Requirement.fltk import *
from utils.constantes import DEPARTEMENTS_OUTRE_MER , LARGEUR_FENETRE, HAUTEUR_FENETRE, RED, GREEN, BLUE
from utils.outils import convertir, rgb_to_hex, convert_to_mercator, key_of_min, key_of_max

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

    return rgb_to_hex(int(RED * valeur_norm), int(GREEN * valeur_norm), int(BLUE))

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


def dessiner_legende(donnees,
    marge=10,
    largeur_case=100,
    hauteur_legende=20,
    espacement=8,
    couleur_case="#444",
):

    y1 = marge
    y2 = marge + hauteur_legende

    nb_cases = 5

    for i in range(nb_cases):
        x1 = (LARGEUR_FENETRE//2 - (nb_cases * (largeur_case + espacement))//2) + i * (largeur_case + espacement)
        x2 = x1 + largeur_case
        couleur_case = determiner_remplissage_legende(donnees, i, nb_cases)
        rectangle(x1, y1, x2, y2,
                  couleur="black",
                  remplissage=couleur_case,
                  epaisseur=1)


def determiner_remplissage_legende(donnees, valeur, nb_cases):

    valeur = valeur / (nb_cases)

    mini = key_of_min(donnees)
    maxi = key_of_max(donnees)

    valeur_norm = convertir(valeur, maxi, mini)
    valeur_norm = max(0, min(1, valeur_norm))

    return rgb_to_hex(int(RED * valeur_norm), int(GREEN * valeur_norm), int(BLUE))