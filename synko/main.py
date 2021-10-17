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
@click.argument("name", nargs=1)
@click.argument("paths", nargs=-1)
def add(name, paths):
    """
    add configuration path for syncing
    """
    paths = list(set(paths))
    track_data = App.get_track_data()
    app_data = App.get_appdata()
    device_id = App.device_id()

    if len(paths) == 0:
        utils.error("no paths specified!")

    # perform various checks and validate
    App.validate_config_paths(paths)

    # check if paths already exists in track file?
    App.check_duplicate_paths(paths)

    # update track data and file
    track_data.setdefault(name, {})
    track_data[name].setdefault(device_id, [])

    # form links and update track data
    for p in paths:
        selected = 0
        link_to = utils.generate_link_path(p, app_data["SYNKO_STORAGE_DIR"])

        # if link_to exists then ask for confirmation
        if os.path.exists(link_to):
            print(SYNKO_ADD_CONFLICT.format(path=p))
            selected = utils.select_option("Select option", [0, 1, "skip", "abort"])

        if selected == "abort":
            utils.warn("aborted!")
            break

        if selected == "skip":
            utils.warn(f"skipped {p}")
            continue

        utils.link(p, link_to, selected)
        track_data[name][device_id].append(p)
        utils.success(f"added {p}")

    # write track data to track file
    App.update_track_data(track_data)

    utils.success("done!")


# index command
# TODO: allow users to enter config name and display
# configs only of that specific configuration
@main.command()
@click.argument("name", nargs=1, required=False)
def index(name):
    """list all the donfig files added to synko"""
    track_data = App.get_track_data()

    if len(track_data) == 0:
        utils.error("nothing to list")

    App.display_track_data()


# remove command
@main.command()
@click.argument("name", nargs=1)
# TODO: @click.option(
#     "--all", "-a", is_flag=True, help="remove all config files under config name"
# )
def remove(name):
    """remove specific config file from synko"""
    track_data = App.get_track_data()
    synko_storage_dir = App.get_storage_dir()
    device_id = App.device_id()

    if name not in track_data:
        utils.error(f"config name '{name}' not found")

    if device_id not in track_data[name]:
        utils.error(f"nothing to remove in '{name}'")

    config_paths = track_data[name][device_id] or []

    if len(config_paths) == 0:
        utils.error(f"nothing to remove in '{name}'")

    # TODO: show select option only when "all" arg is not used
    # when "all" option is used, set to_be_removed_paths=config_paths

    # ask for user input: select config file to delete
    to_be_removed_paths = utils.select_options(
        "Select paths to remove (↑↓ for naivgation and → ← for select and unselect respectively)",
        config_paths,
    )

    if len(to_be_removed_paths) == 0:
        utils.warn("no options selected!")
        utils.error("aborting")

    # unlink src from link_to
    for p in to_be_removed_paths:
        link_to = utils.generate_link_path(p, synko_storage_dir)
        utils.unlink(p, link_to)
        utils.success(f"removed {p}")

    # update track data
    track_data[name][device_id] = [
        i for i in config_paths if i not in to_be_removed_paths
    ]

    # check if to_be_removed_paths are associated with any other
    # device id, if not then delete the backup file
    found = False
    for device in track_data[name]:
        if device != device_id:
            for p in to_be_removed_paths:
                if p in track_data[name][device]:
                    found = True
                    break

        # exit outer loop
        if found:
            break

    if not found:
        utils.delete_backup(p, synko_storage_dir)

    # remove/delete file
    if len(track_data[name][device_id]) == 0:
        track_data[name].pop(device_id, None)

    if len(track_data[name]) == 0:
        track_data.pop(name, None)

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
    utils.success(f"storage path updated to '{storage_path}'")


if __name__ == "__main__":
    # TODO: get OS using platform.system()
    # and exit if OS is not Linux/Darwin
    main()
