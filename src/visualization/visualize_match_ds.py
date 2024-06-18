import math
import sys
import os
from matplotlib import pyplot as plt
import datetime
from matplotlib.ticker import MultipleLocator
import numpy as np
import math
from PyAstronomy.pyasl import getAngDist

sys.path.append("..")

from utility import (
    read_text_file,
    plot_settings,
    parse_date,
    seconds_between_dates,
    clear_name,
    parse_file_name,
    get_delta,
    erase_nan,
)


def parse_GRBalpha_data(path):
    str_data = read_text_file(path).split("\n")
    date = str_data[0][str_data[0].find(":") + 2 :]

    try:
        T90 = float(str_data[3][str_data[3].find(":") + 2 :])
    except:
        T90 = float(str_data[3][str_data[3].find(":") + 2 :][1:])  # >80 -> 80

    lst_data = [list(map(float, s.split())) for s in str_data[7:] if len(s)]

    x = np.array([s[0] for s in lst_data])  # Time
    y1 = np.array([s[1] for s in lst_data])  # Count rate in ~80-400keV
    y2 = np.array([s[2] for s in lst_data])  # Count rate in ~400-950keV
    Y = np.array([y1, y2])

    return date, x, Y, T90


def set_yticks(y, ax):
    max_y = max(y)
    min_y = min(y)

    delta, delta_minor = get_delta(max_y, min_y)
    ax.yaxis.set_major_locator(MultipleLocator(delta))
    ax.yaxis.set_minor_locator(MultipleLocator(delta_minor))

    y_max = math.ceil(max_y / delta) * delta + delta / 2.0
    y_min = math.floor(min_y / delta) * delta
    ax.set_ylim(y_min, y_max)


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


def format_KW_data(x, Y1, Y2, t_start, t_end):
    x_f = []
    Y1_f = [[], []]
    Y2_f = [[], []]
    for index, time in enumerate(x):
        if t_start <= time <= t_end:
            x_f.append(time)
            Y1_f[0].append(Y1[0][index])
            Y1_f[1].append(Y1[1][index])

            Y2_f[0].append(Y2[0][index])
            Y2_f[1].append(Y2[1][index])

    return np.array(x_f), np.array(Y1_f), np.array(Y2_f)


def plot_data(
    ax, x1, Y1, x2, y2, legends, titles, colors, backgrounds, name, limits_dict
):
    # Y: [KW S1, KW S2, GRBalpha]

    ax.step(x1, Y1, where="post", label=legends[0], c=colors[0])
    ax.grid(False)

    twin = ax.twinx()
    twin.grid(False)
    twin.step(x2, y2, c=colors[1], where="post", label=legends[1])

    ax.set_ylabel(titles[0])
    twin.set_ylabel(titles[1])

    ax.set_xlim(min(x2), max(x2))
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = twin.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="upper right")

    twin.spines["left"].set_visible(False)

    ax.yaxis.label.set_color(colors[0])
    twin.yaxis.label.set_color(colors[1])

    ax.spines["left"].set_color(colors[0])
    twin.spines["right"].set_color(colors[1])

    ax.tick_params(axis="y", colors=colors[0])
    twin.tick_params(axis="y", colors=colors[1])

    ax.plot(x1, [backgrounds[0]] * len(x1), c=colors[0], linestyle=":")
    twin.plot(x1, [backgrounds[1]] * len(x1), c=colors[1], linestyle=":")

    limits = limits_dict[name]
    ax.set_xlim(limits[4], limits[5])
    twin.set_xlim(limits[4], limits[5])

    set_yticks(Y1, ax)
    set_yticks(y2, twin)

    return twin


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


# def get_KW_background_calc_interval(trig_time):
#     return max(0, trig_time - 550), max(0, trig_time - 50)


def get_KW_background_calc_interval(name, limits_dict):
    data = limits_dict[name]
    return data[0], data[1]


# def get_GRBalpha_background_calc_inerval(GRBalpha_x, Tpeak, T90):
#     if np.sum(GRBalpha_x < Tpeak - T90) > np.sum(GRBalpha_x > Tpeak + T90):
#         return 0, np.max(Tpeak - T90)
#     return Tpeak + T90, np.max(GRBalpha_x)


def get_GRBalpha_background_calc_inerval(name, limits_dict):
    data = limits_dict[name]
    return data[2], data[3]


def get_plot_interval(GRBalpha_x):
    return np.min(GRBalpha_x), np.max(GRBalpha_x)


def get_KW_background(KW_x, KW_Y1, KW_Y2, trig_time, det, name, limits_dict):
    low, high = get_KW_background_calc_interval(name, limits_dict)
    mask = (low < KW_x) & (KW_x < high)
    return np.mean(KW_Y1[det][mask]), np.mean(KW_Y2[det][mask])


def get_GRBalpha_background(GRBalpha_x, GRBalpha_Y, Tpeak, T90, name, limits_dict):
    low, high = get_GRBalpha_background_calc_inerval(name, limits_dict)
    mask = (low < GRBalpha_x) & (GRBalpha_x < high)
    return np.mean(GRBalpha_Y[0][mask]), np.mean(GRBalpha_Y[1][mask])


def choose_det(S1_background, S2_background, KW_Y1):
    # Use G2 energy range
    S1_max = np.max(erase_nan(KW_Y1[0]))
    S2_max = np.max(erase_nan(KW_Y1[1]))

    if S1_max - S1_background < S2_max - S2_background:
        return 1
    return 0


def write_plot_info(event_name, trig_time, GRBalpha_x, Tpeak, T90, save_file):
    with open(save_file, "a") as file:
        KW_interval = get_KW_background_calc_interval(trig_time)
        GRBalpha_interval = get_GRBalpha_background_calc_inerval(GRBalpha_x, Tpeak, T90)
        plot_interval = get_plot_interval(GRBalpha_x)
        print(
            f"{event_name:>20}",
            f"{KW_interval[0]:15.4f}{KW_interval[1]:15.4f}",
            f"{GRBalpha_interval[0]:15.4f}{GRBalpha_interval[1]:15.4f}",
            f"{plot_interval[0]:15.4f}{plot_interval[1]:15.4f}",
            file=file,
            sep="",
        )


def get_table_name(file, name):
    if name.startswith("GRB"):
        return name
    index = file[:3]
    return f"{clear_name(name)} {index}"


def get_limits_dict(event):
    limits_path = f"../../data/interim/tables/{event}_plot_info.txt"
    str_limits_data = read_text_file(limits_path).split("\n")
    lst_limits_data = [
        [s.strip() for s in line.split("   ") if len(s)]
        for line in str_limits_data[1:]
        if len(line)
    ]
    limits_dict = {}
    for data in lst_limits_data:
        limits_dict[data[0]] = list(map(float, data[1:]))
    return limits_dict


def get_position_time_delta(date, file):
    str_delta = read_text_file(file).split("\n")
    lst_delta = [s.split() for s in str_delta if len(s)]
    for data in lst_delta:
        if abs(seconds_between_dates(f"{data[0]} {data[1]}", date)) < 1:
            return float(data[2])
    print("NOT", date)


def draw_match(GRBalpha_path, save_folder, event):
    limits_dict = get_limits_dict(event)
    for index, file in enumerate(os.listdir(GRBalpha_path)):
        path = os.path.join(GRBalpha_path, file)

        line = read_text_file(path).split("\n")[0]
        GRBalpha_date = line[line.find(":") + 2 :].strip()

        line = read_text_file(path).split("\n")[1]
        GRBalpha_name = line[line.find(":") + 2 :].strip()

        line = read_text_file(path).split("\n")[2]
        GRBalpha_time = line[line.find(":") + 2 :].strip()

        trig_time = seconds_between_dates(GRBalpha_time, GRBalpha_date)

        nearst_date_path = get_nearest_date(GRBalpha_date)
        KW_date, KW_x, KW_Y1, KW_Y2 = parse_KW_data(nearst_date_path)
        GRBalpha_date, GRBalpha_x, GRBalpha_Y, T90 = parse_GRBalpha_data(path)

        delta = seconds_between_dates(KW_date, GRBalpha_date)
        KW_x += delta

        if event == "Solar flare":
            position_time_delta = get_position_time_delta(
                GRBalpha_time, "../../data/solar_flare_delta.txt"
            )
        else:
            position_time_delta = get_position_time_delta(
                GRBalpha_time, "../../data/GRB_delta.txt"
            )
        KW_x += position_time_delta

        NoLoc = position_time_delta == 0
        dict_name = get_table_name(file, GRBalpha_name)

        # if dict_name != "Solar flare 041":
        #     continue
        # print(dict_name, position_time_delta)

        t_start = np.min(GRBalpha_x)
        t_end = np.max(GRBalpha_x)

        KW_x, KW_Y1, KW_Y2 = format_KW_data(KW_x, KW_Y1, KW_Y2, t_start, t_end)

        if not len(KW_x):
            continue

        KW_S1_background = get_KW_background(
            KW_x, KW_Y1, KW_Y2, trig_time, 0, dict_name, limits_dict
        )
        KW_S2_background = get_KW_background(
            KW_x, KW_Y1, KW_Y2, trig_time, 1, dict_name, limits_dict
        )

        idx_det = choose_det(KW_S1_background[0], KW_S2_background[0], KW_Y1)
        det = "S1"
        det_col = "r"
        if idx_det == 1:
            det = "S2"
            det_col = "b"

        KW_background = get_KW_background(
            KW_x, KW_Y1, KW_Y2, trig_time, idx_det, dict_name, limits_dict
        )
        GRBalpha_background = get_GRBalpha_background(
            GRBalpha_x, GRBalpha_Y, trig_time, T90, dict_name, limits_dict
        )

        fig, axis = plt.subplots(3, 1, figsize=(10, 15))

        plot_data(
            axis[0],
            KW_x,
            KW_Y1[idx_det],
            GRBalpha_x,
            GRBalpha_Y[0],
            [f"KW {det} (80-400 keV)", "GRBalpha rate_0 + rate_1"],
            ["counts/s", "counts/s"],
            [det_col, "k"],
            [KW_background[0], GRBalpha_background[0]],
            dict_name,
            limits_dict,
        )

        plot_data(
            axis[1],
            KW_x,
            KW_Y2[idx_det],
            GRBalpha_x,
            GRBalpha_Y[1],
            [f"KW {det} (400-950 keV)", "GRBalpha rate_2 + rate_3"],
            ["counts/s", "counts/s"],
            [det_col, "k"],
            [KW_background[1], GRBalpha_background[1]],
            dict_name,
            limits_dict,
        )

        twin = plot_data(
            axis[2],
            KW_x,
            KW_Y1[0],
            KW_x,
            KW_Y1[1],
            ["KW S1", "KW S2"],
            ["counts/s", "counts/s"],
            ["r", "b"],
            [KW_S1_background[0], KW_S2_background[0]],
            dict_name,
            limits_dict,
        )

        axis[2].set_xlabel(f"seconds since {GRBalpha_date} UT")

        x_min, x_max = np.min(GRBalpha_x), np.max(GRBalpha_x)
        axis[2].set_xlim(x_min, x_max)
        y_both = np.concatenate((KW_Y1[0], KW_Y1[1]))

        axis[2].set_xlim(limits_dict[dict_name][4], limits_dict[dict_name][5])

        set_yticks(y_both, axis[2])
        set_yticks(y_both, twin)
        if NoLoc:
            axis[0].set_title(
                f"{GRBalpha_name}, {GRBalpha_time}, LOCALIZATION IS NOT AVAILABLE"
            )
        else:
            axis[0].set_title(f"{GRBalpha_name}, {GRBalpha_time}")
        fig.savefig(
            os.path.join(save_folder, f"{parse_file_name(file)}.png"),
            bbox_inches="tight",
        )
        plt.close()
        print(f"Done {clear_name(dict_name)}")


def main():

    GRB_save_folder = "../../reports/figures/GRB"
    GRB_path = "../../data/interim/GRBalpha/GRB"

    Solar_flare_save_folder = "../../reports/figures/Solar flare"
    Solar_flare_path = "../../data/interim/GRBalpha/Solar flare"

    draw_match(GRB_path, GRB_save_folder, "GRB")
    # draw_match(Solar_flare_path, Solar_flare_save_folder, "Solar flare")


if __name__ == "__main__":
    main()
