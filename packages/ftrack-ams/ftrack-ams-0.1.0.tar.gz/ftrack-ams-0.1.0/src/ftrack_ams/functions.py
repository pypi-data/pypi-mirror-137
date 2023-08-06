import os

import ftrack_api

server = "https://ams.ftrackapp.com/api?"


def create_project_name(num, client, name):
    return f"{num}_{client.upper()}_{name.upper()}"


def clearConsole():
    return os.system("cls" if os.name in ("nt", "dos") else "clear")


def get_ftrack_session():
    return ftrack_api.Session(
        server_url=server,
        api_key=os.getenv("FTRACK_API_KEY"),
        api_user=os.getenv("FTRACK_API_USER"),
    )
