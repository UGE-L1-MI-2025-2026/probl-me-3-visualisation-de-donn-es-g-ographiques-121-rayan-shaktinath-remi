# Visualisation de données géolocalisées

(test)

L'objectif de ce problème est de visualiser diverses collections de données
géolocalisées sur une carte, à l'aide de `fltk`. On s'appuiera pour cela sur des données publiquement
disponibles, par exemple sur le site du gouvernement dédié à l'«open data», [data.gouv.fr](http://data.gouv.fr).
Pour les fichiers contenant les contours d'autres pays, ceux-ci sont [téléchargeable directement sur le site d'OSM(OpenStreetMaps)](https://osmdata.openstreetmap.de/data/).

## Exemple

Voici quelques captures d'écran montrant plusieurs cartes produites à l'aide de ces données.
Les programmes montrés n'utilisent aucun fichier image, le contour des départements est dessiné grâce à la fonction `polygone` de `fltk`, en s'appuyant sur les [Contours des départements français issus d'OpenStreetMap](https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/), au format [shapefile](https://www.data.gouv.fr/fr/datasets/r/eb36371a-761d-44a8-93ec-3d728bec17ce) (version 2018).


![Températures maximales par département le 01/07/2018](capture_dep.png)

La figure ci-dessus montre la carte des départements métropolitains français, où la couleur de fond de chaque département correspond à la température maximale moyenne observée le premier juillet 2018. Ces données sont issues du dataset [Température quotidienne départementale (depuis janvier 2018)](https://www.data.gouv.fr/fr/datasets/temperature-quotidienne-departementale-depuis-janvier-2018/), téléchargées au format [JSON](https://docs.python.org/3/library/json.html).
Une frise des couleurs par température est dessinée sur le bord droit de la fenêtre.

![Températures maximales par station météo le 01/07/2018](capture_stations.png)

La figure ci-dessus montre la carte des départements métropolitains français, ainsi que la température maximale mesurée le premier juillet 2018 par un ensemble de stations météo. Ces données sont issues du dataset [Données changement climatique - SQR (Séries Quotidiennes de Référence)](https://www.data.gouv.fr/fr/datasets/donnees-changement-climatique-sqr-series-quotidiennes-de-reference/), téléchargées au format ZIP (archive contenant des fichiers CSV).

![Licenciés de basket-ball en 2011 en Seine-et-Marne](capture_basket.png) 

Ce dernier exemple montre une carte de la Seine-et-Marne, où chaque disque représente le nombre de licenciés d'une fédération sportive (ici celle de basket-ball en 2011). 
L'aire de chaque disque est proportionnelle au nombre de licenciés. 
Les données sont issues du dataset [Carte des licenciés sportifs en Seine-et-Marne](https://www.data.gouv.fr/fr/datasets/carte-des-licencies-sportifs-en-seine-et-marne-idf/), au format CSV.
Dans ce prototype, le nom d'une commune et le nombre de licenciés qui y habitent sont affichés quand le pointeur de la souris survole le disque correspondant.

## Tâches obligatoires

Il est demandé de réaliser *a minima* un programme permettant d'afficher l'un des types de cartes illustrés ci-dessus.

De plus, on demande d'ajouter la possibilité de générer une carte **animée**, permettant de tracer l'évolution de données géographiques à travers le temps.  
A titre d'exemple, on propose de visualiser l'évolution de la température, à l'aide du [jeu de données DCENT](https://duochanatharvard.github.io/research_01_DCENT.html).

Il est recommandé de bien explorer les données choisies afin de comprendre ce qu'elles contiennent. Vous aurez pour cela besoin de vous documenter sur les formats [shapefile](https://en.wikipedia.org/wiki/Shapefile), [CSV](https://fr.wikipedia.org/wiki/Comma-separated_values) et éventuellement [JSON](https://fr.wikipedia.org/wiki/JavaScript_Object_Notation), et d'explorer le contenu des fichiers grâce au module [`pyshp`](https://pypi.org/project/pyshp/) ou à un logiciel de tableur comme [LibreOffice](https://fr.libreoffice.org/).

### Format de données et choix de projection

La manipulation du format shapefile a été faite à l'aide du module tiers `pyshp` dont [la documentation](https://pypi.org/project/pyshp/) contient des exemples simples d'utilisation. On détaille dans la partie suivante la manipulation des formats shapefile, sur l'exemple des départements français.

En fonction du format de données choisi pour les coordonnées géographiques, vous aurez à traiter des points exprimés dans deux systèmes de coordonnées différents : [WGS 84](https://fr.wikipedia.org/wiki/WGS_84), ou en [projection de Mercator](https://fr.wikipedia.org/wiki/Projection_de_Mercator). La différence entre les deux formats est détaillée [sur le site d'OpenStreetMap](https://osmdata.openstreetmap.de/info/projections.html#wgs84), mais il est conseillé d'écrire une fonction pour passer facilement passer d'un système de coordonnées à un autre, en fonction des cas d'usage.

Concernant le jeu de données de température DCENT, celui-ci est au format netCDF, que l'on conseille de traiter à l'aide du module [netCDF4](https://unidata.github.io/netcdf4-python/). 

### Comment tracer le contour d'un département ?

Pour accéder à la liste des points constituant le contour du département de Seine-et-Marne, on a par exemple exécuté les commandes suivantes, après avoir installé `pyshp` et téléchargé et décompressé le document indiqué ci-dessus.

```python
>>> import shapefile
>>> sf = shapefile.Reader("departements-20180101") #ouverture du fichier shapefile
>>> sf.records() # visualisation de toutes les entrées du fichier
[...,
Record #47: ['77', 'Seine-et-Marne', 'FR102', 
             'fr:Seine-et-Marne', 5927.0],
...]
>>> seine_et_marne = sf.shape(47) # Récupération de l'entrée correspondant à la Seine-et-Marne
>>> seine_et_marne.bbox # Les points extrémaux de la seine-et-marne
[2.3923284961351237, 48.12014561527111, 
3.559220826259302, 49.11789167125887]
>>> seine_et_marne.points # La liste des points du contour de la Seine-et-Marne
[(2.3923284961351237, 48.335929161584076), 
 (2.393003669902668, 48.336290983108846), 
 (2.3940130169559044, 48.3356802622364), ...]
```

L'attribut `seine_et_marne.bbox` indique les quatre coordonnées extrêmes présentes dans le tracé du contour du département : longitude minimale, latitude minimale, longitude maximale et latitude maximale exprimées en degré dans le système.

La liste des points `seine_et_marne.points` est donnée sous la forme d'une liste de couples de coordonnées (longitude, latitude) également exprimées en degré.

Attention, pour certains départements il y a une petite surprise : des **îles** ! Le dessin du polygone risque de ne pas se passer exactement comme prévu...

### Comment construire les disques ?

Chaque disque représente une donnée localisée à des coordonnées précises, exprimées dans le format WGS 84 (une station météo ou le nombre de licenciés d'un club de basket dans les exemples ci-dessus). Cette information a été récupérée dans les fichiers CSV indiqués sous chaque exemple.

La manipulation du format CSV a été faite à la main, notamment à l'aide de la méthode `split` de Python. 

#### Exemple des clubs de basket

Pour les clubs de basket, on s'est en particulier intéressé aux colonnes suivantes du tableau :

- `'commune'` : nom de chaque ville, pour l'affichage des étiquettes textuelles ;
- `'federation'` : nom de la fédération sportive concernée, pour la sélection des lignes concernant la fédération de basket-ball ;
- `'licences_en_2011'` : nombre de licenciés par commune en 2011, pour le calcul du rayon de chaque disque bleu ;
- `'wgs84'`: latitude et longitude de la commune, en degrés, pour le placement de chaque disque bleu.

Pour le calcul du rayon de chaque disque, il a été choisi de dessiner des disques d'*aire* proportionnelle au nombre représenté.

#### Exemple des stations météo

Pour les stations météo, l'organisation des données est un peu différente : il y a un fichier CSV différent pour chaque station météo, chacun de ces fichiers contenant les relevés de température depuis 1953 pour une station météo donnée. Si vous cherchez bien, vous trouverez sur la page du dataset ou dans les fichiers CSV le numéro, le nom, les coordonnées géographiques et l'altitude de chaque station météo.

## Suggestions d'améliorations

Voici une liste (comme d'habitude non exhaustive) d'améliorations possibles :

### Programme paramétrable

Le programme dispose de plusieurs paramètres en ligne de commande qui permettent de modifier son fonctionnement. 

Par exemple, il pourrait être possible de sélectionner :

- des données différentes dans la même base (par exemple : autres sports, températures moyennes ou minimum, précipitations, etc.), 
- des bases de données différentes (par exemple : restaurants, stations de train ou de métro, etc.),
- un département, région, pays ou commune différente,
- des paramètres d'affichage (échelle des disques, couleurs, taille du texte, etc.).

### Sélection et agrégation de données

Le programme permet de filtrer les données présentées, ou de rassembler plusieurs données entre elles. 

Par exemple, on pourrait souhaiter afficher le nombre total de licenciés par commune, tous sports confondus, si celui-ci dépasse 2% de la population de la commune.

### Visualisation avancée

Le programme permet d'afficher plusieurs données par commune (par exemple plusieurs sports), par exemple à l'aide d'un « diagramme camembert » coloré ou d'un autre mode de visualisation.

Le programme permet de dessiner plusieurs cartes côte à côte montrant des données différentes (par exemple températures minimales, moyennes et maximales, ou évolution des températures sur plusieurs années).

Le programme affiche des détails sur une zone (disque ou département) lorsqu'elle est survolée par la souris : nom de la commune, de la station météo ou du département, détail des données correspondantes, etc.

### Ajout de repères géographiques

Le programme dessine les contours des régions, indique la position des principales villes, ou les principales routes, les voies de chemin de fer, les fleuves, etc. De nombreuses données sont mises à la disposition du public par l'organisation OpenStreetMap, y compris sur le site [data.gouv.fr](data.gouv.fr).

### Interactivité

Il est possible d'obtenir des informations supplémentaires en survolant ou en cliquant sur les éléments graphiques de la fenêtre.

Il est également envisageable de déplacer la carte grâce à des touches du clavier, de zoomer ou dézoomer, etc.

Enfin, dans le cas des données climatiques par exemple, on peut envisager de passer d'une date à une autre grâce aux flèches (en ajoutant 1 jour ou 1 an à la date courante par exemple), ou pourquoi pas de créer une animation pour tenter de visualiser l'évolution du climat en France sur une période plus longue.

### Explorations diverses

Il est également possible d'explorer :

- d'autres formats de données géographiques (par exemple [GeoJSON](https://geojson.org/)) ou de tableurs (`odt`, `docx`) ;
- d'autres méthodes d'accès aux données (par exemple dynamiquement à l'aide d'API et de bibliothèques dédiées) ;
- d'autres échelles géographiques (quartier, commune, région, pays, continent, monde) ;
- d'autres types de données (végétation, pollution, démographie, santé, culture, trafic, célébrités, réseaux sociaux ou media...) ;