from shapefile import *

sf = Reader("departements_20180101")

sf.records()

print(sf)