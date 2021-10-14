# https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
import os
import sys
import yaml
import shutil
import inquirer
from constants import APP_DATA_DIR, SYNKO_STORAGE_DIR


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
    configPaths, removed_paths = remove_non_existing_paths(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            warn(f"'{path}' not found")
        sys.exit(0)

    # get real path, of each path
    get_real_paths(configPaths)

    # remove duplicates after getting real paths
    configPaths = list(set(configPaths))

    # remove paths which are not in home directory
    # for now it only allows config files within home dir
    configPaths, removed_paths = remove_paths_outside_home_dir(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            warn(f"'{path}' outside home directory, cannot be used")
        sys.exit(0)

    # remove paths which are inside dropbox/synko
    configPaths, removed_paths = remove_paths_in_storage_dir(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            warn(f"'{path}' cannot be used as it is used by synko")
        sys.exit(0)

    # removed paths which are inside app data directory (.synko)
    configPaths, removed_paths = remove_paths_in_app_data_dir(configPaths)

    # showing warning for removed paths
    if len(removed_paths) > 0:
        for path in removed_paths:
            warn(f"'{path}' cannot be used as it is used by synko")  # yellow
        sys.exit(0)

    # boom! all done ig?


def remove_paths_in_storage_dir(configPaths):
    """
    - removes paths from provided lists which are inside dropbox/synko

    Returns:
        `removed_paths (list)`: list of paths from configPaths which were removed
        `tmp_paths (list)`: list of paths from configPaths which were not removed
    """
    removed_paths = list()
    tmp_paths = list()

    for p in configPaths:
        if is_path_in_storage_dir(p):
            removed_paths.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, removed_paths


def remove_paths_in_app_data_dir(configPaths):
    """
    - removes paths (among configPaths) which are inside ~/.synko/

    Returns:
        `removed_paths (list)`: list of paths from configPaths which were removed
        `tmp_paths (list)`: list of paths from configPaths which were not removed
    """
    removed_paths = list()
    tmp_paths = list()

    for p in configPaths:
        if is_path_in_app_data_dir(p):
            removed_paths.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, removed_paths


def is_path_in_storage_dir(configPath):
    return SYNKO_STORAGE_DIR in configPath


def is_path_in_app_data_dir(configPath):
    return APP_DATA_DIR in configPath


def remove_non_existing_paths(configPaths):
    """
    - removes paths which do not exist

    args:
        configPaths (list)

    Returns:
        `removed_paths (list)`: list of paths from configPaths which were removed
        `tmp_paths (list)`: list of paths from configPaths which were not removed
    """
    non_existing_paths = list()
    tmp_paths = list()
    for p in configPaths:
        if not os.path.exists(p):
            non_existing_paths.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, non_existing_paths


def get_real_paths(configPaths):
    for i, p in enumerate(configPaths):
        configPaths[i] = os.path.realpath(p)


def remove_paths_outside_home_dir(configPaths):
    """
    - removes paths which are outside the home dir

    NOTE: at this point synko only allows configs inside the home dir

    Returns:
        removed_paths (list): list of paths from configPaths which were removed
        tmp_paths (list): list of paths from configPaths which were not removed
    """
    removed_path = list()
    tmp_paths = list()
    homedir = os.path.expanduser("~")

    for p in configPaths:
        if not p.startswith(homedir):
            removed_path.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, removed_path


def write_yml_file(data, filepath):
    try:
        with open(filepath, "w") as f:
            yaml.dump(data, f)
    except Exception as e:
        error(e)


def read_yml_file(filepath, default_data=dict()):
    """
    - creates yml file (if not exists) and writes default data
    - else reads and returns data
    """
    with open(filepath, "a+") as f:
        try:

            file_size = os.stat(filepath).st_size

            if file_size == 0:
                yaml.safe_dump(default_data, f)
                data = default_data
            else:
                f.seek(0)
                data = yaml.safe_load(f)

        except Exception as exc:
            error(exc)

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


# TODO: handle keyboard interupt
def select_option(msg, options):
    """select only one"""
    option_count = len(options)
    if option_count == 0:
        return None

    questions = [
        inquirer.List(
            "x",
            message=msg,
            choices=options,
        ),
    ]

    selected_option = inquirer.prompt(questions)
    if selected_option is not None:
        return selected_option["x"]
    else:
        return None


# TODO: handle keyboard interupt
def select_options(msg, options):
    """select many options"""
    option_count = len(options)
    if option_count == 0:
        return ()

    questions = [
        inquirer.Checkbox(
            "x",
            message=msg,
            choices=options,
        ),
    ]

    selected_options = inquirer.prompt(questions)
    if selected_options is not None:
        return selected_options["x"]
    else:
        return []


def link_all(paths):
    """
    - calls `link()` on each paths

    Args:
        `paths (list)`: list of config paths

    `TODO:` chmod on link_to
    if link_to is file: chmod 600
    if link_to is folder: chmod 700
    """
    for p in paths:
        link_to = generate_link_path(p)
        link(p, link_to)


def delete_path(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def copy_path(src, dest):
    if os.path.isdir(src):
        shutil.copytree(src, dest)
    elif os.path.isfile(src):
        shutil.copy(src, dest)


def link(src, link_to, mode=0):
    """
    - if mode is 0 remove link_to then perform symlink
    - if mode is 1 remove src then perform symlink
    - moves src to link_to
    - perform symlink

    Args:
        `src (str)`: path to original file
        `link_to (str)`: path where src will be moved to
    """
    if mode == 1:
        delete_path(src)
    else:
        delete_path(link_to)
        # move src to link_to
        shutil.move(src, link_to)

    # symlink link_to <- src
    os.symlink(link_to, src)


def unlink(src, link_to):
    """
    - check if src exists?
    - resolve(src) == link_to?
        - yes: delete src, copy link_to to src
    - else return

    Args:
        `src (str)`: path to original file
        `link_to (str)`: path where src will be moved to
    """
    if os.path.exists(src) and os.path.realpath(src) == link_to:
        # delete src
        os.remove(src)
        # copy link_to to src
        copy_path(link_to, src)


def delete_backup(p):
    """delete backup file"""
    link_to = generate_link_path(p)
    delete_path(link_to)


# TODO: red and bold
def error(msg):
    sys.exit(f"[✕] {msg}")


# TODO: yellow and bold
def warn(msg):
    print(f"[!] {msg}")


# TODO: green and bold
def success(msg):
    print(f"[✓] {msg}")


# TODO: cyan and bold
def info(msg):
    print(f"[i] {msg}")


# def unlink_all(paths):
#     """
#     - calls `unlink()` on each paths

#     Args:
#         `paths (list)`: list of config paths
#     """
#     for p in paths:
#         link_to = generate_link_path(p)
#         unlink(p, link_to)

# def delete_backups(paths):
#     """calls `delete_backup()` on each path"""
#     if len(paths) == 0:
#         return

#     for p in paths:
#         delete_backup(p)
