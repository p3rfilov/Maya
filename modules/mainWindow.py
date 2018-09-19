import maya.OpenMayaUI as mui
try:
	# Maya 2017+
	from PySide2 import QtCore, QtWidgets
	from PySide2.QtUiTools import QUiLoader
	from shiboken2 import wrapInstance
except ImportError:
	from PySide import QtCore, QtWidgets
	from PySide.QtUiTools import QUiLoader
	from shiboken import wrapInstance

class mainWindow(QtWidgets.QWidget):
	'''
	A boilerplate class for displaying a window in Maya using a UI file and PySide.
	Usage:
		window = mainWindow(r'//some/location/window.ui')
		window.ui.some_button.clicked.connect(doSomething)
	'''
	def __init__(self, uiFilePath, *args, **kwargs):
		super(mainWindow, self).__init__(*args, **kwargs)
		self.ui = None
		self.initUI(uiFilePath)
		
	def initUI(self, ui):	
		uiFile = QtCore.QFile(ui)
		loader = QUiLoader()
		uiFile.open(QtCore.QFile.ReadOnly)
		self.ui = loader.load(uiFile, self.getMayaMainWindow())
		uiFile.close()
		self.ui.setWindowFlags(QtCore.Qt.Drawer) # same as Tool, but supports Windows docking
		self.closeExistingWindow(self.ui.windowTitle())
		self.ui.show()
	
	def getMayaMainWindow(self):
		ptr = mui.MQtUtil.mainWindow()
		return wrapInstance(long(ptr), QtWidgets.QWidget)
	
	def closeExistingWindow(self, title):
		widgets = QtWidgets.QApplication.topLevelWidgets()
		for w in widgets:
			if w.isWindow() and not w.isHidden() and w.windowTitle() == title:
				self.closeWindow(w)
		
	def closeWindow(self, widget):
		widget.close()
		widget.deleteLater()
		