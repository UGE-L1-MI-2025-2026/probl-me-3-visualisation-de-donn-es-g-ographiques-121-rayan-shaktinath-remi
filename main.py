from shapefile import *
from Requirement.fltk import *

sf = Reader("departements_20180101")

cree_fenetre(1000,1000)

print(sf.shape)



for i in range(102):
    departement = sf.shape(i)
    for j in range(len(departement.points)):
        polygone(((departement.points[j][0]*68)+350,(departement.points[j][1]*68)-2700),couleur="black")

attend_ev()

ferme_fenetre()