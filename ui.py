

from qgis._core import QgsProject
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import pyqtSignal


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

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()