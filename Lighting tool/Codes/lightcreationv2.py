import maya.cmds as cmds

def create_light(light_type, *args):
    light_name = cmds.shadingNode(light_type, asLight=True)
    cmds.select(light_name)
    return light_name

def delete_selected_lights(*args):
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="light"):
            cmds.delete(obj)

def group_lights(*args):
    selected_objects = cmds.ls(selection=True)
    group_name = cmds.group(selected_objects, name="light_group")
    return group_name

def ungroup_lights(*args):
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="transform") and cmds.listRelatives(obj, children=True, type="light"):
            cmds.ungroup(obj)

def rename_light(*args):
    new_name = cmds.textFieldGrp("renameField", query=True, text=True)
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="light"):
            cmds.rename(obj, new_name)

def lighting_tool_ui():
    window_name = "lightingToolWindow"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    cmds.window(window_name, title="Lighting Tool", widthHeight=(300, 400))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.optionMenu(label="Light Type")
    cmds.menuItem(label="pointLight", command=lambda x: create_light("pointLight"))
    cmds.menuItem(label="directionalLight", command=lambda x: create_light("directionalLight"))
    cmds.menuItem(label="spotLight", command=lambda x: create_light("spotLight"))
    cmds.menuItem(label="areaLight", command=lambda x: create_light("areaLight"))
    
    cmds.button(label="Delete Selected Lights", command=delete_selected_lights)
    cmds.button(label="Group Selected Lights", command=group_lights)
    cmds.button(label="Ungroup Selected Lights", command=ungroup_lights)
    
    cmds.textFieldGrp("renameField", label="New Light Name", text="new_light_name")
    cmds.button(label="Rename Selected Light", command=rename_light)
    
    cmds.showWindow(window_name)

lighting_tool_ui()

