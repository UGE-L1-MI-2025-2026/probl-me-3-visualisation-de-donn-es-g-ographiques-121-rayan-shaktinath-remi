import csv

code_dep = "Code département" 
nbr_abstentions = "% Abstentions"
nbr_blancs = "% Blancs/inscrits"
nbr_nuls = "% Nuls/inscrits"

def obtenir_csv_reader(chemin_fichier):
    #Donne le reader et le fichier
    f = open(chemin_fichier, 'r', encoding='utf-8', newline='')
    reader = csv.reader(f, delimiter=';')
    return reader, f


def extraire_indices(reader):
    #Donne les indices des colonnes
    entetes = next(reader)
    
    index_code_dep = entetes.index(code_dep)
    index_abstentions = entetes.index(nbr_abstentions)
    index_blancs = entetes.index(nbr_blancs)
    index_nuls = entetes.index(nbr_nuls) 
    return index_code_dep, index_abstentions, index_blancs, index_nuls


def traiter_donnees(reader, indices):
    #Construit les trois dictionnaires en traitant les données
    dico_abstentions = {}
    dico_blanc = {}
    dico_nuls = {} 
    
    index_code_dep, index_abstentions, index_blancs, index_nuls = indices
    max_index = max(index_abstentions, index_blancs, index_nuls, index_code_dep) 
    
    for ligne in reader:
        if len(ligne) < max_index + 1:
            continue
            
        code_dep_val = ligne[index_code_dep].strip()
        
        if len(code_dep_val) == 1 and code_dep_val.isdigit():
            code_dep_val = "0" + code_dep_val

        abstentions_str = ligne[index_abstentions].strip().replace(',', '.')
        blancs_str = ligne[index_blancs].strip().replace(',', '.')
        nuls_str = ligne[index_nuls].strip().replace(',', '.') 
            
        if len(code_dep_val) > 3 or (code_dep_val.isdigit() and int(code_dep_val) > 96):
            if code_dep_val not in ["971","972","973","974","975","976","986","987","988", "ZX", "ZZ"]:
                 continue
            
        abstention_dec = float(abstentions_str.strip("%")) / 100
        blancs_dec = float(blancs_str.strip("%")) / 100
        nuls_dec = float(nuls_str.strip("%")) / 100

        if code_dep_val == '2':
            dico_abstentions['2A'] = abstention_dec
            dico_blanc['2A'] = blancs_dec
            dico_nuls['2A'] = nuls_dec
            dico_abstentions['2B'] = abstention_dec
            dico_blanc['2B'] = blancs_dec
            dico_nuls['2B'] = nuls_dec
        elif code_dep_val == "69":
            dico_abstentions['69D'] = abstention_dec
            dico_blanc['69D'] = blancs_dec
            dico_nuls['69D'] = nuls_dec
            dico_abstentions['69M'] = abstention_dec
            dico_blanc['69M'] = blancs_dec
            dico_nuls['69M'] = nuls_dec
        elif code_dep_val not in ["ZX", "ZZ"]:
            dico_abstentions[code_dep_val] = abstention_dec
            dico_blanc[code_dep_val] = blancs_dec
            dico_nuls[code_dep_val] = nuls_dec
            
    return {'abstention': dico_abstentions, 'blancs': dico_blanc, 'nuls': dico_nuls}


def lire_abstentions(chemin_fichier):
    #Fonction principale
    reader, fichier_ouvert = obtenir_csv_reader(chemin_fichier)
    indices = extraire_indices(reader)
    donnees = traiter_donnees(reader, indices)
    fichier_ouvert.close()
    return donnees

CHEMIN_FICHIER = "donner/resultats-definitifs-par-departements.csv" 
donnees_multiples = lire_abstentions(CHEMIN_FICHIER) 
nuls_data = donnees_multiples.get('nuls', {})
departements_tries = sorted(nuls_data.items())
print("Pourcentage de Nuls/Inscrits")
for code, nuls in departements_tries:
    print(f"  {code:<5}: {nuls:.2%}")