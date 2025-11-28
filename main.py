from shapefile import *
from Requirement.fltk import *
from math import *

LARGEUR_FENETRE = 1000
HAUTEUR_FENETRE = 1000
cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

shapefile_france = Reader("departements_20180101")

DEPARTEMENTS_METRO = {
    *[f"{i:02d}" for i in range(1, 96)],  
    "2A", "2B"                                 
}

def convert_to_mercator(coords):
    R = 6378137.0
    lon = coords[0]
    lat = coords[1]  
    
    x = R * radians(lon)
    y = R * log(tan(pi/4.0 + radians(lat)/2.0))
    
    return (x, y)

formes_metro = []
formes = shapefile_france.shapes()
enregistrements = shapefile_france.records()

for i in range(len(formes)):
    code_dept = enregistrements[i][0]
    if code_dept in DEPARTEMENTS_METRO:
        formes_metro.append(formes[i])

min_lat = min(min(pt[0] for pt in forme.points) for forme in formes_metro)
max_lat = max(max(pt[0] for pt in forme.points) for forme in formes_metro)
min_lon = min(min(pt[1] for pt in forme.points) for forme in formes_metro)
max_lon = max(max(pt[1] for pt in forme.points) for forme in formes_metro)

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

def projeter(point):
    coords_merc = convert_to_mercator(point)
    x = (coords_merc[0] - centre_geo_x) * ECHELLE + CENTRE_ECRAN_X
    y = -(coords_merc[1] - centre_geo_y) * ECHELLE + CENTRE_ECRAN_Y  
    return (x, y)

for forme in formes_metro:
    points = forme.points
    parties = list(forme.parts) + [len(points)]
    
    for i in range(len(forme.parts)):
        debut = parties[i]
        fin = parties[i + 1]
        polygon_points = [projeter(p) for p in points[debut:fin]]
        polygone(tuple(polygon_points), couleur="black")

attend_ev()
ferme_fenetre()