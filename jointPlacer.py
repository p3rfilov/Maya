# work in progress
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaUI as omui
import maya.mel as mel
import pymel.core as pm

class jointPlacer():
    '''
    Joint placement tool. Joints are placed based on highlighted edge loops (under cursor).
    Press mouse wheel (or Q) to exit the tool.
    '''
    def __init__(self):
        self.name = 'jointPlacer'
        self.mesh = ''
        self.jointChain = []
    
    def start(self):
        self.deleteUIIfExists()
        cmds.draggerContext(
            self.name,
            releaseCommand='jp.onRelease()',
            dragCommand='jp.onDrag()',
            pressCommand='jp.onPress()',
            cursor='crossHair')
        cmds.setToolTo(self.name)
        self.assignSelection()
        
    def stop(self):
        '''Stop script by switching to Select Tool'''
        self.mesh = ''
        self.jointChain = []
        mel.eval('SelectTool')
        
    def deleteUIIfExists(self):
        if cmds.draggerContext(self.name, exists=True):
            cmds.deleteUI(self.name)
        
    def assignSelection(self):
        sel = pm.ls(sl=True)
        if len(sel) == 1:
            shape = sel[0].getShape()
            if shape.type() == 'mesh':
                self.mesh = shape
#             cmds.selectMode(component=True) # turn on component mode
            else:
                self.error()
        else:
            self.error()
    
    def error(self):
        om.MGlobal.displayError('Please select a single mesh')
        self.stop()
    
    def getEdgeLoop(self):
        h = cmds.ls(psh=True)
        loop = cmds.polySelect(self.mesh, edgeLoop=h)
        return loop
    
    def getHitPoint(self):
        vpX, vpY, _ = cmds.draggerContext(self.name, query=True, anchorPoint=True)
        pos = om.MPoint()
        dir = om.MVector()
        hitpoint = om.MFloatPoint()
        omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
        pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
        for mesh in cmds.ls(type='mesh'):
            selectionList = om.MSelectionList()
            selectionList.add(mesh)
            dagPath = om.MDagPath()
            selectionList.getDagPath(0, dagPath)
            fnMesh = om.MFnMesh(dagPath)
            intersection = fnMesh.closestIntersection(
            om.MFloatPoint(pos2),
            om.MFloatVector(dir),
            None,
            None,
            False,
            om.MSpace.kWorld,
            99999,
            False,
            None,
            hitpoint,
            None,
            None,
            None,
            None,
            None)
            if intersection:
                return (hitpoint.x, hitpoint.y, hitpoint.z)
            else:
                return ()

    def onPress(self):
        button = cmds.draggerContext(self.name, query=True, button=True)
        if button != 2:
            hit = self.getHitPoint()
            print(hit)
        else:
            self.stop()
    
    def onDrag(self):
        dragPosition = cmds.draggerContext(self.name, query=True, dragPoint=True)
        print(dragPosition)
    
    def onRelease(self):
        pass

# if __name__ == '__main__':
jp = jointPlacer()
jp.start()
