#!/usr/bin/python3
import sys
import click
from click.termui import prompt
from Synko import Synko
import utils
from constants import APP_NAME, APP_VERISON


App = Synko()


@click.group()
@click.version_option(version=APP_NAME, prog_name=APP_NAME)
def main():
    # initialize app here
    App.init_app()
    # print(App.get_appdata(), end="\n\n")
    # print(App.get_metadata())
    # perform all checks


# add command
@main.command()
@click.argument("name", nargs=1)
@click.argument("paths", nargs=-1)
def add(name, paths):
    """
    0. validate paths
    1. perform symlink and stuff
    2. update/add paths in track data
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

    # perform symlink

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
    """about this command"""
    track_data = App.get_track_data()

    if len(track_data) == 0:
        click.echo("Nothing to list")
        sys.exit(0)

    if configs:
        App.display_track_data()


# remove command
# TODO: allow removing files
@main.command()
@click.argument("cfgName", nargs=1)
def remove(configs, devices):
    """about this command"""
    pass


if __name__ == "__main__":
    click.echo(
        f"""        
 __  .._ ;_/ _ 
_) \_|[ )| \(_)
   ._|          v{APP_VERISON}

        """
    )
    main()
