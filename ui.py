

from qgis._core import QgsProject
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal

from .backend import query_osm_boundary


class BorderDockWidget(QtWidgets.QDockWidget):
    closingPlugin = pyqtSignal()

    def __init__(self, iface):
        super(BorderDockWidget, self).__init__(iface.mainWindow())
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.setObjectName("BorderDockWidget")
        self.dockWidgetContents = QtWidgets.QWidget(self)
        self.dockWidgetLayout = QtWidgets.QVBoxLayout()
        self.dockWidgetContents.setLayout(self.dockWidgetLayout)

        self.currentCRS = QgsProject.instance().crs()

        self.setWidget(self.dockWidgetContents)

        self._populate_dockwidget()

    def _populate_dockwidget(self):
        locationSearchLayout = QtWidgets.QHBoxLayout()
        locationSearchLayout.addWidget(QtWidgets.QLabel("Admin Boundary:"))
        self.locationSearchField = QtWidgets.QLineEdit()
        locationSearchLayout.addWidget(self.locationSearchField)
        self.locationSearchButton = QtWidgets.QPushButton("Search")
        self.locationSearchButton.clicked.connect(self.search_admin_boundary)
        locationSearchLayout.addWidget(self.locationSearchButton)
        self.dockWidgetLayout.addLayout(locationSearchLayout)

    def search_admin_boundary(self):
        search_text = self.locationSearchField.text()
        if not search_text:
            popup = SearchErrorDialog(self, "Please enter a location first!")
            popup.exec_()
        else:
            try:
                boundary_data = query_osm_boundary(search_text, datetime.time())
                popup = SearchErrorDialog(self, str(boundary_data))
                popup.exec_()
            except Exception as e:
                popup = SearchErrorDialog(self, e.__str__())
                popup.exec_()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

class SearchErrorDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, message=""):
        super().__init__()
        self.parent = parent
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(QtWidgets.QLabel(message))
        self.setLayout(self.layout)