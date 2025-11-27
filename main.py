from shapefile import *
from Requirement.fltk import *

sf = Reader("departements_20180101")

LARGEUR_FENETRE = 1000
HAUTEUR_FENETRE = 1000

cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

shapefile_france = Reader("departements_20180101")

DEPARTEMENTS_METRO = {
    *[str(i).zfill(2) for i in range(1, 96)],  
    "2A", "2B"                                 
}

formes_metro = []
formes = shapefile_france.shapes()
enregistrements = shapefile_france.records()

for i in range(len(formes)):
    code_dept = enregistrements[i][0]
    if code_dept in DEPARTEMENTS_METRO:
        formes_metro.append(formes[i])

min_x = min(min(pt[0] for pt in forme.points) for forme in formes_metro)
max_x = max(max(pt[0] for pt in forme.points) for forme in formes_metro)
min_y = min(min(pt[1] for pt in forme.points) for forme in formes_metro)
max_y = max(max(pt[1] for pt in forme.points) for forme in formes_metro)

largeur_donnees = max_x - min_x
hauteur_donnees = max_y - min_y


echelle_x = LARGEUR_FENETRE / largeur_donnees
echelle_y = HAUTEUR_FENETRE / hauteur_donnees
ECHELLE = min(echelle_x, echelle_y) * 0.95


centre_geo_x = (min_x + max_x) / 2
centre_geo_y = (min_y + max_y) / 2

CENTRE_ECRAN_X = LARGEUR_FENETRE / 2
CENTRE_ECRAN_Y = HAUTEUR_FENETRE / 2
INVERSION_AXE_Y = -1 

ETIREMENT_Y = 1.35 

def projeter(point):

    x = (point[0] - centre_geo_x) * ECHELLE + CENTRE_ECRAN_X
    y = (point[1] - centre_geo_y) * ECHELLE * INVERSION_AXE_Y * ETIREMENT_Y + CENTRE_ECRAN_Y
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