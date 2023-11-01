import maya.cmds as cmds
import os
import platform
import shutil


current_platform = platform.system()

if current_platform == 'Windows':
    print("user using windows")
elif current_platform == 'Linux':
    print("user using linux")
else:
    print("user using something else")

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
    global WIP_path
    global publish_path
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
    print("Sequence Name entered:", name)
    

def WIPExport(*args):
    updateName()
    global name
    global WIP_path
    global valid_directory_path
    assets = cmds.ls(type="transform", selection=True)[0]
    version_no = 1
    this_directory_name = WIP_path + "/" + name
    print("WIP_path:", WIP_path)
    print("this_directory_name:", this_directory_name)

    if not os.path.exists(this_directory_name):
        os.makedirs(this_directory_name)
    file_path = name + "_" + "{:03d}".format(version_no) + ".abc"
    full_file_path = os.path.join(this_directory_name, file_path)  # Construct the full file path

    print("full_file_path:", full_file_path)

    if valid_directory_path:
        while os.path.isfile(full_file_path):
            version_no += 1
            file_path = name + "_" + "{:03d}".format(version_no) + ".abc"
            full_file_path = os.path.join(this_directory_name, file_path)  # Update the full file path
            print("version exists, retrying")

        print("WIP export")
        print("Exporting to:", full_file_path)
        
       # cmds.select(assets)
        cmds.AbcExport(j="-frameRange 1 120 -root " + assets + " -file " + full_file_path)
       # else:
        #    print("No objects selected for export.")
    else:
        print("Directory not set or not valid. Please set the directory using setDirectory.")


def publishExport(*args):
    updateName()
    global name 
    global WIP_path
    global publish_path
    latest_published_version = ""
    version_no = 1
    this_WIP_directory = this_directory_name = WIP_path + "/" + name
    file_path = name + "_" + "{:03d}".format(version_no) + ".abc"
    full_file_path = os.path.join(this_directory_name, file_path)  # Construct the full file path
    while os.path.isfile(full_file_path):
        latest_published_version = full_file_path
        version_no += 1
        file_path = name + "_" + "{:03d}".format(version_no) + ".abc"
        full_file_path = os.path.join(this_directory_name, file_path)  # Update the full file path
    new_file_name = name + "_FINAL.abc"  # Replace with the new file name you want
    print(publish_path)
    # Construct the new file path by combining the directory and the new name
    new_file_path = os.path.join(publish_path, new_file_name)
    print(new_file_path)
    print(latest_published_version)
    try:
        # Copy the source file to the destination folder and rename it
        shutil.copy2(latest_published_version, new_file_path)
        print(f"File copied and renamed to: {new_file_path}")
    except Exception as e:
        print(f"Error copying and renaming the file: {str(e)}") 
        

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