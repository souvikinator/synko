#!/usr/bin/python3
import click
from Synko import Synko
from utils import error
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
    """about this command"""

    paths = set(paths)

    if len(paths) == 0:
        error("No paths specified!")

    # TODO: check if all the paths are real path and also follow if symlink
    # TODO: allow only files and directories
    # TODO: check if backup/synk file already exists
    # TODO: do not allow paths starting with /


# index command
@main.command()
@click.option("--configs", "-c", type=bool, default=True)
@click.option("--devices", "-d", type=bool, default=False)
def index(configs, devices):
    """about this command"""
    pass


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
