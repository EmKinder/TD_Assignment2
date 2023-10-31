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
    print("Unused Nodes")
    return True
    
def NamingConvention():
    print("Naming Convention")
    return True
    
def  NodeHierarchy():
    print("Node Hierarchy")
    return True
    
def ReferenceErrors():
    print("Reference Errors")
    return True
    
def NAN():
    print("NAN")
    return True
    
def CameraAperture():
    print("Camera Aperture")
    return True
    
def CameraFLandFStop():
    print("Camera FL")
    return True
    
def TandPSetPieces():
    print("T and P SP")
    return True
    
def TandPSets():
    print("T and P S")
    return True
    
def ReferenceVersion():
    print("Reference Version")
    return True
    
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
    
    cmds.window('IntegrityCheck', widthHeight=(300,200), resizeToFitChildren = True)
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
    unusedNodesCheck = cmds.checkBox('UnusedNodes', label = 'Unused Nodes', width = 190)
    generalMap['GeneralSec'].append(unusedNodesCheck)
    UnusedNodesPFT = cmds.text('UnusedNodesPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    namingConventionCheck = cmds.checkBox('NamingConvention', label = 'Naming Convention', width = 190)
    generalMap['GeneralSec'].append(namingConventionCheck)
    NamingConventionPFT = cmds.text('NamingConventionPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    nodeHierarchyCheck = cmds.checkBox('NodeHierarchy', label = 'Node Hierarchy', width = 190)
    generalMap['GeneralSec'].append(nodeHierarchyCheck)
    NodeHierarchyPFT = cmds.text('NodeHierarchyPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    referenceErrorsCheck = cmds.checkBox('ReferenceErrors', label = 'Reference Errors', width = 190)
    generalMap['GeneralSec'].append(referenceErrorsCheck)
    ReferenceErrorsPFT = cmds.text('ReferenceErrorsPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    NANCheck = cmds.checkBox('NAN', label = 'NAN', width = 190)
    generalMap['GeneralSec'].append(NANCheck)
    NANPFT = cmds.text('NANPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    layoutCheck = cmds.checkBox('Layout', align = "left", onCommand = lambda x: SelectAllLayout(x), offCommand = lambda x: SelectAllLayout(x))
    layoutMap['LayoutSec'] = []
    layoutMap['LayoutSec'].append(layoutCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    cameraApertureCheck = cmds.checkBox('CameraAperture', label = 'Camera Aperture', width = 190)
    layoutMap['LayoutSec'].append(cameraApertureCheck)
    CameraAperturePFT = cmds.text('CameraAperturePFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    cameraCheck = cmds.checkBox('CameraFLandFStop', label = 'Camera Focal Length and F Stop', width = 190)
    layoutMap['LayoutSec'].append(cameraCheck)
    CameraFLandFStopPFT = cmds.text('CameraFLandFStopPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    setPiecesCheck = cmds.checkBox('SetPieces', align = "left", onCommand = lambda x: SelectAllSetPieces(x), offCommand = lambda x: SelectAllSetPieces(x))
    setPiecesMap['SetPiecesSec'] = []
    setPiecesMap['SetPiecesSec'].append(setPiecesCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    TandPCheckSP = cmds.checkBox('TandPSetPieces', label = 'Transform and Pivot (set pieces)', width = 190)
    setPiecesMap['SetPiecesSec'].append(TandPCheckSP)
    TandPSetPiecesPFT = cmds.text('TandPSetPiecesPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    setsCheck = cmds.checkBox('Sets', onCommand = lambda x: SelectAllSets(x), offCommand = lambda x: SelectAllSets(x))
    setsMap['SetsSec'] = []
    setsMap['SetsSec'].append(setsCheck)
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    TandPCheckS = cmds.checkBox('TandPSets', label = 'Transform and Pivot (sets)', width = 190)
    setsMap['SetsSec'].append(TandPCheckS)
    TandPSetsPFT = cmds.text('TandPSetsPFT', label = '')
    cmds.setParent("..")
    cmds.rowLayout(numberOfColumns = 3)
    cmds.separator(w=20)
    referenceVersionCheck = cmds.checkBox('ReferenceVersion', label = 'Reference Version', width = 190)
    setsMap['SetsSec'].append(referenceVersionCheck)
    ReferenceVersionPFT = cmds.text('ReferenceVersionPFT', label = '')
    cmds.setParent("..")
    cmds.separator(h=10)
    
    cmds.button('Run', align = 'center', command = Run)
       
    cmds.showWindow()

IntegrityCheckUI()