from Requirement.fltk import *
from utils import donnees
from utils.constantes import *
from utils.lecture_csv import *
from utils.donnees import *
from utils.affichage import *

def dessiner_carte(formes_metro, formes_dom, formes_idf, donnees, mode, chefs_lieux):
    
    efface_tout()

    palette = palette_pour_mode(mode)
    stats = calculer_stats_couleurs(donnees, palette)

    params_metro = calculer_params_metropole(formes_metro)
    params_idf = calculer_params_idf(formes_idf)
    params_dom = calculer_params_dom(formes_dom)

    image(650, 970, "image/right.png", largeur=150, hauteur=150, tag="image_droite")
    image(350, 970, "image/left.png", largeur=150, hauteur=150, tag="image_gauche")
    
    dessiner_metropole(formes_metro, donnees, stats, params_metro)
    dessiner_dom(formes_dom, donnees, stats, params_dom)
    dessiner_ile_de_france(formes_idf, donnees, stats, params_idf)
    dessiner_centroides(chefs_lieux, params_metro, params_dom, params_idf)
    dessiner_legende(donnees, stats)
    dessiner_titre(mode)

def main():
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    donnees_csv = lire_abstentions(CHEMIN_CSV)
    formes_metro, formes_dom, formes_idf = separer_formes_geo()

    modes = ["abstention", "blancs", "nuls"]
    index_mode = 0

    mode = modes[index_mode]
    donnees_actuelles = donnees_csv[mode]

    dessiner_carte(formes_metro, formes_dom, formes_idf, donnees_actuelles, mode, CHEFS_LIEUX)

    while True:
        ev = donne_ev()

        if type_ev(ev) == "Quitte":
            break

        if type_ev(ev) == "ClicGauche":
            id_obj = objet_survole()
            if id_obj is not None:
                tags = recuperer_tags(id_obj)
                if tags:
                    if "image_droite" in tags:
                        index_mode = (index_mode + 1) % len(modes)
                        mode = modes[index_mode]
                        donnees_actuelles = donnees_csv[mode]
                        dessiner_carte(formes_metro, formes_dom, formes_idf, donnees_actuelles, mode, CHEFS_LIEUX)
                    elif "image_gauche" in tags:
                        index_mode = (index_mode - 1) % len(modes)
                        mode = modes[index_mode]
                        donnees_actuelles = donnees_csv[mode]
                        dessiner_carte(formes_metro, formes_dom, formes_idf, donnees_actuelles, mode, CHEFS_LIEUX)


        if type_ev(ev) == "ClicGauche":

            id_clic = objet_survole()
            if id_clic is None:
                efface("contexte")
            else:
                tags = recuperer_tags(id_clic)
                code_survole = None
                for t in tags:
                    if t in donnees_actuelles:
                        code_survole = t
                        break

                if code_survole is not None:
                    dessiner_contexte(modes, code_survole, donnees_csv)
                else:
                    efface("contexte")

        if type_ev(ev) == "ClicDroit":
            efface("contexte")

        # --- Survol ---
        efface("info")
        id_obj = objet_survole()
             
        if id_obj:
            tags = recuperer_tags(id_obj)
            code_survole = None
            for t in tags:
                if t in donnees_actuelles or "%" in t:
                    code_survole = t
                    break

            if code_survole is not None:
                dessiner_survol(donnees_actuelles, code_survole, mode)

        mise_a_jour()

    ferme_fenetre()

if __name__ == "__main__":
    main()