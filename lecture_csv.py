import csv

nom_dep = "Code département" 
nbr_abstentions = "% Abstentions"
code_dep = "Code département"

def obtenir_csv_reader(chemin_fichier):
    #Ouvre le fichier csv et le reader
    f = open(chemin_fichier, 'r', encoding='utf-8', newline='')
    reader = csv.reader(f, delimiter=';')
    return reader, f


def extraire_indices(reader):
    #Donne les indices des colonnes
    entetes = next(reader)
    
    index_code_dep = entetes.index(code_dep)
    index_nom_dep = entetes.index(nom_dep)
    index_abstentions = entetes.index(nbr_abstentions)
    
    return index_code_dep, index_nom_dep, index_abstentions


def traiter_donnees(reader, indices):
    #Construit le dico en traitant les données
    nombre_abstentions = {}
    index_code_dep, index_nom_dep, index_abstentions = indices
    max_index = max(index_abstentions, index_nom_dep, index_code_dep)
    
    for ligne in reader:
        if len(ligne) < max_index + 1:
            continue
            
        code_dep_val = ligne[index_code_dep].strip()
        nom_dep_val = ligne[index_nom_dep].strip()
        abstentions_str = ligne[index_abstentions].strip().replace(',', '.')
            
        if len(code_dep_val) > 3 or (code_dep_val.isdigit() and int(code_dep_val) > 96):
            continue
        
        abstentions = str(abstentions_str) 
            
        if code_dep_val == '2':
            nombre_abstentions['2A'] = abstentions
            nombre_abstentions['2B'] = abstentions
        else:
            nombre_abstentions[nom_dep_val] = abstentions
            
    return nombre_abstentions


def lire_abstentions(chemin_fichier):
    #fonction principal
    reader, fichier_ouvert = obtenir_csv_reader(chemin_fichier)
    indices = extraire_indices(reader)
    nombre_abstentions = traiter_donnees(reader, indices)
    fichier_ouvert.close()
    return nombre_abstentions


#test
CHEMIN_FICHIER = "resultats-definitifs-par-departements.csv" 
print(f"Lecture du fichier {CHEMIN_FICHIER}") 
donnees = lire_abstentions(CHEMIN_FICHIER) 
print(f"Nombre de départements : {len(donnees)}")
print("Liste de chaque département avec son nombre d'abstentions :")
departements_tries = sorted(donnees.items())
    
print(departements_tries)