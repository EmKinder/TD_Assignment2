import maya.cmds as cmds
import os

directoryField = None
directory = ""
WIP_path = ""
publish_path = ""
valid_directory_path = False
name = ""

def setDirectory(*args):
    global directoryField 
    global directory
    global valid_directory_path
    selected_directory = cmds.fileDialog2(dialogStyle=2, fileMode=3)
    if selected_directory:
        directory = selected_directory[0]
        if not os.path.exists(directory + "/WIP"):
            customPopup("Directory not valid (missing either WIP or Published folder")
            cmds.textField(directoryField, edit=True, text="")
            valid_directory_path = False
        else:
            cmds.textField(directoryField, edit=True, text=directory)
            WIP_path = directory + "/WIP"
            publish_path = directory + "/Published"
            print("Selected Directory:", directory)
            valid_directory_path = True
            
def updateName(*args):
    global name
    name = cmds.textField('nameText', query=True, text=True)
    print("Sequence Name entered:", sequence_name)

def WIPExport(*args):
    updateName()
    global name 
    global WIP_path
    global valid_directory_path
    models = cmds.ls(geometry=True)
    set_pieces = cmds.ls(type='objectSet')
    animations = cmds.keyframe(q=True)
    lighting = cmds.ls(type='light')
    if(valid_directory_path):
        cmds.file(file_path, force=True, typ="mayaBinary", exportSelected=True)
    print("WIP export")

def publishExport(*args):
    print("Publish export")

def assetPublishing():
    global directoryField 
    window_name = 'assetPublishing'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI('assetPublishing')
    
    cmds.window(window_name, title="Asset Publishing", widthHeight=(500, 200))
    
    main_layout = cmds.columnLayout(adjustableColumn=True)
    
    directoryField = cmds.textField('directoryField', w=300, placeholderText="Select Directory Path")

    cmds.button(label="Set Base Directory", command=setDirectory)
    
    cmds.separator(h=10, style='none')
    
    cmds.text('Name', align="center", font="boldLabelFont")
    cmds.separator(h=5, style='none')
    text_field = cmds.textField('nameText', placeholderText="Name")
    
    cmds.separator(h=10, style='none')
            
    cmds.button(label="WIP", command=WIPExport)
    cmds.separator(h=5, style='none')
    cmds.button(label="Publish", command=publishExport)  
    
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