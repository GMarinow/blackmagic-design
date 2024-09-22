from .core import DaVinciResolveScript as bmd


class Resolve:
    def __init__(self, app: str = 'Resolve'):
        self.app = bmd.scriptapp(app)
        self.media_storage = MediaStorage(self.app.GetMediaStorage())

    def get_media_storage(self):
        """Returns the MediaStorage wrapper class."""
        return self.media_storage
    
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




