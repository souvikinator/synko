# https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
import os
import sys
from constants import APP_DATA_DIR, SYNKO_STORAGE_DIR
import yaml


def validate_config_paths(configPaths):
    """
    working:
        - remove path which do not exist
        - get real path and remove duplicates
        - remove paths which are outside home dir

    args:
        configPaths (list)
    """
    get_real_paths(configPaths)

    # remove paths which do not exist
    removed_paths = remove_non_existing_paths(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            print(f'"{path}" not found\n')  # yellow

    # get real path, of each path
    get_real_paths(configPaths)

    # remove duplicates after getting real paths
    configPaths = list(set(configPaths))

    # remove paths which are not in home directory
    # for now it only allows config files within home dir
    removed_paths = remove_paths_outside_home_dir(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            print(f"[!] '{path}' outside home directory, cannot be used\n")  # yellow

    # remove paths which are inside dropbox/synko
    removed_paths = remove_paths_in_storage_directory(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            print(f"[!] '{path}' cannot be used as it is used by synko\n")  # yellow

    # removed paths which are inside app data directory (.synko)
    removed_paths = remove_paths_in_app_data_dir(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            print(f"[!] '{path}' cannot be used as it is used by synko\n")  # yellow

    # boom! all done ig?


def remove_paths_in_storage_directory(configPaths):
    """
    removes paths which are inside dropbox/synko
    """
    removed_paths = list()

    for p in configPaths:
        if SYNKO_STORAGE_DIR in p:
            removed_paths.append(p)
            configPaths.remove(p)

    return removed_paths


def remove_paths_in_app_data_dir(configPaths):
    """
    removes paths which are inside dropbox/synko
    """
    removed_paths = list()

    for p in configPaths:
        if APP_DATA_DIR in p:
            removed_paths.append(p)
            configPaths.remove(p)

    return removed_paths


def remove_non_existing_paths(configPaths):
    """
    - removes paths which do not exist

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
        configPaths[i] = os.path.realpath(p)


def remove_paths_outside_home_dir(configPaths):
    removed_path = list()
    homedir = os.path.expanduser("~")
    for p in configPaths:
        if not p.startswith(homedir):
            removed_path.append(p)
            configPaths.remove(p)

    return removed_path


def write_yml_file(data, filepath):
    try:
        with open(filepath, "w") as f:
            yaml.dump(data, f)
    except Exception as e:
        print(e)


def read_yml_file(filepath, default_data=dict()):
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


def expand_all_paths(file_paths):
    """
    expands ~ to home directory in list of paths

    Args:
        file_paths (list) : list of paths to expand
    """
    for i, fp in enumerate(file_paths):
        file_paths[i] = expand_path(fp)


def shorten_all_paths(file_paths):
    """
    expands home directory to ~ in list of paths

    Args:
        file_paths (list) : list of paths to shorten
    """
    for i, fp in enumerate(file_paths):
        file_paths[i] = shorten_path(fp)


def expand_path(file_path):
    """
    expand ~ -> home directory in any path

    Args:
        file_path (str)

    Return:
        expanded_path (str)
    """
    return file_path.replace("~", os.path.expanduser("~"))


def shorten_path(file_path):
    """
    expand home directory to ~ in any path

    Args:
        file_path (str)

    Return:
        expanded_path (str)
    """
    return file_path.replace(os.path.expanduser("~"), "~")


def generate_link_path(src_path):
    """about function"""
    base_name = os.path.basename(src_path)
    return os.path.join(SYNKO_STORAGE_DIR, base_name)


def link_all(paths):
    """about function"""
    for p in paths:
        link_to = generate_link_path()
        link(paths, link_to)
        # TODO: chmod


def link(src, link_to):
    """
    1. check if link_to exists
        not? create one and link
        yes? delete link_to
    2. perform symlink

    """
    pass


# TODO: red color
def error(msg):
    print(msg)
    sys.exit(1)


# TODO: yellow color
def warn(msg):
    print(msg)
