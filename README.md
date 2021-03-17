# atelierscientifique-graph

### Fait avec
* [osmnx](https://pypi.org/project/PyQt5/)
* [PyQt5](https://github.com/gboeing/osmnx)

<!-- UTILISATION -->
## Tutoriel

### Installation

1. Téléchargez le repo:
```sh
   git clone https://github.com/tozuky/atelierscientifique-graph.git
```
2. * (Windows) Installez les fichiers wheel suivants:
      * GDAL
      ```sh
      pip install ./depedencies/GDAL-3.2.1-cp38-cp38-win_amd64.whl
      ```
      * Fiona
      ```sh
      pip install ./depedencies/Fiona-1.8.18-cp38-cp38-win_amd64.whl
      ```
   * (UNIX) Installez les modules suivants:
      * GDAL
      ```sh
      pip install gdal
      ```
      * Fiona
      ```sh
      pip install fiona
      ``` 
3. Installez les modules du fichier requirements.txt:
  ```sh
  pip install -r ./dependencies/requirements.txt
  ```
  
### Utilisation

Lancez poldemo.py pour démarrer l'application de demo.
[![Application Démo][app-sc]]

Spécifiez ensuite des données de graphe, soit un fichier xml généré avec osmnx, soit une requête:
[![Paramètres du graphe][graph-settings-sc]]
La requête doit être écrite sous la forme suivante:
    * ville, pays, quartier, continent, lieu, etc.|paramètre1=valeur1,paramètre2=valeur2
    Exemple: Massy, Essonne, France|network_type=drive

Renseignez deux points, soit en tant qu'adresses/lieux, soit directement en coordonnées:
[![Paramètres du chemin][path-settings-sc]]

Finalement, des données de pollution (format csv, avec latitude, longitude, valeurs de pollution) puis ajustez la valeur d'importance:
[![Paramètres de pollution][pol-settings]]
La valeur d'importance correspond à l'importance qu'a la pollution dans la calcul du meilleur chemin entre les deux points donnés. 
* A 0 (tout a gauche), la pollution n'est pas prise en compte, seule la distance est calculée. 
* A 1 (tout a droite), la distance n'est pas prise en compte, seule la pollution est calculée. 
* Entre les deux, la pollution et la distance sont équilibrées selon la valeur.

Cliquez ensuite sur le bouton afficher afin d'afficher vos données:
[![Rendu final][plot-sc]]

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[app-sc]: screenshots/demo.PNG
[graph-settings-sc]: screenshots/graph-settings.png
[path-settings-sc]: screenshots/path-settings.png
[pol-settings-sc]: screenshots/pol-settings.png
[plot-sc]: screenshots/plot.png
