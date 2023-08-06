import click

from ftrack_ams.functions import get_ftrack_session
from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    session = get_ftrack_session()
    click.secho(f"Heyyy {session.api_user}", fg="green")
