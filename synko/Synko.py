import os
import sys
import uuid
import utils
import platform

from constants import (
    APP_DATA_DIR,
    APP_DATA_FILE,
    STORAGE_DIR,
    SYNKO_STORAGE_DIR,
    SYNKO_TRACK_FILE,
)


class Synko:
    def __init__(self):
        # default metadata
        self.__metadata = dict()
        self.__metadata["APP_DATA_DIR"] = APP_DATA_DIR
        self.__metadata["APP_DATA_FILE"] = APP_DATA_FILE
        self.__metadata["SYNKO_TRACK_FILE"] = SYNKO_TRACK_FILE
        self.__metadata["SYNKO_STORAGE_DIR"] = SYNKO_STORAGE_DIR  # storage/synkon
        self.__metadata["SYNKO_DEVICE_ID"] = ""

        # app data
        self.__appdata = dict()
        self.__appdata["PLATFORM"] = platform.system()
        self.__appdata["UID"] = str(uuid.uuid4())
        self.__appdata["STORAGE_NAME"] = "Dropbox"
        self.__appdata["STORAGE_DIR"] = STORAGE_DIR  # dropboxstorage directory ig?

        # track data
        self.__trackdata = dict()

    # TODO: init app
    def init_app(self):
        """initialize synko before command execution"""

        # App data directory exists? no : create one
        os.makedirs(self.__metadata["APP_DATA_DIR"], exist_ok=True)

        # read app data.if not exists, create one
        # populate empty file with default data
        self.__appdata = utils.read_yml_file(
            self.__metadata["APP_DATA_FILE"], self.__appdata
        )

        # set device id
        self.__metadata[
            "SYNKO_DEVICE_ID"
        ] = f'{self.__appdata["PLATFORM"]}~{self.__appdata["UID"]}'

        # if storage path exists (dropbox path)
        # TODO: need to elaborate error msg
        if not os.path.exists(self.__appdata["STORAGE_DIR"]):
            utils.error(
                f'storage directory "{self.__appdata["STORAGE_DIR"]}" for "{self.__metadata["STORAGE_NAME"]}"'
            )

        # synko storage dir exists? no: create one
        # synko storage dir is dropbox_path/synko
        os.makedirs(self.__metadata["SYNKO_STORAGE_DIR"], exist_ok=True)

        # read track data, if does not exist create one
        self.__trackdata = self.__load_tracking_file()

        # all good to go

    # TODO: update storage dir
    def update_storage(self, name=None, dir=None):
        name = name or self.__appdata["STORAGE_DIR"]
        dir = dir or self.__appdata["STORAGE_NAME"]
        utils.write_yml_file(self.__appdata, self.__metadata["APP_DATA_FILE"])

    # TODO: get app data
    def get_appdata(self):
        return self.__appdata

    # TODO: update track data
    def get_track_data(self):
        return self.__trackdata

    def display_track_data(self):
        device_id = self.device_id()
        track_data = self.get_track_data()

        for config in track_data:
            if track_data[config][device_id] is not None:
                print(f"[>] {config}")

                for config_path in track_data[config][device_id]:
                    print(f"[*] {config_path}")

    def check_duplicate_paths(self, configname, file_paths):
        """
        - checks if provided path already exists in track_data

        Args:
            file_paths (list): list of file paths to configs
        """
        found = 0
        device_id = self.device_id()
        track_data = self.get_track_data()

        for config in track_data:
            existing_paths = track_data[config][device_id] or []
            for p in existing_paths:
                if p in file_paths:
                    found += 1
                    # red
                    print(f"[x] '{p}' is already added for sync under '{config}' !")

        if found > 0:
            sys.exit(0)

    def get_metadata(self):
        return self.__metadata

    # TODO: update track data
    def update_track_data(self, trackdata):
        self.__trackdata = trackdata
        # write to file
        self.__update_track_file()

    def __load_tracking_file(self):
        """
        reads track file and expands all the config path
        """
        device_id = self.device_id()
        track_data = utils.read_yml_file(self.__metadata["SYNKO_TRACK_FILE"])

        if len(track_data) > 0:
            for config in track_data:
                if track_data[config][device_id] is not None:
                    utils.expand_all_paths(track_data[config][device_id])

        return track_data

    def __update_track_file(self):
        """
        updates track file with data and also shortens the path
        """
        track_data = self.__trackdata
        device_id = self.device_id()

        if len(track_data) > 0:
            for config in track_data:
                utils.shorten_all_paths(track_data[config][device_id])

        # write to file
        utils.write_yml_file(track_data, self.__metadata["SYNKO_TRACK_FILE"])

    def device_id(self):
        return self.__metadata["SYNKO_DEVICE_ID"]
