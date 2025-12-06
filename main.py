from Requirement.fltk import *
from utils.constantes import LARGEUR_FENETRE, HAUTEUR_FENETRE
from utils.lecture_csv import lire_abstentions
from utils.donnees import separer_formes_geo, calculer_stats_couleurs, calculer_params_metropole, calculer_params_dom
from utils.affichage import dessiner_legende, dessiner_metropole, dessiner_dom

def main():
    
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    donnees_csv = lire_abstentions("donner/resultats-definitifs-par-departements.csv")
    
    formes_metro, formes_dom = separer_formes_geo()

    stats_couleurs = calculer_stats_couleurs(donnees_csv)
    
    params_metro = calculer_params_metropole(formes_metro)

    params_dom = calculer_params_dom(formes_dom)
    
    dessiner_metropole(formes_metro, donnees_csv, stats_couleurs, params_metro)
    dessiner_dom(formes_dom, donnees_csv, stats_couleurs, params_dom)
    dessiner_legende(donnees_csv)

    while True:
        ev = donne_ev() 
        if type_ev(ev) == 'Quitte':
            break
        
        efface("info")

        id_obj = objet_survole()
        
        if id_obj:
            tags = recuperer_tags(id_obj)
            
            code_survole = None
            for e in tags:
                if e in donnees_csv:
                    code_survole = e
                    break
            
            if code_survole:
                abstention = donnees_csv[code_survole] * 100
                x_souris = abscisse_souris()
                y_souris = ordonnee_souris()
                
                msg = "Département " + code_survole + " | Abstention : {:.2f}%".format(abstention) 
                
                if x_souris + 300 > LARGEUR_FENETRE:
                    x_souris = LARGEUR_FENETRE - 305
                
                rectangle(x_souris + 5, y_souris - 40, x_souris + 300, y_souris, 
                          couleur="black", 
                          remplissage="white", 
                          tag="info")
                texte(x_souris + 15, y_souris - 15, msg, 
                      couleur="black", 
                      remplissage="white",
                      taille=12, 
                      tag="info",
                      ancrage="sw")

        mise_a_jour()
    ferme_fenetre()

if __name__ == "__main__":
    main()