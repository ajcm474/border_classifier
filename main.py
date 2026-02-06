from pathlib import Path

from PyQt5.QtGui import QIcon
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QAction, QWidget

from .ui import BorderDockWidget


class BorderClassifier(QWidget):
    def __init__(self, iface):
        super(BorderClassifier, self).__init__(None)

        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.menu = "BorderClassifier"
        self.actions = []
        self.toolbar = None
        
        self.pluginIsActive = False
        self.dockwidget = None

    def initGui(self):
        self.dockwidget = BorderDockWidget(self.iface)

        self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)

        icon_path = str(Path(__file__).parent / "icon.png")

        self.action = QAction(
            QIcon(icon_path),
            "Border Classifier",
            self.iface.mainWindow()
        )
        self.action.setCheckable(True)
        self.action.triggered.connect(self.toggle_panel)

        self.iface.addPluginToMenu("&Border Classifier", self.action)
        self.iface.addToolBarIcon(self.action)

        self.dockwidget.visibilityChanged.connect(self.action.setChecked)

        self.dockwidget.hide()

    def unload(self):
        if self.dockwidget:
            self.iface.removeDockWidget(self.dockwidget)
            self.dockwidget = None

        if self.action:
            self.iface.removePluginMenu("&Border Classifier", self.action)
            self.iface.removeToolBarIcon(self.action)
            self.action = None

    def toggle_panel(self, checked):
        if self.dockwidget:
            self.dockwidget.setVisible(checked)
