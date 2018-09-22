import maya.cmds as cmds
import maya.OpenMaya as om
from PySide2 import QtCore
from PySide2.QtWidgets import QTableWidgetItem
from modules.mainWindow import mainWindow
from modules.utilFuncs import findFileInSysPath

class geoStats():
    '''
    A small tool for displaying geometry statistics of currently selected objects.
    '''
    def __init__(self):
        self.window = mainWindow(findFileInSysPath('geoStats.ui'))
        self.table = self.window.ui.table
        self.connectSignals()
        self.setupTable()
        self.registerCallback()
        self.displayStats()
    
    def setupTable(self):
        self.table.setColumnWidth(0, 120)
        
    def connectSignals(self):
        self.window.ui.btn_refresh.clicked.connect(self.displayStats)

    def registerCallback(self):
        '''
        Registers a callback that is fired each time the selection changes.
        Removes callback when window is closed.
        '''
        self.callbackID = om.MEventMessage.addEventCallback('SelectionChanged', self.displayStats)
        self.window.ui.destroyed.connect(lambda: om.MMessage.removeCallback(self.callbackID))

    def getSel(self):
        sel = cmds.ls(sl=True)
        return sel
    
    def getStats(self):
        stats = cmds.polyEvaluate()
        if isinstance(stats, dict):
            return stats
        else:
            return {}
        
    def displayStats(self, *args, **kwargs):
        self.table.setRowCount(0)
        stats = self.getStats()
        for key, val in stats.iteritems():
            self.table.insertRow(0)
            i1 = QTableWidgetItem(key)      # parameter
            i2 = QTableWidgetItem(str(val)) # value
            i1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            i2.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            i1.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            i2.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
            self.table.setItem(0, 0, i1)
            self.table.setItem(0, 1, i2)
        
p = geoStats()