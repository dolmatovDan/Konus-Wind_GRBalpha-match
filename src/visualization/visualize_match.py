import sys
import os
from matplotlib import pyplot as plt
import datetime
import numpy as np

sys.path.append("..")
from utility import (
    read_text_file,
    plot_settings,
    parse_date,
    transfrom_to_dateobj,
    seconds_between_dates,
    clear_name,
)


def parse_GRBalpha_data(path):
    str_data = read_text_file(path).split("\n")
    date = str_data[0][str_data[0].find(":") + 2 :]
    lst_data = [list(map(float, s.split())) for s in str_data[6:] if len(s)]

    x = np.array([s[0] for s in lst_data])  # Time
    y1 = np.array([s[1] for s in lst_data])  # Count rate in ~80-400keV
    y2 = np.array([s[2] for s in lst_data])  # Count rate in ~400-950keV
    Y = np.array([y1, y2])

    return date, x, Y


def parse_KW_data(path):
    str_data = read_text_file(path).split("\n")
    date = str_data[0][str_data[0].find(":") + 2 :]
    lst_data = [list(map(float, s.split())) for s in str_data[4:] if len(s)]

    x = np.array([s[0] for s in lst_data])  # Time

    y1 = np.array([s[1] for s in lst_data])  # Count rate in ~80-400keV for S1
    y2 = np.array([s[3] for s in lst_data])  # Count rate in ~80-400keV for S2
    Y1 = np.array([y1, y2])

    y1 = np.array([s[2] for s in lst_data])  # Count rate in ~400-950keV for S1
    y2 = np.array([s[4] for s in lst_data])  # Count rate in ~400-950keV for S2
    Y2 = np.array([y1, y2])

    return date, x, Y1, Y2


def plot_data(ax, x1, Y1, x2, y2, legends, titles, date):
    # Y: [KW S1, KW S2, GRBalpha]

    ax.step(x1, Y1[0], label=legends[0])
    ax.step(x1, Y1[1], label=legends[1])
    ax.grid(False)

    twin = ax.twinx()
    twin.grid(False)
    twin.step(x2, y2, c="green", label=legends[2])

    ax.set_xlabel(f"seconds since {date} UT")
    ax.set_ylabel(titles[0])
    twin.set_ylabel(titles[1])

    ax.set_xlim(min(x2), max(x2))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = twin.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right")


def get_nearest_date(date):
    KW_path = "../../data/interim/KW/"
    min_delta = 2e15
    res_file = ""
    for file in os.listdir(KW_path):
        cur_date = parse_date(file[2:-4])
        delta = abs(seconds_between_dates(cur_date, date))
        if min_delta > delta:
            min_delta = delta
            res_file = os.path.join(KW_path, file)
    return res_file


def draw_match(GRBalpha_path, save_folder):
    for index, file in enumerate(os.listdir(GRBalpha_path)):
        path = os.path.join(GRBalpha_path, file)
        line = read_text_file(path).split("\n")[0]
        GRBalpha_date = line[line.find(":") + 2 :].strip()

        nearst_date_path = get_nearest_date(GRBalpha_date)
        KW_date, KW_x, KW_Y1, KW_Y2 = parse_KW_data(nearst_date_path)
        GRBalpha_date, GRBalpha_x, GRBalpha_Y = parse_GRBalpha_data(path)

        delta = seconds_between_dates(KW_date, GRBalpha_date)
        KW_x += delta

        fig, axis = plt.subplots(2, 1, figsize=(16, 10))
        plot_data(
            axis[0],
            KW_x,
            KW_Y1,
            GRBalpha_x,
            GRBalpha_Y[0],
            ["KW S1", "KW S2", "GRBalpha"],
            ["KW G2", "GRBalpha rate_0 + rate_1"],
            GRBalpha_date,
        )

        plot_data(
            axis[1],
            KW_x,
            KW_Y2,
            GRBalpha_x,
            GRBalpha_Y[1],
            ["KW S1", "KW S2", "GRBalpha"],
            ["KW G3", "GRBalpha rate_2 + rate_3"],
            GRBalpha_date,
        )

        line = read_text_file(path).split("\n")[1]
        GRBalpha_name = line[line.find(":") + 2 :].strip()

        fig.savefig(
            os.path.join(save_folder, f"{index:03d}_{clear_name(GRBalpha_name)}.png")
        )
        plt.close()


def main():
    GRB_save_folder = "../../reports/figures/GRB"
    GRB_path = "../../data/interim/GRBalpha/GRB"

    Solar_flare_save_folder = "../../reports/figures/Solar flare"
    Solar_flare_path = "../../data/interim/GRBalpha/Solar flare"

    draw_match(GRB_path, GRB_save_folder)
    draw_match(Solar_flare_path, Solar_flare_save_folder)


if __name__ == "__main__":
    main()
