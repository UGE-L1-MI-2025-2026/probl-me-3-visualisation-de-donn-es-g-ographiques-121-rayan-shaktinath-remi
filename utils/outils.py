from math import radians, log, tan, pi

def convert_to_mercator(coords):
    R = 6378137.0
    lon = coords[0] 
    lat = coords[1]
    
    x = R * radians(lon)
    y = R * log(tan(pi/4.0 + radians(lat)/2.0))
    return (x, y)

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def convertir(value, inf, sup):
    if sup == inf: return 0
    return (value - inf) / (sup - inf)

def key_of_max(d):
    return d[max(d, key=d.get)]

def key_of_min(d):
    return d[min(d, key=d.get)]