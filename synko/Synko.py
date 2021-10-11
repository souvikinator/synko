import os
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
        # TODO: last accessed
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
        self.__trackdata = utils.read_yml_file(self.__metadata["SYNKO_TRACK_FILE"])

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

    def get_metadata(self):
        return self.__metadata

    # TODO: update track data
    def update_track_data(self, trackdata):
        pass
