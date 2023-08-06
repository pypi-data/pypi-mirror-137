import click

from ftrack_ams.functions import get_ftrack_session
from ftrack_ams.main import create_new_project
from . import __version__


@click.command()
@click.version_option(version=__version__)
@click.option("--new", "-n", is_flag=True)
def main(new=False):
    session = get_ftrack_session()
    click.secho(f"👋  Heyyy {session.api_user}", fg="green")
    if new:
        create_new_project(session)
