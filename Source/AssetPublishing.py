import maya.cmds as cmds
import os

directoryField = None
directory = ""

def setDirectory(*args):
    global directoryField 
    global directory
    selected_directory = cmds.fileDialog2(dialogStyle=2, fileMode=3)
    if selected_directory:
        directory = selected_directory[0]
        if not os.path.exists(directory + "/WIP"):
            customPopup("Directory not valid (missing either WIP or Published folder")
            cmds.textField(directoryField, edit=True, text="")
        else:
            cmds.textField(directoryField, edit=True, text=directory)
            print("Selected Directory:", directory)


def assetPublishing():
    global directoryField 
    window_name = 'assetPublishing'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI('assetPublishing')
    
    cmds.window(window_name, title="Asset Publishing", widthHeight=(500, 120))
    
    main_layout = cmds.columnLayout(adjustableColumn=True)
    
    directoryField = cmds.textField('directoryField', w=300, placeholderText="Select Directory Path")

    cmds.button(label="Set Base Directory", command=setDirectory)
    cmds.button(label="WIP")
    cmds.button(label="Publish")  
    
    cmds.showWindow('assetPublishing')
    
def customPopup(message):
    if cmds.window("customPopupWindow", exists=True):
        cmds.deleteUI("customPopupWindow")

    customPopupWindow = cmds.window("customPopupWindow", title="Custom Popup", widthHeight=(200, 100))
    mainLayout = cmds.columnLayout(adjustableColumn=True, parent=customPopupWindow)
    cmds.text(label=message)
    cmds.button(label="Close", command=lambda *args: cmds.deleteUI(customPopupWindow))

    cmds.showWindow(customPopupWindow)
    
assetPublishing()