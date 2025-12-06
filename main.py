# main.py
from Requirement.fltk import cree_fenetre, attend_ev, ferme_fenetre, rectangle
from utils.constantes import LARGEUR_FENETRE, HAUTEUR_FENETRE
from utils.lecture_csv import lire_abstentions
from utils.donnees import separer_formes_geo, calculer_stats_couleurs, calculer_params_metropole, calculer_params_dom
from utils.affichage import dessiner_metropole, dessiner_dom

def main():
    
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)
    donnees_csv = lire_abstentions("donner/resultats-definitifs-par-departements.csv")
    
    formes_metro, formes_dom = separer_formes_geo()

    stats_couleurs = calculer_stats_couleurs(donnees_csv)
    
    params_metro = calculer_params_metropole(formes_metro)

    params_dom = calculer_params_dom(formes_dom)
    
    dessiner_metropole(formes_metro, donnees_csv, stats_couleurs, params_metro)
    dessiner_dom(formes_dom, donnees_csv, stats_couleurs, params_dom)

    attend_ev()
    ferme_fenetre()

if __name__ == "__main__":
    main()