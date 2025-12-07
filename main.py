from Requirement.fltk import *
from utils.constantes import LARGEUR_FENETRE, HAUTEUR_FENETRE
from utils.lecture_csv import lire_abstentions
from utils.donnees import separer_formes_geo, calculer_stats_couleurs, calculer_params_metropole, calculer_params_dom, palette_pour_mode
from utils.affichage import dessiner_legende, dessiner_metropole, dessiner_dom

def dessiner_carte(formes_metro, formes_dom, donnees, mode):
    
    efface_tout()

    palette = palette_pour_mode(mode)
    stats = calculer_stats_couleurs(donnees, palette)

    params_metro = calculer_params_metropole(formes_metro)
    params_dom = calculer_params_dom(formes_dom)

    dessiner_metropole(formes_metro, donnees, stats, params_metro)
    dessiner_dom(formes_dom, donnees, stats, params_dom)
    dessiner_legende(donnees, stats)



def main():
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    donnees_csv = lire_abstentions("donner/resultats-definitifs-par-departements.csv")
    formes_metro, formes_dom = separer_formes_geo()

    modes = ["abstention", "blancs", "nuls"]
    index_mode = 0

    mode = modes[index_mode]
    donnees_actuelles = donnees_csv[mode]

    dessiner_carte(formes_metro, formes_dom, donnees_actuelles, mode)

    while True:
        ev = donne_ev()

        if type_ev(ev) == "Quitte":
            break

        if type_ev(ev) == "Touche" and touche(ev) == "Right":
            index_mode = (index_mode + 1) % len(modes)
            mode = modes[index_mode]
            donnees_actuelles = donnees_csv[mode]
            dessiner_carte(formes_metro, formes_dom, donnees_actuelles, mode)

        if type_ev(ev) == "Touche" and touche(ev) == "Left":
            index_mode = (index_mode - 1) % len(modes)
            mode = modes[index_mode]
            donnees_actuelles = donnees_csv[mode]
            dessiner_carte(formes_metro, formes_dom, donnees_actuelles, mode)

        # --- Survol ---
        efface("info")
        id_obj = objet_survole()

        if id_obj:
            tags = recuperer_tags(id_obj)
            code_survole = None
            for t in tags:
                if t in donnees_actuelles:
                    code_survole = t
                    break

            if code_survole:
                valeur = donnees_actuelles[code_survole] * 100
                x = abscisse_souris()
                y = ordonnee_souris()

                if x + 300 > LARGEUR_FENETRE:
                    x = LARGEUR_FENETRE - 305

                rectangle(x + 5, y - 40, x + 300, y,
                          couleur="black",
                          remplissage="white",
                          tag="info")

                texte(x + 15, y - 15,
                      f"Département {code_survole} | {mode} : {valeur:.2f}%",
                      couleur="black",
                      taille=12,
                      tag="info",
                      ancrage="sw")

        mise_a_jour()

    ferme_fenetre()



if __name__ == "__main__":
    main()
