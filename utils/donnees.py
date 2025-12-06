# donnees.py
from shapefile import Reader
from utils.constantes import *
from utils.outils import convert_to_mercator, key_of_min, key_of_max

def separer_formes_geo():
    sf = Reader("donner/departements_20180101")
    formes = sf.shapes()
    records = sf.records()
    
    metro = []
    dom = []
    
    for forme, record in zip(formes, records):
        code = record[0]
        if code in DEPARTEMENTS_METRO:
            metro.append((forme, code))
        elif code in DEPARTEMENTS_OUTRE_MER:
            dom.append((forme, code))
            
    return metro, dom

def calculer_stats_couleurs(donnees):
    d_metro = {k: v for k, v in donnees.items() if k not in DEPARTEMENTS_OUTRE_MER}
    d_dom = {k: v for k, v in donnees.items() if k in DEPARTEMENTS_OUTRE_MER}

    stats = {
        'metro': (key_of_min(d_metro) if d_metro else 0, key_of_max(d_metro) if d_metro else 1),
        'dom': (key_of_min(d_dom) if d_dom else 0, key_of_max(d_dom) if d_dom else 1)
    }
    return stats

def calculer_params_metropole(formes_metro):
    tous_points = [p for f, c in formes_metro for p in f.points]
    
    min_lon = min(p[0] for p in tous_points)
    max_lon = max(p[0] for p in tous_points)
    min_lat = min(p[1] for p in tous_points)
    max_lat = max(p[1] for p in tous_points)

    min_m = convert_to_mercator((min_lon, min_lat))
    max_m = convert_to_mercator((max_lon, max_lat))

    largeur = max_m[0] - min_m[0]
    hauteur = max_m[1] - min_m[1]

    echelle = min(LARGEUR_FENETRE / largeur, HAUTEUR_FENETRE / hauteur) * 0.9
    
    return {
        'echelle': echelle,
        'centre_geo_x': (min_m[0] + max_m[0]) / 2,
        'centre_geo_y': (min_m[1] + max_m[1]) / 2,
        'centre_ecran_x': LARGEUR_FENETRE / 2,
        'centre_ecran_y': HAUTEUR_FENETRE / 2
    }

def calculer_params_dom(formes_dom):
    l_encart = LARGEUR_FENETRE * CONF_DOM["ratio_taille"]
    h_encart = HAUTEUR_FENETRE * CONF_DOM["ratio_taille"]
    
    coin_x = CONF_DOM["marge"] + CONF_DOM["offset_x"]
    coin_y = HAUTEUR_FENETRE - h_encart - CONF_DOM["marge"] + CONF_DOM["offset_y"]
    
    nb_dom = len(DEPARTEMENTS_OUTRE_MER)
    h_par_dom = h_encart / nb_dom + 10 if nb_dom > 0 else 1
    
    params_dom = {}
    pos_y_actuelle = coin_y
    
    codes_tries = sorted(DEPARTEMENTS_OUTRE_MER)
    
    for code in codes_tries:
        forme = next((f for f, c in formes_dom if c == code), None)
        if not forme: continue
        
        points = forme.points
        min_lon = min(p[0] for p in points)
        max_lon = max(p[0] for p in points)
        min_lat = min(p[1] for p in points)
        max_lat = max(p[1] for p in points)
        
        min_m = convert_to_mercator((min_lon, min_lat))
        max_m = convert_to_mercator((max_lon, max_lat))
        
        larg = max_m[0] - min_m[0]
        haut = max_m[1] - min_m[1]
        
        ech_x = l_encart / larg if larg > 0 else 1
        ech_y = h_par_dom / haut if haut > 0 else 1
        
        params_dom[code] = {
            'echelle': min(ech_x, ech_y) * 0.9,
            'centre_geo_x': (min_m[0] + max_m[0]) / 2,
            'centre_geo_y': (min_m[1] + max_m[1]) / 2,
            'centre_ecran_x': coin_x + l_encart / 2,
            'centre_ecran_y': pos_y_actuelle + h_par_dom / 2
        }
        pos_y_actuelle += h_par_dom
        
    return params_dom