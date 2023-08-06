import os
import platform

proj_dir_windows = "X:"
proj_dir_macos = "/Volumes/ams-fileserver/"


def get_latest_proj():
    projectcodes = []

    dir = proj_dir_windows if platform.system() == "Windows" else proj_dir_macos

    for x in os.scandir(dir):
        if x.is_dir():
            try:
                code = int(x.name[0:4])
            except Exception:
                continue
            else:
                if code != 9999:
                    projectcodes.append(code)

    return max(projectcodes) + 1


def create_project_on_fileserver(project):

    if platform.system() == "Windows":
        project_dir = f"{proj_dir_windows}/{project}/"
    else:
        project_dir = f"{proj_dir_macos}/{project}"

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
