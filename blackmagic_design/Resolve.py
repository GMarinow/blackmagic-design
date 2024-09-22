import os
import subprocess
import time
from .core import DaVinciResolveScript as bmd


class Resolve:
    def __init__(self, app: str = 'Resolve'):
        """
        Initializes the Resolve class, wrapping the DaVinci Resolve application.

        Args:
            app (str): The name of the DaVinci Resolve application to connect to. Defaults to 'Resolve'.
        """
        self.app = None
        self.media_storage = None
        self.project_manager = None

        try:
            self.app = bmd.scriptapp(app)
            if self.app:
                self.media_storage = MediaStorage(self.app.GetMediaStorage())
                self.project_manager = ProjectManager(self.app.GetProjectManager())
        except Exception as e:
            print(f"Failed to initialize Resolve: {e}")

    def open(
            self, executable_path: str = 'C:/Program Files/Blackmagic Design/DaVinci Resolve/Resolve.exe',
            wait_time: int = 15, gui: str = '-gui'
    ) -> str:
        """
        Attempts to open DaVinci Resolve if it is not already running.

        Args:
            executable_path (str): The file path to the DaVinci Resolve executable. Defaults to the typical installation path.
            wait_time (int): Time to wait (in seconds) after attempting to open DaVinci Resolve before checking if it's running. Defaults to 15 seconds.
            gui (str): for now GUI use -nogui

        Returns:
            str: A message indicating whether Resolve was successfully opened, is already running, or if there was an error.
        """
        if not os.path.exists(executable_path):
            return f"Error: Resolve executable not found at '{executable_path}'. Please check the path and try again."

        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            if 'Resolve.exe' in result.stdout:
                return "DaVinci Resolve is already running."

            if gui == '-gui':
                subprocess.Popen([executable_path])
            elif gui == '-nogui':
                subprocess.Popen(f'{executable_path} -nogui')

            time.sleep(wait_time)

            result = subprocess.run(['tasklist'], capture_output=True, text=True)
            if 'Resolve.exe' in result.stdout:
                return "DaVinci Resolve opened successfully."
            else:
                return "Error: Failed to detect Resolve in the task list. Please verify if the application has started."

        except Exception as e:
            return f"Error: Failed to open DaVinci Resolve - {str(e)}"

    def get_media_storage(self):
        """
        Returns the MediaStorage object for interacting with DaVinci Resolve's media storage.

        Returns:
            MediaStorage: The media storage interface.
        """
        return self.media_storage

    def get_project_manager(self):
        """
        Returns the ProjectManager object for interacting with DaVinci Resolve's project manager.

        Returns:
            ProjectManager: The project manager interface.
        """
        return self.project_manager

    def open_page(self, page_name: str) -> bool:
        """
        Switches to the indicated page in DaVinci Resolve.

        Args:
            page_name (str): The name of the page to switch to. Must be one of: 
                             "media", "cut", "edit", "fusion", "color", "fairlight", "deliver".

        Returns:
            bool: True if the page was successfully opened, False otherwise.
        """
        valid_pages = ["media", "cut", "edit", "fusion", "color", "fairlight", "deliver"]
        if page_name.lower() not in valid_pages:
            raise ValueError(f"Invalid page name: {page_name}. Must be one of {valid_pages}.")
        
        return self.app.OpenPage(page_name.lower())

    def get_current_page(self) -> str:
        """
        Returns the page currently displayed in the main window.

        Returns:
            str: The name of the currently active page. It can be one of:
                 "media", "cut", "edit", "fusion", "color", "fairlight", "deliver", or None.
        """
        return self.app.GetCurrentPage()

    def get_product_name(self) -> str:
        """
        Returns the product name of DaVinci Resolve.

        Returns:
            str: The product name.
        """
        return self.app.GetProductName()

    def get_version(self) -> list:
        """
        Returns the version of DaVinci Resolve as a list of version fields.

        Returns:
            list: A list of product version fields in [major, minor, patch, build, suffix] format.
        """
        return self.app.GetVersion()

    def get_version_string(self) -> str:
        """
        Returns the product version as a formatted string.

        Returns:
            str: The product version in "major.minor.patch[suffix].build" format.
        """
        return self.app.GetVersionString()

    def load_layout_preset(self, preset_name: str) -> bool:
        """
        Loads a UI layout preset.

        Args:
            preset_name (str): The name of the preset to load.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.LoadLayoutPreset(preset_name)

    def update_layout_preset(self, preset_name: str) -> bool:
        """
        Overwrites an existing UI layout preset.

        Args:
            preset_name (str): The name of the preset to overwrite.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.UpdateLayoutPreset(preset_name)

    def export_layout_preset(self, preset_name: str, preset_file_path: str) -> bool:
        """
        Exports a UI layout preset to the specified file path.

        Args:
            preset_name (str): The name of the preset to export.
            preset_file_path (str): The path to export the preset to.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.ExportLayoutPreset(preset_name, preset_file_path)

    def delete_layout_preset(self, preset_name: str) -> bool:
        """
        Deletes a UI layout preset.

        Args:
            preset_name (str): The name of the preset to delete.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.DeleteLayoutPreset(preset_name)

    def save_layout_preset(self, preset_name: str) -> bool:
        """
        Saves the current UI layout as a preset.

        Args:
            preset_name (str): The name to save the preset as.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.SaveLayoutPreset(preset_name)

    def import_layout_preset(self, preset_file_path: str, preset_name: str = None) -> bool:
        """
        Imports a UI layout preset from a file path.

        Args:
            preset_file_path (str): The path to the preset file.
            preset_name (str, optional): The name to save the preset as. Defaults to None.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.ImportLayoutPreset(preset_file_path, preset_name)

    def import_render_preset(self, preset_path: str) -> bool:
        """
        Imports a render preset from a file path.

        Args:
            preset_path (str): The path to the render preset file.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.ImportRenderPreset(preset_path)

    def export_render_preset(self, preset_name: str, export_path: str) -> bool:
        """
        Exports a render preset to a file path.

        Args:
            preset_name (str): The name of the preset to export.
            export_path (str): The path to export the preset to.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.ExportRenderPreset(preset_name, export_path)

    def import_burn_in_preset(self, preset_path: str) -> bool:
        """
        Imports a data burn-in preset from a file path.

        Args:
            preset_path (str): The path to the burn-in preset file.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.ImportBurnInPreset(preset_path)

    def export_burn_in_preset(self, preset_name: str, export_path: str) -> bool:
        """
        Exports a data burn-in preset to a file path.

        Args:
            preset_name (str): The name of the preset to export.
            export_path (str): The path to export the preset to.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.app.ExportBurnInPreset(preset_name, export_path)

    def quit(self) -> str:
        """
        Attempts to quit the DaVinci Resolve application gracefully. If it fails to close, 
        provides feedback to manually terminate the process.

        Returns:
            str: A message indicating whether DaVinci Resolve was closed successfully 
            or if manual intervention is required.
        """
        try:
            self.app.Quit()

            result = subprocess.run(['tasklist'], capture_output=True, text=True)

            if 'Resolve.exe' not in result.stdout:
                return 'DaVinci Resolve has been closed successfully.'

            return 'DaVinci Resolve did not close. Please use the kill function to terminate it manually.'
        
        except AttributeError:
            return 'Resolve application is not initialized. Cannot quit.'

        except Exception as e:
            return f'Failed to quit DaVinci Resolve: {e}'

    def kill(self) -> str:
        """
        Forces the termination of the DaVinci Resolve application process.

        Returns:
            str: A message indicating whether DaVinci Resolve was successfully terminated 
            or if an error occurred.
        """
        try:
            # Forcefully kill DaVinci Resolve process using taskkill
            result = subprocess.run(['taskkill', '/IM', 'Resolve.exe', '/F'], capture_output=True, text=True)

            # Check the result of the taskkill command
            if 'SUCCESS' in result.stdout:
                return 'DaVinci Resolve has been forcefully terminated.'
            else:
                return 'Failed to terminate DaVinci Resolve. Process may not be running.'

        except Exception as e:
            return f'Failed to kill DaVinci Resolve: {e}'

class MediaStorage:
    def __init__(self, media_storage):
        """
        Initializes the MediaStorage class, wrapping the provided media storage object.

        Args:
            media_storage: The underlying MediaStorage object from DaVinci Resolve's API.
        """
        self.media_storage = media_storage

    def get_mounted_volume_list(self) -> list:
        """
        Retrieves a list of folder paths corresponding to mounted volumes 
        displayed in DaVinci Resolve’s Media Storage.

        Returns:
            list: A list of absolute folder paths (strings) corresponding to mounted volumes.
        """
        return self.media_storage.GetMountedVolumeList()

    def get_sub_folder_list(self, folder_path: str) -> list:
        """
        Retrieves a list of folder paths in the given absolute folder path.

        Args:
            folder_path (str): The absolute path of the folder whose subfolders are to be listed.

        Returns:
            list: A list of absolute folder paths (strings) contained within the specified folder.
        """
        return self.media_storage.GetSubFolderList(folder_path)

    def get_file_list(self, folder_path: str) -> list:
        """
        Retrieves a list of media and file listings in the given absolute folder path.

        Args:
            folder_path (str): The absolute path of the folder whose files are to be listed.

        Returns:
            list: A list of media files (strings) contained within the specified folder.
                  Note: The media listings may include logically consolidated entries.
        """
        return self.media_storage.GetFileList(folder_path)

    def reveal_in_storage(self, path: str) -> bool:
        """
        Expands and displays the given file or folder path in DaVinci Resolve’s Media Storage.

        Args:
            path (str): The absolute file or folder path to reveal in Media Storage.

        Returns:
            bool: True if the file or folder is successfully revealed, False otherwise.
        """
        return self.media_storage.RevealInStorage(path)

    def add_item_list_to_media_pool(self, *items) -> list:
        """
        Adds the specified file or folder paths from Media Storage into the current Media Pool folder.

        Args:
            *items: One or more file or folder paths to be added to the Media Pool.

        Returns:
            list: A list of MediaPoolItems created from the added file or folder paths.
        """
        return self.media_storage.AddItemListToMediaPool(*items)

    def add_item_list_to_media_pool_array(self, items: list) -> list:
        """
        Adds an array of file or folder paths from Media Storage into the current Media Pool folder.

        Args:
            items (list): A list of file or folder paths to be added to the Media Pool.

        Returns:
            list: A list of MediaPoolItems created from the added file or folder paths.
        """
        return self.media_storage.AddItemListToMediaPool(items)

    def add_item_list_to_media_pool_info(self, item_info_list: list) -> list:
        """
        Adds a list of itemInfos from Media Storage into the current Media Pool folder. 

        Args:
            item_info_list (list): A list of dictionaries where each dictionary represents 
                                   item information with "media", "startFrame", and "endFrame" keys.

        Returns:
            list: A list of MediaPoolItems created based on the specified itemInfos.
        """
        return self.media_storage.AddItemListToMediaPool(item_info_list)

    def add_clip_mattes_to_media_pool(self, media_pool_item, paths: list, stereo_eye: str = None) -> bool:
        """
        Adds specified media files as mattes for the given MediaPoolItem.

        Args:
            media_pool_item: The MediaPoolItem for which the mattes are to be added.
            paths (list): A list of file paths to be added as mattes.
            stereo_eye (str, optional): Specifies which eye ("left" or "right") to add the matte to 
                                        for stereo clips. Defaults to None.

        Returns:
            bool: True if the mattes are successfully added, False otherwise.
        """
        return self.media_storage.AddClipMattesToMediaPool(media_pool_item, paths, stereo_eye)

    def add_timeline_mattes_to_media_pool(self, paths: list) -> list:
        """
        Adds specified media files as timeline mattes in the current media pool folder.

        Args:
            paths (list): A list of file paths to be added as timeline mattes.

        Returns:
            list: A list of MediaPoolItems created as timeline mattes.
        """
        return self.media_storage.AddTimelineMattesToMediaPool(paths)

class ProjectManager:
    def __init__(self, project_manager):
        """
        Initializes the ProjectManager class, wrapping the provided project manager object.

        Args:
            project_manager: The underlying ProjectManager object from DaVinci Resolve's API.
        """
        self.project_manager = project_manager

    def archive_project(
            self, project_name: str, file_path: str, is_archive_src_media: bool = True,
            is_archive_render_cache: bool = True, is_archive_proxy_media: bool = False
    ) -> bool:
        """
        Archives the project to the specified file path with the given options.

        Args:
            project_name (str): The name of the project to archive.
            file_path (str): The path to save the archived project.
            is_archive_src_media (bool): Whether to include source media in the archive. Defaults to True.
            is_archive_render_cache (bool): Whether to include render cache in the archive. Defaults to True.
            is_archive_proxy_media (bool): Whether to include proxy media in the archive. Defaults to False.

        Returns:
            bool: True if the project was successfully archived, False otherwise.
        """
        return self.project_manager.ArchiveProject(project_name, file_path, is_archive_src_media, is_archive_render_cache, is_archive_proxy_media)

    def create_project(self, project_name: str):
        """
        Creates and returns a new project if the name is unique.

        Args:
            project_name (str): The name of the new project.

        Returns:
            Project: The newly created project, or None if a project with the same name already exists.
        """
        return self.project_manager.CreateProject(project_name)

    def delete_project(self, project_name: str) -> bool:
        """
        Deletes the specified project in the current folder, if it is not currently loaded.

        Args:
            project_name (str): The name of the project to delete.

        Returns:
            bool: True if the project was successfully deleted, False otherwise.
        """
        return self.project_manager.DeleteProject(project_name)

    def load_project(self, project_name: str):
        """
        Loads and returns the project with the specified name.

        Args:
            project_name (str): The name of the project to load.

        Returns:
            Project: The loaded project, or None if no matching project is found.
        """
        return self.project_manager.LoadProject(project_name)

    def get_current_project(self):
        """
        Retrieves the currently loaded project.

        Returns:
            Project: The currently loaded project.
        """
        return self.project_manager.GetCurrentProject()

    def save_project(self) -> bool:
        """
        Saves the currently loaded project.

        Returns:
            bool: True if the project was successfully saved, False otherwise.
        """
        return self.project_manager.SaveProject()

    def close_project(self, project) -> bool:
        """
        Closes the specified project without saving.

        Args:
            project: The project to close.

        Returns:
            bool: True if the project was successfully closed, False otherwise.
        """
        return self.project_manager.CloseProject(project)

    def create_folder(self, folder_name: str) -> bool:
        """
        Creates a folder with the specified name in the current folder.

        Args:
            folder_name (str): The name of the folder to create.

        Returns:
            bool: True if the folder was successfully created, False otherwise.
        """
        return self.project_manager.CreateFolder(folder_name)

    def delete_folder(self, folder_name: str) -> bool:
        """
        Deletes the specified folder in the current directory.

        Args:
            folder_name (str): The name of the folder to delete.

        Returns:
            bool: True if the folder was successfully deleted, False otherwise.
        """
        return self.project_manager.DeleteFolder(folder_name)

    def get_project_list_in_current_folder(self) -> list:
        """
        Retrieves a list of project names in the current folder.

        Returns:
            list: A list of project names (strings) in the current folder.
        """
        return self.project_manager.GetProjectListInCurrentFolder()

    def get_folder_list_in_current_folder(self) -> list:
        """
        Retrieves a list of folder names in the current folder.

        Returns:
            list: A list of folder names (strings) in the current folder.
        """
        return self.project_manager.GetFolderListInCurrentFolder()

    def goto_root_folder(self) -> bool:
        """
        Navigates to the root folder in the database.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.project_manager.GotoRootFolder()

    def goto_parent_folder(self) -> bool:
        """
        Navigates to the parent folder of the current folder, if it exists.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self.project_manager.GotoParentFolder()

    def get_current_folder(self) -> str | None:
        """
        Returns the name of the current folder, or None if the folder is not set.

        Returns:
            str or none: The name of the current folder, or None if no folder is set.
        """
        return self.project_manager.GetCurrentFolder() or None

    def open_folder(self, folder_name: str) -> bool:
        """
        Opens the folder with the specified name.

        Args:
            folder_name (str): The name of the folder to open.

        Returns:
            bool: True if the folder was successfully opened, False otherwise.
        """
        return self.project_manager.OpenFolder(folder_name)

    def import_project(self, file_path: str, project_name: str = None) -> bool:
        """
        Imports a project from the specified file path.

        Args:
            file_path (str): The path of the project to import.
            project_name (str, optional): The name of the project to create upon import. Defaults to None.

        Returns:
            bool: True if the project was successfully imported, False otherwise.
        """
        return self.project_manager.ImportProject(file_path, project_name)

    def export_project(self, project_name: str, file_path: str, with_stills_and_luts: bool = True) -> bool:
        """
        Exports the specified project to the given file path.

        Args:
            project_name (str): The name of the project to export.
            file_path (str): The path to save the exported project.
            with_stills_and_luts (bool): Whether to include stills and LUTs in the export. Defaults to True.

        Returns:
            bool: True if the project was successfully exported, False otherwise.
        """
        return self.project_manager.ExportProject(project_name, file_path, with_stills_and_luts)

    def restore_project(self, file_path: str, project_name: str = None) -> bool:
        """
        Restores a project from the specified file path.

        Args:
            file_path (str): The path of the project to restore.
            project_name (str, optional): The name of the restored project. Defaults to None.

        Returns:
            bool: True if the project was successfully restored, False otherwise.
        """
        return self.project_manager.RestoreProject(file_path, project_name)

    def get_current_database(self) -> dict:
        """
        Retrieves information about the current database connection.

        Returns:
            dict: A dictionary containing information about the current database with keys 
                  'DbType', 'DbName', and optionally 'IpAddress'.
        """
        return self.project_manager.GetCurrentDatabase()

    def get_database_list(self) -> list:
        """
        Retrieves a list of databases added to DaVinci Resolve.

        Returns:
            list: A list of dictionaries, each containing database information.
        """
        return self.project_manager.GetDatabaseList()

    def set_current_database(self, db_info: dict) -> bool:
        """
        Switches the current database connection to the specified database.

        Args:
            db_info (dict): A dictionary with keys 'DbType', 'DbName', and optionally 'IpAddress'.

        Returns:
            bool: True if the database connection was successfully switched, False otherwise.
        """
        return self.project_manager.SetCurrentDatabase(db_info)

    def create_cloud_project(self, cloud_settings: dict):
        """
        Creates and returns a cloud project with the specified settings.

        Args:
            cloud_settings (dict): A dictionary containing cloud project settings.

        Returns:
            Project: The newly created cloud project.
        """
        return self.project_manager.CreateCloudProject(cloud_settings)

    def import_cloud_project(self, file_path: str, cloud_settings: dict) -> bool:
        """
        Imports a cloud project from the specified file path.

        Args:
            file_path (str): The path of the cloud project to import.
            cloud_settings (dict): A dictionary containing cloud project settings.

        Returns:
            bool: True if the cloud project was successfully imported, False otherwise.
        """
        return self.project_manager.ImportCloudProject(file_path, cloud_settings)

    def restore_cloud_project(self, folder_path: str, cloud_settings: dict) -> bool:
        """
        Restores a cloud project from the specified folder path.

        Args:
            folder_path (str): The path of the cloud project to restore.
            cloud_settings (dict): A dictionary containing cloud project settings.

        Returns:
            bool: True if the cloud project was successfully restored, False otherwise.
        """
        return self.project_manager.RestoreCloudProject(folder_path, cloud_settings)


