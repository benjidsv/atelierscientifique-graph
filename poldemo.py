import os, sys
from osmnx.geocoder import geocode
from scripts.graphdisplayer import PlotGraph
from scripts.hconverter import GetGraphFromData
from scripts.polbackup import GeneratePollutionMapRelativeToGraph
from scripts.bestpath import Astar
from scripts.graphs import Graph
from functools import partial
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QHBoxLayout, QVBoxLayout, QGridLayout, QLayout, QFrame, QMessageBox
from PyQt5.QtWidgets import QGroupBox, QPushButton, QFileDialog, QLabel, QSlider, QSizePolicy, QComboBox, QLineEdit
from qdarkstyle import load_stylesheet_pyqt5 as darktheme


class PolDemoUI(QMainWindow):
    def __init__(self):
        """View initializer."""
        super().__init__()
        # Propriétés de la fenêtre
        self.setWindowTitle('Graph demo')
        self.setWindowIcon(QIcon('./ressources/icon.png'))
        self.graphpath = ''
        self.polpath = ''
        # Création du layout et widget central
        self.generalLayout = QHBoxLayout()
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.centralWidget.setLayout(self.generalLayout)
        # Création des widgets
        self._createInputs()
        
        

    def _createInputs(self):
        """Creates inputs"""
        inputLayout = QVBoxLayout()
        inputLayout.setAlignment(Qt.AlignLeft)
        
        # Initialisation des QGroupBox
        graphGBox = QGroupBox('Graphe')
        self.graphLayout = QVBoxLayout()
        graphGBox.setLayout(self.graphLayout)
        pathGBox = QGroupBox('Meilleur chemin')
        self.pathLayout = QVBoxLayout()
        pathGBox.setLayout(self.pathLayout)
        inputLayout.addWidget(graphGBox)
        polGBox = QGroupBox('Pollution')
        polLayout = QGridLayout()
        polLayout.setAlignment(Qt.AlignLeft)
        polGBox.setLayout(polLayout)
        inputLayout.addWidget(polGBox)

        # Ajout des widgets
        self.buttons = {'Afficher': None}
        for txt in self.buttons:
            self.buttons[txt] = QPushButton(txt)
            inputLayout.addWidget(self.buttons[txt])
        self.generalLayout.addLayout(inputLayout)
        
        # ========= GRAPH COMBO =========
        goptions = ['Requête OSM', 'Fichier']
        self.graphcombo = QComboBox()
        self.graphcombo.addItems(goptions)
        self.graphLayout.addWidget(self.graphcombo)
        self.graphLayout.addWidget(pathGBox)
        self.graphBrowse = QPushButton('Parcourir')
        self.graphQuery = QLineEdit()
        # ========= PATH COMBO =========
        poptions = ['Adresse', 'Coordonnées']
        self.pathcombo = QComboBox()
        self.pathcombo.addItems(poptions) 
        self.pathLayout.addWidget(self.pathcombo)
        # === Coords layout ===
        coordsLayout = QGridLayout()
        latlon = QHBoxLayout()
        latlon.addWidget(QLabel('Latitude'))
        latlon.addWidget(QLabel('Longitude'))
        coordsLayout.addLayout(latlon, 0, 1)
        coordsLayout.addWidget(QLabel('Départ:'), 1, 0)
        start = QHBoxLayout()
        self.startlat = QLineEdit()
        self.startlon = QLineEdit()
        start.addWidget(self.startlat)
        start.addWidget(self.startlon)
        coordsLayout.addLayout(start, 1, 1)
        coordsLayout.addWidget(QLabel('Arrivée:'), 2, 0)
        goal = QHBoxLayout()
        self.goallat = QLineEdit()
        self.goallon = QLineEdit()
        goal.addWidget(self.goallat)
        goal.addWidget(self.goallon)
        coordsLayout.addLayout(goal, 2, 1)
        self.coordsInput = QFrame()
        self.coordsInput.setLayout(coordsLayout)
        # === Query Input === 
        self.startQuery = QLineEdit()
        self.goalQuery = QLineEdit()
        queryLayout = QGridLayout()
        queryLayout.addWidget(QLabel('Départ:'), 0, 0)
        queryLayout.addWidget(self.startQuery, 0, 1)
        queryLayout.addWidget(QLabel('Arrivée:'), 1, 0)
        queryLayout.addWidget(self.goalQuery, 1, 1)
        self.pathQueries = QFrame()
        self.pathQueries.setLayout(queryLayout)
        # INIT
        self._updateGraphGBox()
        self._updatePathGBox()

        #            btntext : [pos, labeltxt]
        politems = {'Parcourir': [(0, 0), 'Données:']}
        for txt, info in politems.items():
            self.buttons[txt] = QPushButton(txt)
            polLayout.addWidget(QLabel(info[1]), info[0][0], info[0][1])
            polLayout.addWidget(self.buttons[txt], info[0][0], info[0][1] + 1)
        self.weightslider = QSlider(Qt.Horizontal)
        self.weightslider.setMaximum(100)
        polLayout.addWidget(QLabel("Importance:"), 2, 0)
        polLayout.addWidget(self.weightslider, 2, 1)
            
    def _updateGraphGBox(self):
        if self.graphcombo.currentText() == 'Fichier':
            self.graphmode = 'path'
            self.graphQuery.setParent(None)
            self.graphLayout.insertWidget(1, self.graphBrowse)
        elif self.graphcombo.currentText() == 'Requête OSM':
            self.graphmode = 'query'
            self.graphBrowse.setParent(None)
            self.graphLayout.insertWidget(1, self.graphQuery)

    def _updatePathGBox(self):
        if self.pathcombo.currentText() == 'Coordonnées':
            self.pathmode = 'coords'
            self.pathQueries.setParent(None)
            self.pathLayout.addWidget(self.coordsInput)
        elif self.pathcombo.currentText() == 'Adresse':
            self.pathmode = 'query'
            self.coordsInput.setParent(None)
            self.pathLayout.addWidget(self.pathQueries)

    def _browse(self, pathtype:str):
        """Opens a QFileDialog"""
        if pathtype == 'graph':
            filepath = QFileDialog.getOpenFileName(self, 'Graphe', '', '*.xml')[0]
            if filepath == '': return
            else: 
                self.graphpath = filepath
                self.graphBrowse.setText(os.path.basename(filepath))
        elif pathtype == 'pol':
            filepath = QFileDialog.getOpenFileName(self, 'Données de pollution', '', '*.csv')[0]
            if filepath == '': return
            else: 
                self.polpath = filepath
                self.buttons['Parcourir'].setText(os.path.basename(filepath))

    def _configPopup(self):
        """Opens a config QDialog"""
        print('CONFIG')

    def _listenClickInput(self):
        self.display.listening = True
        self.buttons['Sélectionner'].setEnabled(False)
    
    def _drawGraph(self, graph):
        """Draws the selected graph"""
        edges = self.graph.GetEdges()
    
        for line in edges: 
            self.display.axes.plot(*zip(*line), 'c')

    def errorPopup(self):
        error = QMessageBox(QMessageBox.Critical, 'Erreur', 'Données de Graphe invalides.')
        error.exec()

    def GetPoints(self) -> tuple:
        """Returns current entered start and end point coords or none if undefined"""
        if self.pathmode == 'coords': 
            if self.startlon == '' or self.startlat == '' or self.goallon == '' or self.goallat == '': return None
            return (self.startlon, self.startlat), (self.goallon, self.goallat)
        if self.pathmode == 'query':
            if self.startQuery.text() == '' or self.goalQuery.text() == '': return None
            start, goal = geocode(self.startQuery.text()), geocode(self.goalQuery.text())
            slonlat, glonlat = (start[1], start[0]), (goal[1], goal[0])
            return slonlat, glonlat


class BestLayoutController():
    """BestLayout Controller"""
    def __init__(self, pathfinding, pollution, plotting, view):
        """Initializer"""
        self._pathfinding = pathfinding
        self._pollution = pollution
        self._plotting = plotting
        self._view = view
        # Connects signals and slots
        self._connectSignals()

    def _connectSignals(self):
        """Connects signals and slots"""
        self._view.graphcombo.currentIndexChanged.connect(self._view._updateGraphGBox)
        self._view.pathcombo.currentIndexChanged.connect(self._view._updatePathGBox)
        self._view.buttons['Parcourir'].clicked.connect(partial(self._view._browse, pathtype='pol'))
        self._view.graphBrowse.clicked.connect(partial(self._view._browse, pathtype='graph'))
        self._view.buttons['Afficher'].clicked.connect(self._displayGraph)

    def _displayGraph(self):
        graph = self._computeGraph()
        if not graph: 
            self._view.errorPopup()
            return
        print('graph created')
        polmap = self._computePolmap(graph)
        graph.SetPollutionMap(polmap)
        print("polmap computed")
        self._view.currentGraph = graph
        path = self._computePath()
        print("path computed")
        self._plotting(graph, path, polmap)

    def _computeGraph(self):
        """Computes the given graph (file or osmnx query) and sends it to be plotted"""
        if self._view.graphmode == 'path': 
            if self._view.graphpath == '': return None
            graph = GetGraphFromData(self._view.graphpath, mode='path')
        elif self._view.graphmode == 'query': 
            if self._view.graphQuery.text() == '': return None
            graph = GetGraphFromData(self._view.graphQuery.text(), mode='query')
        return graph

    def _computePath(self):
        points = self._view.GetPoints()
        if points:
            start = self._view.currentGraph.ComputeNearestPoint(points[0])
            goal = self._view.currentGraph.ComputeNearestPoint(points[1])
            path = self._pathfinding(self._view.currentGraph, start, goal, self._view.weightslider.value()/100)
            return path
        else: 
            return None

    def _computePolmap(self, graph):
        if os.path.isfile(self._view.polpath): polmap = self._pollution(graph, self._view.polpath)
        else: polmap = None
        return polmap
        

def main():
    """Main function."""
    # Creates an instance of QApplication
    poldemo = QApplication(sys.argv)
    # Shows the calculator's GUI
    view = PolDemoUI()
    view.show()
    poldemo.setStyleSheet(darktheme())
    # Creates the controller and assign its model
    ctrl = BestLayoutController(Astar, GeneratePollutionMapRelativeToGraph, PlotGraph, view)
    # Executes the calculator's main loop
    sys.exit(poldemo.exec())

if __name__ == '__main__':
    main()