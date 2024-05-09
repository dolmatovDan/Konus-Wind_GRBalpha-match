import datetime
import os
import time
from dateutil import parser
from datetime import timedelta
import numpy as np


def create_folder(name):
    if os.path.isdir(name):
        print(f"Folder {name} already exists")
        return False
    path = name
    os.mkdir(path)
    return True


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
    """
    LS V +44 17 / RX J0440.9+4431 -> LS V +44 17
    """
    if name.find("/") == -1:
        return name
    pos = name.find("/")
    return name[:pos]


def read_text_file(name):
    with open(name, "r") as f:
        return f.read()


def convert_raw_to_interim(data):
    """
    split("  "): 2023-10-01 03:22:23.850207   2023-10-01 03:22:24.850207 ->
        -> ["2023-10-01 03:22:23.850207", "2023-10-01 03:22:24.850207"]
                       ^                             ^
                leave spaces
    """
    return [s.strip() for s in data.split("  ") if len(s)]


def convert_seconds_to_time(n_seconds):
    time_format = time.strftime("%H:%M:%S", time.gmtime(n_seconds))
    return time_format


def parse_date(date):
    """
    20240204_66244 -> 2024-02-04 18:24:04
    """
    year = int(date[:4])
    month = int(date[4:6])
    day = int(date[6:8])
    seconds = int(date[9:])

    time = convert_seconds_to_time(seconds)
    return f"{year}-{month:02d}-{day:02d} {time}"


def get_date_after_delta(date, delta):
    start_date = parser.parse(date)
    new_date = start_date + timedelta(seconds=float(delta))
    return new_date.strftime("%Y-%m-%d %H:%M:%S.%f")


def transfrom_to_dateobj(date):
    if date.find(".") == -1:
        # Means that num of seconds is integer
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    # Means that num of seconds is float
    return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")


def seconds_between_dates(str_dt1, str_dt2):
    dt1 = transfrom_to_dateobj(str_dt1)
    dt2 = transfrom_to_dateobj(str_dt2)
    delta = (dt1 - dt2).total_seconds()
    return delta


def erase_nan(arr):
    return arr[~np.isnan(arr)]


def get_min_max(arr):
    arr_sorted = sorted(erase_nan(arr))
    d = int(len(arr) * 0.025)
    return arr_sorted[d], arr_sorted[-d]
