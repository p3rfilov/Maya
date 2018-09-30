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
                self.mesh = str(shape)
#             cmds.selectMode(component=True) # turn on component mode
            else:
                self.error()
        else:
            self.error()
    
    def error(self):
        om.MGlobal.displayError('Please select a single mesh')
        self.stop()
    
    def getVertLoop(self):
        '''
        Obtain a vertex loop given a mesh face and a ray hit coordinate.
        1. Get face vertices
        2. Measure the distance of each vertex to the hit point
        3. Pick 2 closest vertices and obtain a loop selection
        '''
        hit = self.getHitPoint()
        if hit:
            hitPos = hit[0]
            face = hit[1]
            obj = self.mesh + '.f[{f}]'.format(f=face)
            face2verts = cmds.polyListComponentConversion(obj, fromFace=True, toVertex=True)
            verts = []
            for v in face2verts:
                verts += cmds.ls(v, fl=True)
            vertPos = [cmds.pointPosition(v, world=True) for v in verts]
            print(vertPos)
#         cmds.SelectEdgeLoopSp()
    
    def getHitPoint(self):
        vpX, vpY, _ = cmds.draggerContext(self.name, query=True, anchorPoint=True)
        pos = om.MPoint()
        dir = om.MVector()
        hitPoint = om.MFloatPoint()
        hitFace = om.MScriptUtil().asIntPtr()
        
        omui.M3dView().active3dView().viewToWorld(int(vpX), int(vpY), pos, dir)
        pos2 = om.MFloatPoint(pos.x, pos.y, pos.z)
        
        selectionList = om.MSelectionList()
        selectionList.add(self.mesh)
        dagPath = om.MDagPath()
        selectionList.getDagPath(0, dagPath)
        fnMesh = om.MFnMesh(dagPath)
        
        intersection = fnMesh.closestIntersection(
        om.MFloatPoint(pos2),   # raySource
        om.MFloatVector(dir),   # rayDirection
        None,                   # faceIds
        None,                   # triIds
        False,                  # idsSorted
        om.MSpace.kWorld,       # space
        99999,                  # maxParam
        False,                  # testBothDirections
        None,                   # accelParams
        hitPoint,               # hitPoint
        None,                   # hitRayParam
        hitFace,                # hitFace
        None,                   # hitTriangle
        None,                   # hitBary1
        None)                   # hitBary2
        
        if intersection:
            return (
                hitPoint,
                om.MScriptUtil(hitFace).asInt() # get face number from pointer
                )
        else:
            return ()

    def onPress(self):
        button = cmds.draggerContext(self.name, query=True, button=True)
        if button != 2:
            vertLoop = self.getVertLoop()
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
