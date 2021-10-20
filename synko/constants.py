""" contains all synko specific constants """

import os

APP_NAME = "synko"
APP_VERISON = "0.9.0"

# user specific consts
USER_HOME_DIR = os.path.expanduser("~")

# synko specific directories
APP_DATA_DIR = os.path.join(USER_HOME_DIR, f".{APP_NAME}")
APP_DATA_FILE = os.path.join(APP_DATA_DIR, "data.yml")

STORAGE_NAME = "Dropbox"
STORAGE_DIR = os.path.join(USER_HOME_DIR, "Dropbox")
SYNKO_STORAGE_DIR = "synko"
SYNKO_TRACK_FILE = ".track"


SYNKO_BANNER = f"""        
 __  .._ ;_/ _ 
_) \_|[ )| \(_)
   ._|          v{APP_VERISON}
"""

SYNKO_ABOUT = """Sync application configurations and settings across multiple devices
currently supports linux and macos, working in progress for windows
more details: https://github.com/souvikinator/synko
"""

USAGE_DETAILS = """Usage: synko [options] [command] [args]

Commands:

 add	add configuration to synko, first argument is name of config followed by path to config files
 remove  remove configuration from synko, takes config name as argument
 index	list all configurations added to synko
 info	   list info related to synko (platform, device_id, storage name and storage path)
 reset	reverts synko's settings to default, unregisters current device and removes all files added for sync 

To know mode about specific command: synko [command] --help

Options:

--help      show this message and exit
--version   show version number


for detailed usage guide, go to https://github.com/souvikinator/synko#-how-to-use
"""

# error and warning messages

SYNKO_ADD_CONFLICT = """CONFLICT!
Looks like backup file of '{path}' already exists on this device 
and may have different content than the one on another device!

[0] This will possibly sync data of '{path}' on this device to another device

[1] This will possibly sync data from another device with '{path}' on this device

For more information select abort
visit https://github.com/souvikinator/synko/blob/master/README.md#add .
"""

STORAGE_DIR_NOT_FOUND = """storage directory '{storagepath}' not found! 

for more info checkout https://github.com/souvikinator/synko/blob/master/README.md#info
"""
