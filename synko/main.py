#!/usr/bin/python3
import os
import click

from synko import utils
from synko.app import Synko
from synko.constants import (
    APP_DATA_DIR,
    APP_NAME,
    APP_VERISON,
    SYNKO_ADD_CONFLICT,
    USAGE_DETAILS,
    SYNKO_BANNER,
    SYNKO_ABOUT,
)


App = Synko()


class HelpfulCmd(click.Group):
    def format_help(self, ctx, formatter):
        print(SYNKO_BANNER)
        print(SYNKO_ABOUT)
        print(USAGE_DETAILS)


@click.group(cls=HelpfulCmd)
@click.version_option(version=APP_VERISON, prog_name=APP_NAME)
def main():
    """CLI entry point"""
    print(SYNKO_BANNER)
    # initialize app here
    App.init_app()


# add command
@main.command()
@click.argument("paths", nargs=-1)
@click.option("-c", "--config-name", type=str, required=True, prompt=True)
def add(config_name, paths):
    """
    add configuration path for syncing
    """
    paths = list(set(paths))
    track_data = App.get_track_data()
    app_data = App.get_appdata()
    device_name = App.device_name()

    if len(paths) == 0:
        utils.error("no paths specified!")

    if len(config_name) == 0:
        utils.error("config-name must be specified")

    # perform various checks and validate
    App.validate_config_paths(paths)

    # check if paths already exists in track file?
    App.check_duplicate_paths(paths)

    # create folder named config_name in synko_storage_dir
    config_folder = os.path.join(app_data["SYNKO_STORAGE_DIR"], config_name)
    os.makedirs(config_folder, exist_ok=True)

    # form links and update track data
    for p in paths:
        selected_mode = 0
        link_to = utils.generate_link_path(
            p, config_name, app_data["SYNKO_STORAGE_DIR"]
        )

        if os.path.exists(link_to):

            if (os.path.isfile(p) and os.stat(p).st_size == 0) or (
                os.path.isdir(p) and not any(os.scandir(p))
            ):
                selected_mode = 1

            # if link_to exists and original file/dir is not empty, then ask for confirmation
            elif (os.path.isfile(p) and os.stat(p).st_size > 0) or (
                os.path.isdir(p) and any(os.scandir(p))
            ):
                # CONFLICT! let user select the best
                utils.warn(SYNKO_ADD_CONFLICT.format(path=p))
                selected_mode = utils.select_option(
                    "Select option", [0, 1, "skip", "abort"]
                )

        if selected_mode == "abort":
            utils.warn("aborted!")
            break

        if selected_mode == "skip":
            utils.warn(f"skipped {p}")
            continue

        track_data.setdefault(device_name, {})
        track_data[device_name].setdefault(config_name, [])

        utils.link(p, link_to, selected_mode)
        track_data[device_name][config_name].append(p)
        utils.success(f"added {p}")

    # write track data to track file
    App.update_track_data(track_data)

    utils.success("done!")


# index command
# TODO: allow users to enter config name and display
# configs only of that specific configuration
@main.command()
@click.option(
    "-c",
    "--config-name",
    type=str,
    required=False,
)
def index(config_name):
    """list all the donfig files added to synko"""
    # TODO: pass name as arg below if config_name is not None
    App.display_track_data()


# remove command
@main.command()
@click.option("-c", "--config-name", type=str, required=False)
@click.option("-a", "--all-config", is_flag=True, default=False)
def remove(config_name, all_config):
    """
    remove specific config file or all config files from synko

    usage:
        `synko remove --config-name=[configname]`: to remove files in provided configname (select from dropdown)
        `synko remove -a/--all-config`: to remove all config added to synko in current device
    """
    track_data = App.get_track_data()
    synko_storage_dir = App.get_storage_dir()
    device_name = App.device_name()

    to_be_removed_paths = []
    tmp_current_device_track_data = {}

    if all_config and config_name is not None:
        utils.error("-a/--all-config and -c/--config-name can't be used together!")

    # if no options is provided
    if not all_config and config_name is None:
        utils.error("no options provided!")

    if config_name is not None:

        if device_name not in track_data:
            utils.error(f"nothing to remove in '{config_name}'")

        if config_name not in track_data[device_name]:
            utils.error(f"config name '{config_name}' not found")

        config_paths = track_data[device_name][config_name]

        if len(config_paths) == 0:
            utils.error(f"nothing to remove in '{config_name}'")

        # ask for user input: select config file to delete
        to_be_removed_paths = utils.select_options(
            "Select paths to remove (↑↓ for naivgation and → ← for select and unselect respectively)",
            config_paths,
        )

        if len(to_be_removed_paths) == 0:
            utils.warn("no options selected!")
            utils.error("aborting!")

        # unlink src from link_to
        for p in to_be_removed_paths:
            link_to = utils.generate_link_path(p, config_name, synko_storage_dir)
            utils.unlink(p, link_to)
            utils.success(f"removed {p}")

        # update track data
        track_data[device_name][config_name] = [
            i for i in config_paths if i not in to_be_removed_paths
        ]

        # update track data
        if len(track_data[device_name][config_name]) == 0:
            del track_data[device_name][config_name]

        if len(track_data[device_name]) == 0:
            del track_data[device_name]

        # check if to_be_removed_paths are associated with any other
        # device id, if not then delete the backup file
        to_be_deleted_backups = to_be_removed_paths

        for device in track_data:
            if device != device_name:
                for p in to_be_removed_paths:
                    if p in track_data[device][config_name]:
                        to_be_deleted_backups.remove(p)

        for p in to_be_deleted_backups:
            utils.delete_backup(p, config_name, synko_storage_dir)

    elif all_config:
        # if -a/--all-config provided
        # confirm first, then remove all
        utils.info(
            "This will remove all the config files added to synko in this device (won't affect other devices)"
        )
        sure = utils.select_option("Are you sure you want to proceed?", ["yes", "no"])
        if sure == "no":
            utils.error("aborting!")

        if device_name in track_data:
            for config in track_data[device_name]:
                for path in track_data[device_name][config]:
                    # unlink src from link_to
                    link_to = utils.generate_link_path(path, config, synko_storage_dir)
                    utils.unlink(path, link_to)
                    utils.success(f"removed {path}")
                    to_be_removed_paths.append(path)

            tmp_current_device_track_data = track_data[device_name]
            del track_data[device_name]

        # check if to_be_removed_paths are associated with any other
        # device id, if not then delete the backup file
        to_be_deleted_backups = to_be_removed_paths
        for device in track_data:
            for config in track_data[device]:
                for p in to_be_removed_paths:
                    if p in track_data[device][config]:
                        to_be_deleted_backups.remove(p)

        for config in tmp_current_device_track_data:
            for p in to_be_deleted_backups:
                if p in tmp_current_device_track_data[config]:
                    utils.delete_backup(p, config, synko_storage_dir)

    App.update_track_data(track_data)
    utils.success("done!")


# info command
@main.command()
@click.option(
    "-p",
    "--storage-path",
    type=str,
    default="",
    help="takes path to the storage directory (Dropbox folder as of now)",
)
def info(storage_path):
    """displays current settings for synko"""
    if len(storage_path) == 0:
        App.display_synko_info()
        return

    storage_path = os.path.realpath(storage_path)

    if not os.path.isdir(storage_path):
        utils.error(f"make sure that '{storage_path}' exists and is a directory")

    if utils.is_path_in_app_data_dir(storage_path, APP_DATA_DIR):
        utils.error(f"'{storage_path}' is used by synko, so it cannot be used")

    App.update_storage_path(storage_path)
    App.update_app_data_file()
    utils.success(f"storage path updated to '{storage_path}'")


@main.command()
def reset():
    """
    reset synko to the original state, all the settings will revert to default
    will remove all the file added to synko
    """
    track_data = App.get_track_data()
    synko_storage_dir = App.get_storage_dir()
    device_name = App.device_name()
    to_be_removed_paths = []

    # confirm first
    utils.info(
        """This will remove all the config files added to synko in this device (won't affect other devices).
This action will also revert the synko settings to default and unregister current device.
Synko will be fresh as new!
        """
    )
    sure = utils.select_option("Are you sure you want to proceed?", ["yes", "no"])
    if sure == "no":
        utils.error("aborting!")
    else:

        to_be_removed_paths = []
        tmp_current_device_track_data = {}

        # unlink all files added to synko, and remove files
        # which are not associated with any other devices
        if device_name in track_data:
            for config in track_data[device_name]:
                for path in track_data[device_name][config]:
                    # unlink src from link_to
                    link_to = utils.generate_link_path(path, config, synko_storage_dir)
                    utils.unlink(path, link_to)
                    utils.success(f"removed {path}")
                    to_be_removed_paths.append(path)

            tmp_current_device_track_data = track_data[device_name]
            del track_data[device_name]

        # check if to_be_removed_paths are associated with any other
        # device id, if not then delete the backup file
        to_be_deleted_backups = to_be_removed_paths
        for device in track_data:
            for config in track_data[device]:
                for p in to_be_removed_paths:
                    if p in track_data[device][config]:
                        to_be_deleted_backups.remove(p)

        for config in tmp_current_device_track_data:
            for p in to_be_deleted_backups:
                if p in tmp_current_device_track_data[config]:
                    utils.delete_backup(p, config, synko_storage_dir)

        # delete the app data directory
        App.reset_app_data()
        # update track file with changes
        App.update_track_data(track_data)

        utils.success("done!")


if __name__ == "__main__":
    # TODO: get OS using platform.system()
    # and exit if OS is not Linux/Darwin
    main()
