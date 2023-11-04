import maya.cmds as cmds
import os
import shutil
import re
import maya.mel as mel
from functools import partial

directoryField = None
directory = ""
WIP_path = ""
publish_path = ""
valid_directory_path = False
name = ""
department_name = "Modelling"

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
    global department_name
    print("Department: " + department_name)
    version_no = 1
    if not name == "":
        this_directory_name = WIP_path + "/" + name
        sequence_directory = this_directory_name + "/Sequence"
        assets_directory = this_directory_name + "/Assets"
        print("WIP_path:", WIP_path)
        print("this_directory_name:", this_directory_name)
    
        if not os.path.exists(this_directory_name):
            os.makedirs(this_directory_name)
            os.makedirs(sequence_directory)
            os.makedirs(assets_directory)
        file_path = name + "_" + "{:03d}".format(version_no) + ".mb"
        if department_name == "Modelling":
            full_file_path = os.path.join(assets_directory, file_path)
        else:
            full_file_path = os.path.join(sequence_directory, file_path)
    
        print("full_file_path:", full_file_path)
    
        if valid_directory_path:
            while os.path.isfile(full_file_path):
                version_no += 1
                file_path = name + "_" + "{:03d}".format(version_no - 1) + ".mb"
                if department_name == "Modelling":
                    full_file_path = os.path.join(assets_directory, file_path)
                else:
                    full_file_path = os.path.join(sequence_directory, file_path)
                print("version exists, retrying")
    
            print("WIP export")
            print("Exporting to:", full_file_path)
            
            cmds.file(rename=full_file_path)
            cmds.file(save=True, type="mayaBinary")
        else:
            print("Directory not set or not valid.")
            customPopup("Directory not set or not valid.")
            return
        customPopup("Publish Success!")
    else:
        customPopup("No name specified")

def publishExport(*args):
    updateName()
    global name 
    global WIP_path
    global publish_path
    global directory_name
    version_no = 1
    if not name == "":
        if department_name == "Modelling":
            this_directory_name = WIP_path + "/" + name + "/Assets"
        else:
            this_directory_name = WIP_path + "/" + name + "/Sequence"
        file_path = name + "_" + "{:03d}".format(version_no) + ".mb"
        full_file_path = os.path.join(this_directory_name, file_path)
        
        latest_published_version = ""
        if valid_directory_path:
            while os.path.isfile(full_file_path):
                latest_published_version = full_file_path
                version_no += 1
                file_path = name + "_" + "{:03d}".format(version_no) + ".mb"
                full_file_path = os.path.join(this_directory_name, file_path)
            
            new_file_name = file_path
            this_publish_path = os.path.join(publish_path, name)
            setPiece_path = this_publish_path + "/setPiece"
            set_path = this_publish_path + "/sets"    
            layout_path = this_publish_path + "/layout"
            animation_path = this_publish_path +"/animations"
            layout_source_path = layout_path + "/source"
            layout_cache_path = layout_path + "/cache"
            
            if not os.path.exists(this_publish_path):
                os.makedirs(this_publish_path)
                os.makedirs(setPiece_path)
                os.makedirs(set_path)
                os.makedirs(layout_path)
                os.makedirs(animation_path)
                os.makedirs(layout_cache_path)
                os.makedirs(layout_source_path)
                
            cmds.file(latest_published_version, open=True, force=True)
            default_cameras = ["frontShape", "perspShape", "sideShape", "topShape", "|persp", "|front", "|side", "|top", "persp", "front", "side", "top"]
            all_cameras = cmds.ls(type='camera')
            cameras = [cam for cam in all_cameras if cam not in default_cameras]
            for camera_name in cameras:
                print(camera_name)
                if not camera_name:
                    print("no camera selected")
                else:
                    cmds.select(camera_name, replace=True)
                    source_exported_file = layout_source_path + "/" + camera_name + "_" + "{:03d}".format(version_no - 1) + ".mb"
                    cache_exported_file = layout_cache_path + "/" + camera_name + "_" + "{:03d}".format(version_no - 1) + ".abc"
                    cmds.file(source_exported_file, exportSelected=True, type='mayaBinary', preserveReferences=False)
                    cmds.AbcExport(j="-frameRange 1 120 -root " + camera_name + " -file " + cache_exported_file)
            print("Exporting Cameras Done")
            all_set_list = cmds.ls(dag=True, type='transform')
            set_list = [set for set in all_set_list if set not in default_cameras]
            set_name = set_list[0]
            print(set_name)
            if not set_name:
                print("no set selected")
            
            else:
                cmds.select(set_name, replace=True)
                exported_file = set_path + "/" + set_name + "_" + "{:03d}".format(version_no - 1) + ".mb"             
                cmds.file(exported_file, exportSelected=True, type='mayaBinary', preserveReferences=False)
                objects_in_set = cmds.listRelatives(set_name, children=True, type='transform', fullPath=True)
                print("Exporting Sets Done")
                for object_name in objects_in_set:
                    sanitized_name = object_name.replace(set_name, "")
                    sanitized_name = sanitized_name.replace("mRef", "")
                    sanitized_name = sanitized_name.replace("_", "")
                    sanitized_name = sanitized_name.replace(":", "")
                    sanitized_name = sanitized_name.replace("|", "")


                    set_export_path = setPiece_path + "/" + sanitized_name
                    exported_file = set_export_path + "/" + sanitized_name + "_" + "{:03d}".format(version_no - 1) + ".mb"
                    cmds.select(object_name, replace=True)
                    cmds.file(exported_file, exportSelected=True, type='mayaBinary', preserveReferences=False)
                    FBX_file_path = animation_path +"/" + sanitized_name +"/fbx"
                    ABC_file_path = os.path.join(animation_path, sanitized_name, "alembic")
                    if not os.path.exists(FBX_file_path):
                        os.makedirs(FBX_file_path)
                    if not os.path.exists(ABC_file_path):
                        os.makedirs(ABC_file_path)
                    alembic_file = os.path.join(ABC_file_path, sanitized_name + "_" + "{:03d}".format(version_no - 1) + ".abc")
                    fbx_export_path = FBX_file_path + "/" + sanitized_name + "_" + "{:03d}".format(version_no - 1)
                    print(fbx_export_path)
                    cmds.file(fbx_export_path, force=True, type="FBX export", pr=True, es=True )
                    cmds.AbcExport(j="-frameRange 1 120 -root " + object_name + " -file " + alembic_file)
                        
        else:
            print("Directory not set or not valid.")
            customPopup("Directory not set or not valid.")
            return
        customPopup("Publish Success!")
    else:
        customPopup("No name specified")        
def menu_item_selected(selection):
    global department_name
    department_name = selection
    print("Department Changed To: " + department_name)
    
def sanitize_name(name):
    return name.replace(':', '_').replace('|', '_')
                
def assetPublishing():
    global directoryField 
    window_name = 'assetPublishing'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI('assetPublishing')
    
    cmds.window(window_name, title="Asset Publishing", widthHeight=(500, 200))
    
    main_layout = cmds.columnLayout(adjustableColumn=True)
    cmds.separator(h=10, style='none')
    directoryField = cmds.textField('directoryField', w=300, placeholderText="Select Directory Path")
    cmds.separator(h=5, style='none')
    cmds.button(label="Set Base Directory", command=setDirectory)
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=5, style='double')
    cmds.separator(h=5, style='none')
    
    cmds.text('Name', align="center", font="boldLabelFont")
    cmds.separator(h=5, style='none')
    text_field = cmds.textField('nameText', placeholderText="Name")
    
    cmds.separator(h=10, style='none')
    cmds.separator(h=5, style='double')
    cmds.separator(h=5, style='none')
    
    menu_label = 'Department'
    menu_items = ['Modelling', 'Layout', 'Animation', 'Lighting']
    
    menu = cmds.optionMenu(label=menu_label, changeCommand=lambda x: menu_item_selected(cmds.optionMenu(menu, q=True, v=True)))

    for item in menu_items:
        cmds.menuItem(label=item)
        
    cmds.separator(h=10, style='none')
    cmds.separator(h=5, style='double')
    cmds.separator(h=5, style='none')     
           
    cmds.button(label="WIP", command=WIPExport)
    cmds.separator(h=5, style='none')
    cmds.button(label="Publish", command=publishExport)  
    
    cmds.separator(h=10, style='none')
    
    
    cmds.showWindow('assetPublishing')

        
def customPopup(message):
    if cmds.window("customPopupWindow", exists=True):
        cmds.deleteUI("customPopupWindow")

    customPopupWindow = cmds.window("customPopupWindow", title="System Message", widthHeight=(200, 50))
    mainLayout = cmds.columnLayout(adjustableColumn=True, parent=customPopupWindow)
    cmds.text(label=message)
    cmds.button(label="Close", command=lambda *args: cmds.deleteUI(customPopupWindow))

    cmds.showWindow(customPopupWindow)
    
assetPublishing()