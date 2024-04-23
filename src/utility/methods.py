import os


def create_folder(name):
    if os.path.isdir(name):
        print(f"Folder {name} already exists")
    else:
        path = name
        os.mkdir(path)


def get_folder_size(folder_name):
    return len(
        [
            name
            for name in os.listdir(folder_name)
            if os.path.isfile(os.path.join(folder_name, name))
        ]
    )


def get_folders_num(folder_name):
    return len(
        [
            name
            for name in os.listdir(folder_name)
            if os.path.isdir(os.path.join(folder_name, name))
        ]
    )


def clear_name(name):
    if name.find("/") == -1:
        return name
    pos = name.find("/")
    return name[:pos]
