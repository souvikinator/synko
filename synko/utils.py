# https://stackoverflow.com/questions/898669/how-can-i-detect-if-a-file-is-binary-non-text-in-python
import os
import re
import sys
import shutil
import yaml
import inquirer

from synko.constants import APP_DATA_DIR


def ask_question(msg, key, validator):
    questions = [
        inquirer.Text(
            key,
            message=msg,
            validate=validator,
        ),
    ]

    answers = inquirer.prompt(questions)
    if answers is None or answers[key] is None:
        sys.exit(1)

    return answers[key]


def is_valid_storage_path(answers, storage_path):
    if not os.path.isdir(storage_path):
        raise inquirer.errors.ValidationError("", "storage path must be a directory")

    if is_path_in_app_data_dir(storage_path, APP_DATA_DIR):
        return inquirer.errors.ValidationError(
            "", f"'{storage_path}' is not a valid storage path as it is used by Synko"
        )

    return True


def is_valid_device_name(answers, device_name):
    if not re.match("^[a-zA-Z0-9]*$", device_name):
        raise inquirer.errors.ValidationError(
            "", f"device name can only be alphanumeric with no spaces"
        )

    return True


def remove_paths_in_storage_dir(config_paths, synko_storage_dir):
    """
    - removes paths from provided lists which are inside dropbox/synko

    Returns:
        `removed_paths (list)`: list of paths from config_paths which were removed
        `tmp_paths (list)`: list of paths from config_paths which were not removed
    """
    tmp_paths = []
    removed_paths = []

    for p in config_paths:
        if is_path_in_storage_dir(p, synko_storage_dir):
            removed_paths.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, removed_paths


def remove_paths_in_app_data_dir(config_paths, app_data_dir):
    """
    - removes paths (among config_paths) which are inside ~/.synko/

    Returns:
        `removed_paths (list)`: list of paths from config_paths which were removed
        `tmp_paths (list)`: list of paths from config_paths which were not removed
    """
    removed_paths = []
    tmp_paths = []

    for p in config_paths:
        if is_path_in_app_data_dir(p, app_data_dir):
            removed_paths.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, removed_paths


def is_path_in_storage_dir(config_path, synko_storage_dir):
    """
    checks if a path is in the synko storage directory

    Args:
        `config_path` (str),
        `synko_storage_dir` (str)
    """
    return synko_storage_dir in config_path


def is_path_in_app_data_dir(config_path, app_data_dir):
    return app_data_dir in config_path


def remove_non_existing_paths(config_paths):
    """
    - removes paths which do not exist

    args:
        `config_paths` (list)

    Returns:
        `removed_paths` (list): list of paths from config_paths which were removed
        `tmp_paths` (list): list of paths from config_paths which were not removed
    """
    non_existing_paths = []
    tmp_paths = []
    for p in config_paths:
        if not os.path.exists(p):
            non_existing_paths.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, non_existing_paths


def get_real_paths(config_paths):
    """updates paths in config_paths to their real path"""
    for i, p in enumerate(config_paths):
        config_paths[i] = os.path.realpath(p)


def remove_paths_outside_home_dir(config_paths):
    """
    - removes paths which are outside the home dir

    NOTE: at this point synko only allows configs inside the home dir only

    Returns:
        removed_paths (list): list of paths from config_paths which were removed
        tmp_paths (list): list of paths from config_paths which were not removed
    """
    removed_path = []
    tmp_paths = []
    homedir = os.path.expanduser("~")

    for p in config_paths:
        if not p.startswith(homedir):
            removed_path.append(p)
        else:
            tmp_paths.append(p)

    return tmp_paths, removed_path


def write_yml_file(data, filepath):
    """write data to yaml file"""
    try:
        with open(filepath, "w") as f:
            yaml.dump(data, f)
    except yaml.YAMLError as e:
        print(e)
        error("Error writing yaml file!")
    except FileExistsError as e:
        print(e)
        error(f"{filepath} not found")
    except Exception as e:
        error(e)


def read_yml_file(filepath, default_data={}):
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
        except FileNotFoundError:
            error(f"File {filepath} not found.  Aborting")
        except OSError:
            error(f"OS error occurred trying to open {filepath}")
        except yaml.YAMLError:
            error(f"Error occurred while reading YAML file {filepath}")
        except Exception as err:
            error(f"Unexpected error opening {filepath} is, {err}")

    return data


def expand_all_paths(file_paths):
    """
    - expands ~ to home directory in list of paths
    - calls `expand_path()` internally

    Args:
        `file_paths` (list) : list of paths to expand
    """
    for i, fp in enumerate(file_paths):
        file_paths[i] = expand_path(fp)


def shorten_all_paths(file_paths):
    """
    - expands home directory to ~ in list of paths
    - calls `shoten_path()` internally

    Args:
        `file_paths` (list) : list of paths to shorten
    """
    for i, fp in enumerate(file_paths):
        file_paths[i] = shorten_path(fp)


def expand_path(file_path):
    """- expand ~ -> home directory in any path"""
    return file_path.replace("~", os.path.expanduser("~"))


def shorten_path(file_path):
    """- expand home directory to ~ in any path"""
    return file_path.replace(os.path.expanduser("~"), "~")


def generate_link_path(src_path, config_name, synko_storage_dir):
    """- generate backup file path using the original file path"""
    base_name = os.path.basename(src_path)
    return os.path.join(synko_storage_dir, config_name, base_name)


def select_option(msg, options):
    """- select only one option prompt"""
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
    return None


def select_options(msg, options):
    """- select many options prompt"""
    option_count = len(options)
    if option_count == 0:
        return []

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
    return []


def delete_path(path):
    """delete file/dir"""
    if os.path.isdir(path):
        shutil.rmtree(path)
    elif os.path.isfile(path):
        os.remove(path)


def copy_path(src, dest):
    """copy file/dir from src to dest"""
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
        `link_to (str)`: path where src will be moved to (backup path)
    """
    if os.path.exists(src) and os.path.realpath(src) == link_to:
        # delete src
        os.remove(src)
        # copy link_to to src
        copy_path(link_to, src)


def delete_backup(filepath, config_name, synko_storage_dir):
    """
    - generate backup file path (link_to) from filepath arg and delete

    Args:
        `filepath`: path to origin file
        `synko_storage_dir`: path to synko storage directory
    """
    link_to = generate_link_path(filepath, config_name, synko_storage_dir)
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
