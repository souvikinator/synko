#!/usr/bin/python3
import sys
import click
from click.termui import prompt
from Synko import Synko
import utils
from constants import APP_NAME, APP_VERISON


App = Synko()


@click.group()
@click.version_option(version=APP_VERISON, prog_name=APP_NAME)
def main():
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
    device_id = App.device_id()

    if len(paths) == 0:
        utils.error("No paths specified!")

    # perform various checks and validate
    utils.validate_config_paths(paths)

    # check if paths already exists in track file?
    App.check_duplicate_paths(paths)

    # form links
    utils.link_all(paths)

    # update track data and file
    track_data.setdefault(name, dict())
    track_data[name].setdefault(device_id, list())

    track_data[name][device_id].extend(paths)
    App.update_track_data(track_data)

    click.echo(f"added successfully to synko!")


# index command
@main.command()
@click.option("--configs", "-c", type=bool, default=True)
# @click.option("--devices", "-d", type=bool, default=False)
def index(configs):
    """list all the donfig files added to synko"""
    track_data = App.get_track_data()

    if len(track_data) == 0:
        click.echo("Nothing to list")
        sys.exit(0)

    if configs:
        App.display_track_data()


# remove command
# TODO: allow removing files
@main.command()
@click.argument("name", nargs=1)
@click.option("-a/-na", default=False)
def remove(name, a):
    """remove specific config file from synko"""

    track_data = App.get_track_data()
    device_id = App.device_id()

    if name not in track_data:
        utils.error(f"config name '{name}' not found")

    if device_id not in track_data[name]:
        utils.error(f"nothing to remove in config name '{name}'")

    config_paths = track_data[name][device_id] or []

    if len(config_paths) == 0:
        utils.error(f"nothing to remove in config name '{name}'")

    # ask for user input: select config file to delete
    to_be_removed_paths = utils.select_options(config_paths)

    if len(to_be_removed_paths) == 0:
        utils.error(f"No options selected!\nAborting remove")

    # unlink src from link_to
    utils.unlink_all(to_be_removed_paths)

    # update track data
    track_data[name][device_id] = [
        i for i in config_paths if i not in to_be_removed_paths
    ]

    # check if to_be_removed_paths are associated with any other device id, if not then delete them
    for device in track_data[name]:
        for p in to_be_removed_paths:
            if p not in track_data[name][device]:
                utils.delete_backup(p)

    # remove/delete file
    if len(track_data[name][device_id]) == 0:
        track_data[name].pop(device_id, None)

    if len(track_data[name]) == 0:
        track_data.pop(name, None)

    App.update_track_data(track_data)

    print(f"removed successfully!")


if __name__ == "__main__":
    click.echo(
        f"""        
 __  .._ ;_/ _ 
_) \_|[ )| \(_)
   ._|          v{APP_VERISON}

        """
    )
    main()
