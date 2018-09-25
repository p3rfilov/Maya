# work in progress
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel

class jointPlacer():
    '''
    Joint placement tool. Joints are placed based on highlighted edge loops (under cursor).
    Press Q, W, E or R to exit the tool.
    '''
    def __init__(self):
        self.name = 'jointPlacer'
        self.selection = ''
    
    def start(self):
        self.deleteUIIfExists()
        cmds.draggerContext(
            self.name,
            releaseCommand='jointPlacer().onRelease()',
            dragCommand='jointPlacer().onDrag()',
            pressCommand='jointPlacer().onPress()',
            cursor='crossHair')
        cmds.setToolTo(self.name)
        self.assignSelection()
        
    def stop(self):
        '''Stop script by switching to Select Tool'''
        mel.eval('SelectTool')
        
    def deleteUIIfExists(self):
        if cmds.draggerContext(self.name, exists=True):
            cmds.deleteUI(self.name)
        
    def assignSelection(self):
        sel = cmds.ls(sl=True)
        if len(sel) == 1:
            self.selection = sel[0]
            cmds.selectMode(component=True) # turn on component mode
        else:
            om.MGlobal.displayError('Please select a single mesh')
            self.selection = ''
            self.stop()
    
    def getEdgeLoop(self):
        h = cmds.ls(psh=True)
        loop = cmds.polySelect(self.selection, edgeLoop=h)
        return loop

    def onPress(self):
        if self.selection:
            pass
    
    def onRelease(self):
        if self.selection:
            pass
    
    def onDrag(self):
        if self.selection:
            pass

# if __name__ == '__main__':
jp = jointPlacer()
jp.start()
