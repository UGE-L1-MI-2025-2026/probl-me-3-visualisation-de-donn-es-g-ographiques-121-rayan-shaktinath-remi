from Requirement.fltk import *
from utils.constantes import *
from utils.lecture_csv import *
from utils.donnees import *
from utils.affichage import *

def dessiner_carte(formes_metro, formes_dom, formes_idf, donnees, mode):
    
    efface_tout()

    palette = palette_pour_mode(mode)
    stats = calculer_stats_couleurs(donnees, palette)

    params_metro = calculer_params_metropole(formes_metro)
    params_idf = calculer_params_idf(formes_idf)
    params_dom = calculer_params_dom(formes_dom)

    dessiner_metropole(formes_metro, donnees, stats, params_metro)
    dessiner_dom(formes_dom, donnees, stats, params_dom)
    dessiner_ile_de_france(formes_idf, donnees, stats, params_idf)
    dessiner_legende(donnees, stats)
    dessiner_titre(mode)

def main():
    cree_fenetre(LARGEUR_FENETRE, HAUTEUR_FENETRE)

    donnees_csv = lire_abstentions("donner/resultats-definitifs-par-departements.csv")
    formes_metro, formes_dom, formes_idf = separer_formes_geo()

    modes = ["abstention", "blancs", "nuls"]
    index_mode = 0

    mode = modes[index_mode]
    donnees_actuelles = donnees_csv[mode]

    dessiner_carte(formes_metro, formes_dom, formes_idf, donnees_actuelles, mode)

    while True:
        ev = donne_ev()

        if type_ev(ev) == "Quitte":
            break

        if type_ev(ev) == "Touche" and touche(ev) == "Right":
            index_mode = (index_mode + 1) % len(modes)
            mode = modes[index_mode]
            donnees_actuelles = donnees_csv[mode]
            dessiner_carte(formes_metro, formes_dom, formes_idf, donnees_actuelles, mode)

        if type_ev(ev) == "Touche" and touche(ev) == "Left":
            index_mode = (index_mode - 1) % len(modes)
            mode = modes[index_mode]
            donnees_actuelles = donnees_csv[mode]
            dessiner_carte(formes_metro, formes_dom, formes_idf, donnees_actuelles, mode)

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
                
                x = abscisse_souris()
                y = ordonnee_souris()

                if x + 300 > LARGEUR_FENETRE:
                    x = LARGEUR_FENETRE - 305
                if y - 40 < 0:
                    y = 45
                
                rectangle(x + 5, y - 40, x + 300, y,
                        couleur="black",
                        remplissage="white",
                        tag="info")
                if "%" in code_survole:
                    valeur = code_survole
                    texte(x + 15, y - 15,
                        f"Proportion de {mode} : {valeur}",
                        couleur="black",
                        taille=12,
                        tag="info",
                        ancrage="sw")
                elif code_survole is not None:
                    valeur = valeur = donnees_actuelles[code_survole] * 100
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
