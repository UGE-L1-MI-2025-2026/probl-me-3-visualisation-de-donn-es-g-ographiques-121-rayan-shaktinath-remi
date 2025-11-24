from shapefile import *
from Requirement.fltk import *

sf = Reader("departements_20180101")

cree_fenetre(1000,1000)

print(sf.record)

seine_et_marne = sf.shape(47)
seine_et_marne = sf.shape(47)

for i in range(100):
    departement = sf.shape(i)
    for j in range(len(departement.points)):
        polygone((departement.points[j][0]*20,departement.points[j][1]*20),couleur="black")

attend_ev()

ferme_fenetre()