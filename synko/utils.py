# https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
import os
import sys

# import json
import yaml
from yaml.loader import Loader


def validate_config_path(configPaths):
    """
    0. get real path of all the paths
    1. check if all paths exists
    2. check if they are any duplicates in configPaths after getting real path
    """
    get_real_paths(configPaths)

    removed_config_paths = remove_non_existing_paths(configPaths)

    # showing warning for removed paths
    if len(removed_config_paths) > 0:
        for path in removed_config_paths:
            print(f'"{path}" not found\n')  # yellow

    # remove duplicates after getting real paths
    configPaths = set(configPaths)

    # remove paths which are not in home directory
    removed_paths_outside_home = remove_files_outside_home_dir(configPaths)

    # showing warning for removed paths
    if len(removed_config_paths) > 0:
        for path in removed_config_paths:
            print(f'"{path}" outside home directory\n')  # yellow


def remove_non_existing_paths(configPaths):
    """
    removes paths which do not exist
    args:
        configPaths (list)
    return:
        removed config paths (list)
    """
    non_existing_paths = list()

    for p in configPaths:
        if not os.path.exists(p):
            non_existing_paths.append(p)
            configPaths.remove(p)

    return non_existing_paths


def get_real_paths(configPaths):
    for i, p in enumerate(configPaths):
        configPaths[i] = os.path.realpath(configPaths[i])


def remove_files_outside_home_dir(configPaths):
    removed_path = list()
    homedir = os.path.expanduser("~")
    for p in configPaths:
        if not p.startswith(homedir):
            removed_path.append(p)
            configPaths.remove(p)


def write_yml_file(data, filepath):
    try:
        with open(filepath, "w") as f:
            yaml.dump(data, f)
    except Exception as e:
        print(e)


def read_yml_file(filepath, default_data={}):
    with open(filepath, "a+") as f:
        try:

            file_size = os.stat(filepath).st_size

            if file_size == 0:
                yaml.safe_dump(default_data, f)
                data = default_data
            else:
                f.seek(0)
                data = yaml.safe_load(f)

        except yaml.YAMLError as exc:
            print(exc)

    return data


# TODO: red color
def error(msg):
    print(msg)
    sys.exit(1)


# TODO: yellow color
def warn(msg):
    print(msg)
