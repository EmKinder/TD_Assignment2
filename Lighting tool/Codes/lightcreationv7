import maya.cmds as cmds

def create_light(light_type, *args):
    light_types = {
        "Point Light": "pointLight",
        "Directional Light": "directionalLight",
        "Spot Light": "spotLight",
        "Area Light": "areaLight"
    }
    if light_type in light_types:
        light_name = cmds.shadingNode(light_types[light_type], asLight=True)
        light_transform = cmds.listRelatives(light_name, parent=True, fullPath=True)
        if light_transform:
            cmds.select(light_transform)
            return light_transform[0]
    else:
        cmds.warning("Invalid light type specified")

def delete_selected_lights(*args):
    selected_objects = cmds.ls(selection=True, dag=True, long=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="light"):
            light_transform = cmds.listRelatives(obj, parent=True, fullPath=True)
            if light_transform:
                cmds.delete(light_transform)
        elif cmds.listRelatives(obj, children=True, type="light"):
            cmds.delete(obj)

def group_lights(*args):
    selected_objects = cmds.ls(selection=True)
    if selected_objects:
        group_name = cmds.group(selected_objects, name="light_group")
        return group_name
    else:
        cmds.warning("No lights selected to group")

def rename_light(*args):
    new_name = cmds.textFieldGrp("renameLightField", query=True, text=True)
    selected_objects = cmds.ls(selection=True, long=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="transform") and cmds.listRelatives(obj, children=True, type="light"):
            cmds.rename(obj, new_name)
        else:
            cmds.warning(f"{obj} is not a light transform.")

def rename_group(*args):
    new_name = cmds.textFieldGrp("renameGroupField", query=True, text=True)
    selected_objects = cmds.ls(selection=True, long=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="transform") and cmds.listRelatives(obj, children=True):
            cmds.rename(obj, new_name)
        else:
            cmds.warning(f"{obj} is not a transform or has no children.")

def lighting_tool_ui():
    window_name = "lightingToolWindow"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    cmds.window(window_name, title="Lighting Tool", widthHeight=(300, 400))
    cmds.columnLayout(adjustableColumn=True)
    
    light_type_menu = cmds.optionMenu(label="Light Type")
    cmds.menuItem(label="Point Light")
    cmds.menuItem(label="Directional Light")
    cmds.menuItem(label="Spot Light")
    cmds.menuItem(label="Area Light")
    
    cmds.button(label="Create Light", command=lambda x: create_light(cmds.optionMenu(light_type_menu, query=True, value=True)))
    cmds.button(label="Delete Selected Lights", command=delete_selected_lights)
    cmds.button(label="Group Selected Lights", command=group_lights)
    
    cmds.textFieldGrp("renameLightField", label="New Light Name", text="new_light_name")
    cmds.button(label="Rename Selected Light", command=rename_light)
    
    cmds.textFieldGrp("renameGroupField", label="New Group Name", text="new_group_name")
    cmds.button(label="Rename Selected Group", command=rename_group)
    
    cmds.showWindow(window_name)

lighting_tool_ui()
