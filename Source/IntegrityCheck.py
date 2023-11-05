import os

import re

import math

import maya.cmds as cmds
from functools import partial

generalMap = {}
layoutMap = {}
setPiecesMap = {}
setsMap = {}

checkboxPassFail = {}
    
def SelectAllChecks(bAll):
    for checkbox in generalMap.get('GeneralSec'):
        if (checkbox != 'All'):
            cmds.checkBox(checkbox, edit = True, value = bAll)
    for checkbox in layoutMap.get('LayoutSec'):
        if (checkbox != 'All'):
            cmds.checkBox(checkbox, edit = True, value = bAll)
    for checkbox in setPiecesMap.get('SetPiecesSec'):
        if (checkbox != 'All'):
            cmds.checkBox(checkbox, edit = True, value = bAll)
    for checkbox in setsMap.get('SetsSec'):
        if (checkbox != 'All'):
            cmds.checkBox(checkbox, edit = True, value = bAll)
    
def SelectAllGeneral(bGeneral):
    for checkbox in generalMap.get('GeneralSec', []):
        cmds.checkBox(checkbox, edit = True, value = bGeneral)
        
def SelectAllLayout(bLayout):
    for checkbox in layoutMap.get('LayoutSec', []):
        cmds.checkBox(checkbox, edit = True, value = bLayout)
        
def SelectAllSetPieces(bSetPieces):
    for checkbox in setPiecesMap.get('SetPiecesSec', []):
        cmds.checkBox(checkbox, edit = True, value = bSetPieces)
        
def SelectAllSets(bSets):
    for checkbox in setsMap.get('SetsSec', []):
        cmds.checkBox(checkbox, edit = True, value = bSets)
    
def UnusedNodes():
    
    allCorrect = True
    nodes = cmds.ls(dag = True, long = True)
    
    for node in nodes:
        if not cmds.listConnections(node):
            print(f"Deleting empty node: {node}")
            cmds.delete(node)
            allCorrect = False
            
    return allCorrect
    
def NamingConvention():
    allCorrect = True
    assets = cmds.ls(type = 'transform')
    
    prefix = 'mRef_'
    
    pattern = re.compile(f'^{prefix}[^0-9]+[0-9]+$')
    
    for asset in assets:
        name = asset.split("|")[-1]
        match_result = pattern.match(name)
        
        if not match_result:
            exclude = []
            message = f"Asset '{name}' does not match the naming convention."
            cmds.textScrollList('logText', edit = True, append = "Naming Convention")
            cmds.textScrollList('logText', edit = True, append = message)
            allCorrect = False
                
    return allCorrect
    
    
def NodeHierarchy():
        
    folderPath = "C:/Users/keege/OneDrive/Documents/maya/projects/default/TD Assignment 2/Published/Test/setPiece"
    assets = cmds.ls('*mRef_*', type = 'transform')
    allCorrect = True
    folderNames = [folder for folder in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, folder))]
    
    for asset in assets:
        for folder in folderNames:
            if folder in asset.split('|')[-1]:
                
                currentFilePath = cmds.referenceQuery(asset, filename = True)

                correctFilePath = "C:/Users/keege/OneDrive/Documents/maya/projects/default/TD Assignment 2/Published/Test/setPiece/{}/model/source/".format(folder)
                if not currentFilePath.startswith(correctFilePath):
                    cmds.textScrollList('logText', edit = True, append = "Node Hierarchy")
                    cmds.textScrollList('logText', edit = True, append = currentFilePath)
                    cmds.textScrollList('logText', edit = True, append = correctFilePath)
                    allCorrect = False
                
    return allCorrect


def ReferenceErrors():

    correctFolder = "Published"
    assets = cmds.ls('*mRef_*', type = 'transform')
    allCorrect = True
    
    for asset in assets:
        currentFilePath = cmds.referenceQuery(asset, filename = True)
        if not correctFolder in currentFilePath:
            cmds.textScrollList('logText', edit = True, append = "Reference Errorr")
            cmds.textScrollList('logText', edit = True, append = currentFilePath)
            allCorrect = False
            
    return allCorrect 
        
def NAN():
    
    allCorrect = True
    assets = cmds.ls(type = "transform")
    
    for asset in assets:
        attributes = cmds.listAttr(asset, string = '*.*', scalar = True)
        if attributes is not None:
            for attribute in attributes:
                value = cmds.getAttr(asset + '.' + attribute)
                if math.isnan(value) or abs(value) < 0.0001:
                    roundedValue = RoundToFour(value)
                    cmds.setAttr(asset + '.' + attribute, roundedValue, type = 'double')
                    allCorrect = False
                    print(asset)
                    
    return allCorrect
    
def RoundToFour(value):
    return round(value, 4)
    
def CameraAperture():
    
    defaultCameras = ["frontShape", "perspShape", "sideShape", "topShape", "|persp", "|front", "|side", "|top", "persp", "front", "side", "top"]
    allCameras = cmds.ls(type='camera')
    cameras = [cam for cam in allCameras if cam not in defaultCameras]
    
    correctHoriAp = 16
    correctVertiAp = 9
    
    allCorrect = True
    
    for cam in cameras:
        horiAp = cmds.getAttr(cam + '.horizontalFilmAperture')
        vertiAp = cmds.getAttr(cam + '.verticalFilmAperture')
        if (horiAp != correctHoriAp):
            cmds.setAttr(cam + '.horizontalFilmAperture', correctHoriAp)
            allCorrect = False
            
        if (vertiAp != correctVertiAp):
            cmds.setAttr(cam + '.verticalFilmAperture', correctVertiAp)
            allCorrect = False
            
    return allCorrect

    
def CameraFLandFStop():
    
    FLDistances = [12, 14, 16, 18, 21, 25, 27, 32, 35, 40, 50, 65, 75, 100, 135, 150]
    
    FStops = [1.3, 2, 2.8, 4, 5.6, 8, 11, 16, 22]
    
    cameras = cmds.ls(type = 'camera')
    
    allCorrect = True
    
    for cam in cameras:
        thisFL = cmds.getAttr(cam + '.focalLength')
        thisfStop = cmds.getAttr(cam + '.fStop')
        
        if thisFL not in FLDistances:
            roundDownFL = min(FLDistances, key=lambda x: abs(x - thisFL))
            cmds.setAttr(cam + '.focalLength', roundDownFL)
            allCorrect = False
            
        if thisfStop not in FStops:
            roundDownFS = min(FStops, key = lambda x: abs(x - thisFStop))
            cmds.setAttr(cam + '.fStop', roundDownFS)
            allCorrect = False
                
    return allCorrect
    
def TandPSetPieces():
    setPieces = cmds.ls(type = 'transform')
    
    allCorrect = True
    
    folderPath = "C:/Users/keege/OneDrive/Documents/maya/projects/default/TD Assignment 2/Published/Test/setPiece"
    
    folderNames = [folder for folder in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, folder))]
    
    for folder in folderNames:
        for setPiece in setPieces:
            if folder in setPiece:
                if CheckObjTandP(setPiece) == False:
                    allCorrect = False     
    
    return allCorrect
    
def TandPSets():
    setPieces = cmds.ls(type = 'transform')
    
    allCorrect = True
    
    folderPath = "C:/Users/keege/OneDrive/Documents/maya/projects/default/TD Assignment 2/Published/Test/sets"
    
    folderNames = [folder for folder in os.listdir(folderPath) if os.path.isdir(os.path.join(folderPath, folder))]
    
    for folder in folderNames:
        for setPiece in setPieces:
            if folder in setPiece:
                if CheckObjTandP(setPiece) == False:
                    allCorrect = False     
    
    return allCorrect
    
def CheckObjTandP(obj):
    scalePiv = cmds.xform(obj, query = True, scalePivot = True, objectSpace = True)
    rotatePiv = cmds.xform(obj, query = True, rotatePivot= True, objectSpace = True)
    
    if scalePiv != [0, 0, 0] or rotatePiv !=[0, 0, 0]:
        cmds.xform(obj, scalePivot = (0, 0, 0), objectSpace = True)
        cmds.xform(obj, rotatePivot = (0, 0, 0), objectSpace = True)
        return False
    else:
        return True
    
def ReferenceVersion():
    setPieces = cmds.ls(type='transform')

    allCorrect = True

    folderPath = "C:/Users/keege/OneDrive/Documents/maya/projects/default/TD Assignment 2/Published/Test/setPiece"

    folderNames = []
    
    for folder in os.listdir(folderPath):
        if os.path.isdir(os.path.join(folderPath, folder)):
            folderNames.append(folder)

    for folder in folderNames:
        for setPiece in setPieces:
            if folder in setPiece:
                referencePath = os.path.join(folderPath, folder, "model", "source")
                highestVersionNo = -1
                highestVersion = None

                for filename in os.listdir(referencePath):
                    if filename.endswith(".ma") or filename.endswith(".mb"):
                        versionStr = filename[-6:-3]
                        try:
                            version = int(versionStr)
                            if version > highestVersionNo:
                                highestVersionNo = version
                                highestVersion = filename
                        except ValueError:
                            print(f"Invalid version number in file: {filename}")

                if highestVersion is not None:
                    if setPiece != highestVersion:
                        message = f"The highest version for {setPiece} is: {highestVersion}"
                        cmds.textScrollList('logText', edit = True, append = "Reference Versions")
                        cmds.textScrollList('logText', edit = True, append = message)
                else:
                    print(f"No valid files with 3-digit versions were found for {setPiece}.")
                       
    
checkboxFunctions = {
    'UnusedNodes': UnusedNodes,
    'NamingConvention': NamingConvention,
    'NodeHierarchy': NodeHierarchy,
    'ReferenceErrors': ReferenceErrors,
    'NAN': NAN,
    'CameraAperture': CameraAperture,
    'CameraFLandFStop': CameraFLandFStop,
    'TandPSetPieces': TandPSetPieces,
    'TandPSets': TandPSets,
    'ReferenceVersion': ReferenceVersion
}
                        
def Run(*args):
    
    cmds.textScrollList('logText', edit = True, removeAll = True)
    
    for checkboxName, function in checkboxFunctions.items():
        isChecked = cmds.checkBox(checkboxName, query = True, value = True)
        if isChecked == True:
            PassFail = function()
            label = "Passed" if PassFail else "Failed"
            cmds.text(checkboxName + "PFT", edit = True, label = label)
        else:
            cmds.text(checkboxName + "PFT", edit = True, label = '')
    
def IntegrityCheckUI():
    
    if cmds.window('IntegrityCheck', exists = True):
        cmds.deleteUI('IntegrityCheck')
    
    cmds.window('IntegrityCheck', widthHeight=(500,200), resizeToFitChildren = True)
    cmds.columnLayout(adjustableColumn=True)
        
    cmds.text('Integrity Checker', align = "center", font = "boldLabelFont")
    cmds.separator(h=10)
    cmds.checkBox('All', onCommand = lambda x: SelectAllChecks(x), offCommand = lambda x: SelectAllChecks(x))
    cmds.separator(h=10)
    
    generalCheck = cmds.checkBox('General', align = "left", onCommand = lambda x: SelectAllGeneral(x), offCommand = lambda x: SelectAllGeneral(x))
    generalMap['GeneralSec'] = []
    generalMap['GeneralSec'].append(generalCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    unusedNodesCheck = cmds.checkBox('UnusedNodes', label = 'Unused Nodes', width = 390)
    generalMap['GeneralSec'].append(unusedNodesCheck)
    UnusedNodesPFT = cmds.text('UnusedNodesPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    namingConventionCheck = cmds.checkBox('NamingConvention', label = 'Naming Convention', width = 390)
    generalMap['GeneralSec'].append(namingConventionCheck)
    NamingConventionPFT = cmds.text('NamingConventionPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    nodeHierarchyCheck = cmds.checkBox('NodeHierarchy', label = 'Node Hierarchy', width = 390)
    generalMap['GeneralSec'].append(nodeHierarchyCheck)
    NodeHierarchyPFT = cmds.text('NodeHierarchyPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    referenceErrorsCheck = cmds.checkBox('ReferenceErrors', label = 'Reference Errors', width = 390)
    generalMap['GeneralSec'].append(referenceErrorsCheck)
    ReferenceErrorsPFT = cmds.text('ReferenceErrorsPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    NANCheck = cmds.checkBox('NAN', label = 'NAN', width = 390)
    generalMap['GeneralSec'].append(NANCheck)
    NANPFT = cmds.text('NANPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    layoutCheck = cmds.checkBox('Layout', align = "left", onCommand = lambda x: SelectAllLayout(x), offCommand = lambda x: SelectAllLayout(x))
    layoutMap['LayoutSec'] = []
    layoutMap['LayoutSec'].append(layoutCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    cameraApertureCheck = cmds.checkBox('CameraAperture', label = 'Camera Aperture', width = 390)
    layoutMap['LayoutSec'].append(cameraApertureCheck)
    CameraAperturePFT = cmds.text('CameraAperturePFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    cameraCheck = cmds.checkBox('CameraFLandFStop', label = 'Camera Focal Length and F Stop', width = 390)
    layoutMap['LayoutSec'].append(cameraCheck)
    CameraFLandFStopPFT = cmds.text('CameraFLandFStopPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    setPiecesCheck = cmds.checkBox('SetPieces', label = 'Set Pieces', align = "left", onCommand = lambda x: SelectAllSetPieces(x), offCommand = lambda x: SelectAllSetPieces(x))
    setPiecesMap['SetPiecesSec'] = []
    setPiecesMap['SetPiecesSec'].append(setPiecesCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    TandPCheckSP = cmds.checkBox('TandPSetPieces', label = 'Transform and Pivot (set pieces)', width = 390)
    setPiecesMap['SetPiecesSec'].append(TandPCheckSP)
    TandPSetPiecesPFT = cmds.text('TandPSetPiecesPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    setsCheck = cmds.checkBox('Sets', onCommand = lambda x: SelectAllSets(x), offCommand = lambda x: SelectAllSets(x))
    setsMap['SetsSec'] = []
    setsMap['SetsSec'].append(setsCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    TandPCheckS = cmds.checkBox('TandPSets', label = 'Transform and Pivot (sets)', width = 390)
    setsMap['SetsSec'].append(TandPCheckS)
    TandPSetsPFT = cmds.text('TandPSetsPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    referenceVersionCheck = cmds.checkBox('ReferenceVersion', label = 'Reference Version', width = 390)
    setsMap['SetsSec'].append(referenceVersionCheck)
    ReferenceVersionPFT = cmds.text('ReferenceVersionPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    cmds.textScrollList('logText', h = 200, allowMultiSelection = False)
    
    cmds.separator(h=10)
    cmds.button('Run', align = 'center', command = Run)
       
    cmds.showWindow()

IntegrityCheckUI()