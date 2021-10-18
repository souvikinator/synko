import os
import sys
import uuid
import platform

from synko import utils

from synko.constants import (
    APP_DATA_DIR,
    APP_DATA_FILE,
    STORAGE_DIR,
    SYNKO_STORAGE_DIR,
    SYNKO_TRACK_FILE,
    STORAGE_DIR_NOT_FOUND,
)


class Synko:
    def __init__(self):

        # default app data
        self.__appdata = {}
        self.__appdata["PLATFORM"] = platform.system()
        self.__appdata["DEVICE_NAME"] = ""
        self.__appdata["STORAGE_DIR"] = STORAGE_DIR
        self.__appdata["SYNKO_STORAGE_DIR"] = os.path.join(
            STORAGE_DIR, SYNKO_STORAGE_DIR
        )
        self.__appdata["SYNKO_TRACK_FILE"] = os.path.join(
            self.__appdata["SYNKO_STORAGE_DIR"], SYNKO_TRACK_FILE
        )

        # default metadata
        self.__metadata = {}
        self.__metadata["APP_DATA_DIR"] = APP_DATA_DIR
        self.__metadata["APP_DATA_FILE"] = APP_DATA_FILE

        # track data
        self.__trackdata = {}

    # init app
    def init_app(self):
        """initialize synko before command execution"""

        # App data directory exists? no : create one
        os.makedirs(self.__metadata["APP_DATA_DIR"], exist_ok=True)

        # warn: storage path does not exist, and take input from user
        if not os.path.exists(STORAGE_DIR):
            utils.info(STORAGE_DIR_NOT_FOUND.format(storagepath=STORAGE_DIR))

            # ask user to enter one
            storage_path = utils.ask_question(
                "Enter storage path", "storage", utils.is_valid_storage_path
            )
            storage_path = os.path.realpath(storage_path)
            self.update_storage_path(storage_path)

        # load data from track file, if does not exist create file
        self.__trackdata = self.__load_tracking_file()

        # read app data and set storage dir and track file path
        self.__appdata = self.__load_app_data()

        # check if device name is assigned
        if len(self.__appdata["DEVICE_NAME"]) == 0:
            # TODO: give a info message
            self.set_device_name()

        # write to app data file
        self.update_app_data_file()

        # all good to go

    def __load_app_data(self):
        data = utils.read_yml_file(self.__metadata["APP_DATA_FILE"], self.__appdata)

        return data

    def __load_tracking_file(self):
        """
        reads track file and expands all the config path
        """
        track_data = utils.read_yml_file(self.__appdata["SYNKO_TRACK_FILE"])

        if len(track_data) > 0:
            for config in track_data:
                for device_id in track_data[config]:
                    utils.expand_all_paths(track_data[config][device_id])

        return track_data

    def __update_track_file(self):
        """
        updates track file with data and also shortens the path
        """
        track_data = self.__trackdata

        if len(track_data) > 0:
            for config in track_data:
                for device_id in track_data[config]:
                    utils.shorten_all_paths(track_data[config][device_id])

        # write to file
        utils.write_yml_file(track_data, self.__appdata["SYNKO_TRACK_FILE"])

    def set_device_name(self):
        # ask for device name
        device_name = utils.ask_question(
            "Enter device name", "device_name", utils.is_valid_device_name
        )
        if self.is_duplicate_device_name(device_name):
            utils.error(f"device name {device_name} is already in use!")
        self.update_device_name(device_name)

    def update_device_name(self, device_name):
        self.__appdata["DEVICE_NAME"] = device_name

    def get_device_list(self):
        device_list = []
        for config in self.__trackdata:
            for device in self.__trackdata[config]:
                device_list.append(device)

        return list(set(device_list))

    def get_metadata(self):
        return self.__metadata

    def get_storage_dir(self):
        return self.__appdata["SYNKO_STORAGE_DIR"]

    # update track data
    def update_track_data(self, trackdata):
        self.__trackdata = trackdata
        # write to file
        self.__update_track_file()

    def device_id(self):
        return self.__metadata["SYNKO_DEVICE_ID"]

    def display_synko_info(self):
        """displays synko data/info"""
        for key in self.__appdata:
            if key not in ("SYNKO_STORAGE_DIR", "SYNKO_TRACK_FILE"):
                utils.info(f"{key} : {self.__appdata[key]}")

    def get_appdata(self):
        """get app data"""
        return self.__appdata

    def get_track_data(self):
        """get track file data"""
        return self.__trackdata

    def display_track_data(self):
        """display track data related to current device"""
        device_id = self.device_id()
        track_data = self.get_track_data()
        found = 0
        for config in track_data:
            if device_id in track_data[config]:
                found += 1
                print(f"[+] {config}")  # TODO: orange (only the config not [+])

                for config_path in track_data[config][device_id]:
                    print(
                        f" |__ {config_path}"
                    )  # TODO: cyan (only config_path not |__ )
                print("\n")

        if not found:
            utils.error("Nothing to list")

    # update storage dir
    def update_storage_path(self, dirpath=None):
        if dirpath is not None:
            self.__appdata["STORAGE_DIR"] = dirpath
            self.__appdata["SYNKO_STORAGE_DIR"] = os.path.join(
                self.__appdata["STORAGE_DIR"], SYNKO_STORAGE_DIR
            )
            self.__appdata["SYNKO_TRACK_FILE"] = os.path.join(
                self.__appdata["SYNKO_STORAGE_DIR"], SYNKO_TRACK_FILE
            )

    def update_app_data_file(self):
        utils.write_yml_file(self.__appdata, self.__metadata["APP_DATA_FILE"])

    def is_duplicate_device_name(self, device_name):
        device_list = self.get_device_list()
        return device_name in device_list

    def check_duplicate_paths(self, file_paths):
        """
        - checks if provided path already exists in track_data

        Args:
            file_paths (list): list of file paths to configs
        """
        found = 0
        device_id = self.device_id()
        track_data = self.get_track_data()

        for config in track_data:
            if device_id in track_data[config]:
                existing_paths = track_data[config][device_id] or []
                for p in existing_paths:
                    if p in file_paths:
                        found += 1
                        utils.warn(f"'{p}' is already added for sync under '{config}'")

        if found > 0:
            utils.error("aborting!")

    def validate_config_paths(self, config_paths):
        """
        working:
            - remove path which do not exist
            - get real path and remove duplicates
            - remove paths which are outside home dir

        args:
            config_paths (list)
        """
        synko_storage_dir = self.__appdata["SYNKO_STORAGE_DIR"]

        utils.get_real_paths(config_paths)

        # remove paths which do not exist
        config_paths, removed_paths = utils.remove_non_existing_paths(config_paths)

        # showing warning for removed paths
        if len(removed_paths) > 0:
            for path in removed_paths:
                utils.warn(f"'{path}' not found")
            sys.exit(0)

        # get real path, of each path
        utils.get_real_paths(config_paths)

        # remove duplicates after getting real paths
        config_paths = list(set(config_paths))

        # remove paths which are not in home directory
        # for now it only allows config files within home dir
        config_paths, removed_paths = utils.remove_paths_outside_home_dir(config_paths)

        # showing warning for removed paths
        if len(removed_paths) > 0:
            for path in removed_paths:
                utils.warn(f"'{path}' outside home directory, cannot be used")
            sys.exit(0)

        # remove paths which are inside dropbox/synko
        config_paths, removed_paths = utils.remove_paths_in_storage_dir(
            config_paths, synko_storage_dir
        )

        # showing warning for removed paths
        if len(removed_paths) > 0:
            for path in removed_paths:
                utils.warn(f"'{path}' cannot be used as it is used by synko")
            sys.exit(0)

        # removed paths which are inside app data directory (.synko)
        config_paths, removed_paths = utils.remove_paths_in_app_data_dir(
            config_paths, APP_DATA_DIR
        )

        # showing warning for removed paths
        if len(removed_paths) > 0:
            for path in removed_paths:
                utils.warn(f"'{path}' cannot be used as it is used by synko")  # yellow
            sys.exit(0)

        # boom! all done ig?
