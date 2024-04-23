import os


def create_folder(name):
    if os.path.isdir(name):
        print(f"Folder {name} already exists")
    else:
        path = name
        os.mkdir(path)
