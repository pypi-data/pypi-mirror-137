import os

import click
from pick import pick

from ftrack_ams.functions import clearConsole, get_ftrack_session
from ftrack_ams.functions import create_project_name
from . import __version__


proj_dir = "X:/"
projects = []


def get_latest_proj():
    projectcodes = []
    for x in os.scandir(proj_dir):
        if x.is_dir():
            try:
                code = int(x.name[0:4])
            except Exception:
                continue
            else:
                # print(code)
                if code != 9999:
                    projectcodes.append(code)

    return max(projectcodes) + 1


@click.command()
@click.version_option(version=__version__)
@click.option("--new", "-n", is_flag=True)
def main(new=None):
    session = get_ftrack_session()

    print(f"👋 {session.api_user}, y'all got logged the F in")

    if new:
        create_new_project(session)


# print(f'making a new project for {projects[p]["name"]}')


def create_new_project(session):

    continue_project_creation = get_yes_no(
        "Are you sure you want to create a new project? 🕵️‍♂️"
    )

    if not continue_project_creation:
        print("ok bye 👋")
        quit()

    projects = session.query("Project")
    users = session.query("User")

    clearConsole()

    print(f"Ok {session.api_user}, which team are we making a project for?")

    option, index = pick(
        sorted([p["name"] for p in projects if "invoice" not in p["name"]]),
        "Select the team:",
    )

    clearConsole()
    num = get_latest_proj()
    team = [t for t in projects if option.lower() in t["name"].lower()][0]
    print(f"💁‍♂️ Making a new project for {team['name']}")

    dest_folder = None

    for child in projects[index]["children"]:
        if child["name"] == "Projects":
            dest_folder = child

    if dest_folder is None:
        print(f"could not find a 'Projects' folder for team {team['name']}")
        quit()

    while True:
        client = input("Enter client letter code (3 characters):")
        if len(client) == 3:
            print(f"making project number {num} for client {client}")
            break
        else:
            print("didnt get ya fully")
            continue

    while True:
        projname = input("Enter project letter code (3 characters):")
        if len(projname) == 3:
            break
        else:
            print("Didnt get ya fully? Type three characters.")
            continue

    project_name = create_project_name(num, client, projname)

    while True:
        try:
            num_int = int(input("Enter amount of INT shots:\n"))
        except ValueError:
            print("Sorry, I didn't understand that? Did you type a number?")
            # better try again... Return to the start of the loop
            continue
        else:
            print(f"Number of INT:{num_int}")
            break

    while True:
        try:
            num_ext = int(input("Enter amount of EXT shots:\n"))
        except ValueError:
            print("Sorry, I didn't understand that? Did you type a number?")
            # better try again... Return to the start of the loop
            continue
        else:
            print(f"Number of EXT:{num_ext}")
            break

    if num_int == 0:
        desc = f"{num_ext} EXT"
    elif num_ext == 0:
        desc = f"{num_int} INT"
    else:
        desc = f"{num_int} INT/{num_ext} EXT"

    proj = session.create(
        "Amsproj",
        {
            "name": project_name,
            "parent": dest_folder,
            "description": desc,
        },
    )

    task_templates = team["project_schema"]["task_templates"]

    for template in task_templates:
        # print(template["name"])
        if template["name"] == "Annelies_Template":
            annelies_template = template
        if template["name"] == "Image_Template":
            image_template = template
        if template["name"] == "PM_Template":
            production_template = template

    pm_choice, index = pick(["Hanne", "Nele", "Pieter"], "Select project manager")
    project_manager = [i for i in users if pm_choice.lower() in i["username"].lower()][
        0
    ]

    for task_type in [t["task_type"] for t in production_template["items"]]:
        task = session.create("Task",
                              {"name": task_type["name"],
                               "type": task_type,
                               "parent": proj})
        session.create(
            "Appointment",
            {"context": task,
             "resource": project_manager,
             "type": "assignment"},
        )

    for u in users:
        if u["username"] == "Annelies.Cardoen":
            annelies = u

    for task_type in [t["task_type"] for t in annelies_template["items"]]:
        task = session.create(
            "Task", {"name": task_type["name"], "type": task_type, "parent": proj}
        )
        session.create(
            "Appointment", {"context": task, "resource": annelies, "type": "assignment"}
        )

    if num_int > 0:
        int_folder = session.create("Folder",
                                    {"name": f"{num}_INT", "parent": proj})
        ia, index = pick(
            ["Tom", "Ellen", "Dainius", "Siarhei", "Lowie", "Austris"],
            "Select interior artist:",
        )
        int_artist = [i for i in users if ia.lower() in i["username"].lower()][0]

        for i in range(num_int):
            int_shot_name = f"{num}_INT_{chr(ord('@')+i+1)}"
            int_shot = session.create(
                "Image", {"name": int_shot_name, "parent": int_folder}
            )
            for task_type in [t["task_type"] for t in image_template["items"]]:
                task = session.create(
                    "Task",
                    {"name": task_type["name"], "type": task_type, "parent": int_shot},
                )
                session.create(
                    "Appointment",
                    {"context": task, "resource": int_artist, "type": "assignment"},
                )

    if num_ext > 0:
        ext_folder = session.create("Folder", {"name": f"{num}_EXT", "parent": proj})
        exterior_artist, index = pick(
            ["Tom", "Robin", "Dainius", "Siarhei", "Lowie"], "Select exterior artist:"
        )
        ext_artist = [
            i for i in users if exterior_artist.lower() in i["username"].lower()
        ][0]
        for i in range(num_ext):
            ext_shot_name = f"{num}_EXT_{chr(ord('@')+i+1)}"
            ext_shot = session.create(
                "Image", {"name": ext_shot_name, "parent": ext_folder}
            )
            for task_type in [t["task_type"] for t in image_template["items"]]:
                task = session.create(
                    "Task",
                    {"name": task_type["name"], "type": task_type, "parent": ext_shot},
                )
                session.create(
                    "Appointment",
                    {"context": task, "resource": ext_artist, "type": "assignment"},
                )

    drone = get_yes_no("Does the project require photography?")

    session.commit()

    print(f"Succesfully created {project_name} for {team['name']}")
    print(f"--- creating objects for {project_name} on ftrack")
    print(f"--- creating outlook folder for {project_name}")
    print(f"--- creating directory for {project_name} on X:/")
    print(f"-- {num_int} INT tasks for {ia}") if num_int > 0 else None
    print(f"-- {num_ext} EXT tasks for {exterior_artist}") if num_ext > 0 else None
    print("--- creating photography tasks") if drone else None
    print(f"--- creating {project_name}.mxp for 3dsmax project")
    print(f"--- updating {project_name} on teamleader")


def create_project_on_fileserver(project):
    project_dir = f"X:/{project}/"
    print(project_dir)
    print(f"{project_dir} already exists") if os.path.isdir(
        project_dir
    ) else os.makedirs(project_dir)

    go = os.path.join(project_dir, "GegevensOpdrachtgever")
    print(f"{go} already exists") if os.path.isdir(go) else os.makedirs(go)
    mv = os.path.join(project_dir, "Mails&Vergaderingen")
    print(f"{mv} already exists") if os.path.isdir(mv) else os.makedirs(mv)

    maps = os.path.join(project_dir, "Maps")
    print(f"{maps} already exists") if os.path.isdir(maps) else os.makedirs(maps)

    scenes = os.path.join(project_dir, "scenes")
    print(f"{scenes} already exists") if os.path.isdir(scenes) else os.makedirs(scenes)


def get_yes_no(question):
    answer = pick(["Yes", "No"], question)
    return True if answer[1] == 0 else False


if __name__ == "__main__":
    main()
