import maya.cmds as cmds
import os
import re

class ImportFilesUI:
    def __init__(self):
        self.window = 'importFilesWindow'
        self.title = 'Import Files'
        self.size = (800, 600)
        self.file_checkboxes = {}
        self.files_to_import = {}
        self.folder_path = None

    def create(self):
        if cmds.window(self.window, exists=True):
            cmds.deleteUI(self.window, window=True)

        self.window = cmds.window(self.window, title=self.title, widthHeight=self.size)
        self.main_layout = cmds.rowColumnLayout(numberOfColumns=2, columnWidth=[(1, 400), (2, 400)], parent=self.window)

        asset_types = ['set', 'layout', 'character', 'prop']
        for asset_type in asset_types:
            self.file_checkboxes[asset_type] = []
            self.files_to_import[asset_type] = {}

            cmds.setParent(self.main_layout)
            frame = cmds.frameLayout(label=f"{asset_type.capitalize()} Files", collapsable=True, bgc=[0.2, 0.2, 0.2])
            cmds.button(label=f'Select {asset_type.capitalize()} Folder', command=lambda x, asset_type=asset_type: self.select_folder(asset_type))
            scroll_layout = cmds.scrollLayout(horizontalScrollBarThickness=0, verticalScrollBarThickness=16, bgc=[0, 0, 0], height=300)
            column_layout = cmds.columnLayout(adjustableColumn=True, parent=scroll_layout)
            self.file_checkboxes[asset_type] = (scroll_layout, column_layout, [])

        cmds.setParent(self.main_layout)
        cmds.columnLayout(adjustableColumn=True)
        cmds.button(label='Reference Selected', command=self.reference_selected_from_all, height=50)
        cmds.button(label='Reference All', command=self.reference_all_from_all, height=50)
        cmds.button(label='Check Version', command=self.check_versions)

        cmds.showWindow(self.window)

    def select_folder(self, asset_type):
        folder_selection = cmds.fileDialog2(fileMode=2, caption=f"Select {asset_type.capitalize()} Folder", okCaption='Select')
        if not folder_selection:
            return
        folder_path = folder_selection[0] if isinstance(folder_selection, list) else folder_selection
        if not os.path.isdir(folder_path):
            cmds.warning(f"The selected path is not a valid folder: {folder_path}")
            return
        self.folder_path = folder_path
        self.refresh_ui(asset_type)

    def refresh_ui(self, asset_type):
        scroll_layout, column_layout, _ = self.file_checkboxes[asset_type]
        cmds.deleteUI(column_layout, layout=True)
        column_layout = cmds.columnLayout(adjustableColumn=True, parent=scroll_layout)
        self.file_checkboxes[asset_type] = (scroll_layout, column_layout, [])
        self.files_to_import[asset_type].clear()

        all_files = {}
        for dirpath, dirnames, files in os.walk(self.folder_path):
            valid_extensions = ['.ma', '.mb', '.obj', '.fbx', '.abc']
            for f in files:
                if os.path.splitext(f)[-1].lower() in valid_extensions:
                    version_match = re.search(r'v(\d+)', f)
                    if version_match:
                        version = int(version_match.group(1))
                        base_name = f[:version_match.start()]
                        if base_name not in all_files or all_files[base_name][1] < version:
                            all_files[base_name] = (os.path.join(dirpath, f), version)

        for base_name, (file_path, version) in sorted(all_files.items(), key=lambda item: item[1][1], reverse=True):
            file_rel_path = os.path.relpath(file_path, self.folder_path)
            checkbox = cmds.checkBox(label=file_rel_path, align='left', value=True, parent=column_layout)
            self.file_checkboxes[asset_type][2].append((checkbox, file_path))
            self.files_to_import[asset_type][file_rel_path] = file_path
    def reference_selected(self, asset_type):
        # Reference the files that are checked for the given asset type
        _, _, checkboxes = self.file_checkboxes[asset_type]
        for checkbox, file_path in checkboxes:
            if cmds.checkBox(checkbox, query=True, value=True):
                # Determine the namespace based on the file name
                namespace = os.path.basename(file_path).split('.')[0].replace(' ', '_')
                try:
                    cmds.file(file_path, r=True, namespace=namespace)  # Use 'r' flag for referencing
                    print(f"Referenced {file_path} successfully with namespace: {namespace}.")
                except Exception as e:
                    cmds.warning(f"Failed to reference {file_path}: {e}")

    def reference_selected_from_all(self, *args):
        # Reference selected files from all asset types
        for asset_type in self.file_checkboxes:
            self.reference_selected(asset_type)

    def reference_all_from_all(self, *args):
        # Reference all files from all asset types
        for asset_type in self.file_checkboxes:
            _, _, checkboxes = self.file_checkboxes[asset_type]
            for checkbox, file_path in checkboxes:
                # Set the checkbox to True before referencing
                cmds.checkBox(checkbox, edit=True, value=True)
            self.reference_selected(asset_type)
            
    def check_versions(self, *args):
        new_version_found = False
        updates = []

        for asset_type, file_paths in self.files_to_import.items():
            for file_rel_path, file_full_path in file_paths.items():
                directory = os.path.dirname(file_full_path)
                base_name, ext = os.path.splitext(os.path.basename(file_full_path))
                base_name_no_version = re.sub(r'v\d+$', '', base_name)

                all_files_in_dir = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
                highest_version = 0
                highest_version_file = ""
                for f in all_files_in_dir:
                    if f.startswith(base_name_no_version) and f.endswith(ext):
                        version_match = re.search(r'v(\d+)', f)
                        if version_match:
                            version = int(version_match.group(1))
                            if version > highest_version:
                                highest_version = version
                                highest_version_file = f

                current_version_match = re.search(r'v(\d+)', base_name)
                if current_version_match:
                    current_version = int(current_version_match.group(1))
                    if highest_version > current_version:
                        new_version_found = True
                        updates.append((file_full_path, os.path.join(directory, highest_version_file), highest_version, asset_type))

        if new_version_found:
            for current_file, new_file, new_version, asset_type in updates:
                result = cmds.confirmDialog(
                    title='New Version Found',
                    message=f"A new version for {os.path.basename(current_file)} is available: v{new_version}. Do you want to update?",
                    button=['Yes', 'No'],
                    defaultButton='Yes',
                    cancelButton='No',
                    dismissString='No'
                )
                if result == 'Yes':
                    self.replace_with_new_version(current_file, new_file, asset_type)
        else:
            cmds.confirmDialog(title='Check Version', message='No new versions found.', button=['Ok'])

    def replace_with_new_version(self, old_file, new_file, asset_type):
        print(f"Updating {old_file} to {new_file}")
        file_rel_path = os.path.relpath(new_file, self.folder_path)
        self.files_to_import[asset_type][file_rel_path] = new_file
        self.refresh_ui(asset_type)
        cmds.confirmDialog(
            title='Update Completed',
            message=f"The file has been updated to the latest version: {os.path.basename(new_file)}",
            button=['Ok']
        )

# Create and show the UI
ui = ImportFilesUI()
ui.create()