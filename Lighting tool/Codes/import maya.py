import maya.cmds as cmds

def create_light(light_type):
    light_name = cmds.shadingNode(light_type, asLight=True)
    cmds.select(light_name)
    return light_name

def delete_selected_lights():
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="light"):
            cmds.delete(obj)

def select_light(light_name):
    cmds.select(light_name, replace=True)

def group_lights():
    selected_objects = cmds.ls(selection=True)
    group_name = cmds.group(selected_objects, name="light_group")
    return group_name

def ungroup_lights():
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="transform") and cmds.listRelatives(obj, children=True, type="light"):
            cmds.ungroup(obj)

def rename_light(old_name, new_name):
    cmds.rename(old_name, new_name)

def lighting_tool_ui():
    window_name = "lightingToolWindow"
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    cmds.window(window_name, title="Lighting Tool", widthHeight=(300, 400))
    cmds.columnLayout(adjustableColumn=True)
    
    cmds.optionMenu(label="Light Type", changeCommand=create_light)
    cmds.menuItem(label="Point Light")
    cmds.menuItem(label="Directional Light")
    cmds.menuItem(label="Spot Light")
    cmds.menuItem(label="Area Light")
    
    cmds.button(label="Delete Selected Lights", command=lambda x: delete_selected_lights())
    cmds.button(label="Group Selected Lights", command=lambda x: group_lights())
    cmds.button(label="Ungroup Selected Lights", command=lambda x: ungroup_lights())
    
    cmds.textFieldGrp(label="Rename Light", text="new_light_name", buttonLabel="Rename", buttonCommand=rename_selected_light)
    
    cmds.showWindow(window_name)

def rename_selected_light(*args):
    new_name = cmds.textFieldGrp("lightingToolWindow|columnLayout1|textFieldGrp1", query=True, text=True)
    selected_objects = cmds.ls(selection=True)
    for obj in selected_objects:
        if cmds.objectType(obj, isType="light"):
            rename_light(obj, new_name)

lighting_tool_ui()
