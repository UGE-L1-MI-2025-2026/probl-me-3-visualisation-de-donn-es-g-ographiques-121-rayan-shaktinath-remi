from shapefile import *
from Requirement.fltk import *
from math import *
from lecture_csv import *
from matplotlib import *

LARGEUR_FENETRE = 1000
HAUTEUR_FENETRE = 1000
cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

shapefile_france = Reader("departements_20180101")

CHEMIN_FICHIER = "resultats-definitifs-par-departements.csv" 
donnees = lire_abstentions(CHEMIN_FICHIER)
#donnees = {'01': 0, '02': 0.36, '03': 0.3122, '04': 0.2989, '05': 0.2822, '06': 0.3358, '07': 0.28190000000000004, '08': 0.3475, '09': 0.2942, '10': 0.3265, '11': 0.3, '12': 0.2633, '13': 0.335, '14': 0.2945, '15': 0.2807, '16': 0.3135, '17': 0.3024, '18': 0.33899999999999997, '19': 0.2688, '21': 0.2902, '22': 0.2585, '23': 0.2937, '24': 0.28190000000000004, '25': 0.3046, '26': 0.2932, '27': 0.326, '28': 0.33990000000000004, '29': 0.26649999999999996, '2A': 0.3611, '2B': 0.35609999999999997, '30': 0.31370000000000003, '31': 0.272, '32': 0.2615, '33': 0.2927, '34': 0.3072, '35': 0.2643, '36': 0.3196, '37': 0.3072, '38': 0.2897, '39': 0.2925, '40': 0.2802, '41': 0.316, '42': 0.30879999999999996, '43': 0.2755, '44': 0.2858, '45': 0.32549999999999996, '46': 0.2611, '47': 0.2995, '48': 0.24960000000000002, '49': 0.30269999999999997, '50': 0.3062, '51': 0.3396, '52': 0.3397, '53': 0.31620000000000004, '54': 0.34729999999999994, '55': 0.33270000000000005, '56': 0.2728, '57': 0.3747, '58': 0.3307, '59': 0.3586, '60': 0.3427, '61': 0.3143, '62': 0.3521, '63': 0.2894, '64': 0.2809, '65': 0.29309999999999997, '66': 0.32159999999999994, '67': 0.3274, '68': 0.34729999999999994, '69': 0.28350000000000003, '70': 0.29510000000000003, '71': 0.31120000000000003, '72': 0.33380000000000004, '73': 0.2888, '74': 0.3123, '75': 0.26739999999999997, '76': 0.3233, '77': 0.34869999999999995, '78': 0.29460000000000003, '79': 0.306, '80': 0.32189999999999996, '81': 0.2824, '82': 0.2932, '83': 0.3308, '84': 0.3243, '85': 0.2986, '86': 0.3037, '87': 0.2768, '88': 0.32030000000000003, '89': 0.3275, '90': 0.3081, '91': 0.3274, '92': 0.2749, '93': 0.9, '94': 0.32020000000000004, '95': 0.3515,}


DEPARTEMENTS_METRO = {
    *[f"{i:02d}" for i in range(1, 96)],  
    "2A", "2B","69D","69M"                                 
}

def convert_to_mercator(coords):
    R = 6378137.0
    lon = coords[0]
    lat = coords[1]  
    
    x = R * radians(lon)
    y = R * log(tan(pi/4.0 + radians(lat)/2.0))
    return (x, y)

formes_metro_avec_code = []
formes = shapefile_france.shapes()
enregistrements = shapefile_france.records()

for forme, enregistrement in zip(formes, enregistrements):
    code_dept = enregistrement[0]
    if code_dept in DEPARTEMENTS_METRO:
        formes_metro_avec_code.append((forme, code_dept))

def rgb_to_hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

formes_metro_seules = [item[0] for item in formes_metro_avec_code]

if formes_metro_seules:
    min_lat = min(min(pt[0] for pt in forme.points) for forme in formes_metro_seules)
    max_lat = max(max(pt[0] for pt in forme.points) for forme in formes_metro_seules)
    min_lon = min(min(pt[1] for pt in forme.points) for forme in formes_metro_seules)
    max_lon = max(max(pt[1] for pt in forme.points) for forme in formes_metro_seules)

    min_merc = convert_to_mercator((min_lat, min_lon))
    max_merc = convert_to_mercator((max_lat, max_lon))

    min_x_merc = min_merc[0]
    min_y_merc = min_merc[1]
    max_x_merc = max_merc[0]
    max_y_merc = max_merc[1]

    largeur_donnees = max_x_merc - min_x_merc
    hauteur_donnees = max_y_merc - min_y_merc

    echelle_x = LARGEUR_FENETRE / largeur_donnees
    echelle_y = HAUTEUR_FENETRE / hauteur_donnees
    ECHELLE = min(echelle_x, echelle_y) * 0.9  

    centre_geo_x = (min_x_merc + max_x_merc) / 2
    centre_geo_y = (min_y_merc + max_y_merc) / 2

    CENTRE_ECRAN_X = LARGEUR_FENETRE / 2
    CENTRE_ECRAN_Y = HAUTEUR_FENETRE / 2
else:
    ECHELLE = 1
    centre_geo_x = 0
    centre_geo_y = 0
    CENTRE_ECRAN_X = LARGEUR_FENETRE / 2
    CENTRE_ECRAN_Y = HAUTEUR_FENETRE / 2


def key_of_max(d):
    clee = max(d, key = d.get)
    return d[clee]

def key_of_min(d):
    clee = min(d, key = d.get)
    return d[clee]

def convertir(value, inf, sup):
    norm = (value - inf) / (sup - inf)
    return norm

def determiner_remplissage(donnees, code_dep):
    if code_dep not in donnees:
        return "grey"

    valeur_mini = key_of_min(donnees)
    valeur_max = key_of_max(donnees)
    valeur = convertir(donnees[code_dep],valeur_max,valeur_mini)
    

    return rgb_to_hex(int(0*valeur),int(100*valeur),int(190*valeur))


def projeter(point):
    coords_merc = convert_to_mercator(point)
    x = (coords_merc[0] - centre_geo_x) * ECHELLE + CENTRE_ECRAN_X
    y = -(coords_merc[1] - centre_geo_y) * ECHELLE + CENTRE_ECRAN_Y  
    return (x, y)


for forme, code_dep in formes_metro_avec_code:
    points = forme.points
    parties = list(forme.parts) + [len(points)]
    remp = determiner_remplissage(donnees, code_dep)

    for i in range(len(forme.parts)):
        debut = parties[i]
        fin = parties[i + 1]
        polygon_points = [projeter(p) for p in points[debut:fin]]
        polygone(tuple(polygon_points), couleur="black", remplissage=remp)

attend_ev()
ferme_fenetre()