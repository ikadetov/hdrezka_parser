import os


def check_folder_series(title, season):
    if not os.path.exists("hdrezka/"):
        os.mkdir("hdrezka/")
    if not os.path.exists(f"hdrezka/{title}"):
        os.mkdir(f"hdrezka/{title}")
        os.mkdir(f"hdrezka/{title}/{season}")
        return True
    elif not os.path.exists(f"hdrezka/{title}/{season}"):
        os.mkdir(f"hdrezka/{title}/{season}")
        return True
    else:
        return True


def check_folder_films(title):
    if not os.path.exists("hdrezka/"):
        os.mkdir("hdrezka/")
    if not os.path.exists(f"hdrezka/{title}"):
        os.mkdir(f"hdrezka/{title}")
        return True
    else:
        return True
