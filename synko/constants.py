import os

APP_NAME = "synko"
APP_VERISON = "0.0.1"

# user specific consts
USER_HOME_DIR = os.path.expanduser("~")

# synko specific directories
APP_DATA_DIR = os.path.join(USER_HOME_DIR, f".{APP_NAME}")
APP_DATA_FILE = os.path.join(APP_DATA_DIR, "data.yml")

STORAGE_NAME = "Dropbox"
STORAGE_DIR = os.path.join(USER_HOME_DIR, "Dropbox")
SYNKO_STORAGE_DIR = os.path.join(STORAGE_DIR, "synko")
SYNKO_TRACK_FILE = os.path.join(SYNKO_STORAGE_DIR, ".track")
