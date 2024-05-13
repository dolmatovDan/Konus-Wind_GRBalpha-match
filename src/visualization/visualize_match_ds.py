import math
import sys
import os
from matplotlib import pyplot as plt
import datetime
from matplotlib.ticker import MultipleLocator
import numpy as np

sys.path.append("..")

from utility import (
    read_text_file,
    plot_settings,
    parse_date,
    transfrom_to_dateobj,
    seconds_between_dates,
    clear_name,
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


def get_delta(y_max, y_min):
    lst_num = [1, 2, 5]
    lst_minor = [0.5, 1, 1]
    n = len(lst_num)
    delta_y = lst_num[0]
    delta_minor = lst_minor[0]

    n_ticks = math.floor((y_max - y_min) / delta_y)

    i = 0
    while n_ticks > 4:
        delta_y = lst_num[i % n] * 10 ** math.floor(i / n)
        delta_minor = lst_minor[i % n] * 10 ** math.floor(i / n)
        n_ticks = math.floor((y_max - y_min) / delta_y)
        i = i + 1
    return delta_y, delta_minor


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


def plot_data(ax, x1, Y1, x2, y2, legends, titles, colors, backgrounds):
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


def get_KW_background(KW_x, KW_Y1, KW_Y2, trig_time, det):
    mask = (trig_time - 550 < KW_x) & (KW_x < trig_time - 50)
    return np.mean(KW_Y1[det][mask]), np.mean(KW_Y2[det][mask])


def get_GRBalpha_background(GRBalpha_x, GRBalpha_Y, Tpeak, T90):
    mask = 0
    if np.sum(GRBalpha_x < Tpeak - T90) > np.sum(GRBalpha_x > Tpeak + T90):
        mask = GRBalpha_x < Tpeak - T90
    else:
        mask = GRBalpha_x > Tpeak + T90
    return np.mean(GRBalpha_Y[0][mask]), np.mean(GRBalpha_Y[1][mask])


def choose_det(S1_background, S2_background, KW_Y1):
    # Use G2
    S1_max = np.max(KW_Y1[0])
    S2_max = np.max(KW_Y1[1])
    if S1_max - S1_background < S2_max - S2_background:
        return 1
    return 0


def draw_match(GRBalpha_path, save_folder):

    for index, file in enumerate(os.listdir(GRBalpha_path)):

        # if file != "GRB 230510B_079.thc":
        #     continue
        # print(file)

        path = os.path.join(GRBalpha_path, file)

        line = read_text_file(path).split("\n")[0]
        GRBalpha_date = line[line.find(":") + 2 :].strip()

        line = read_text_file(path).split("\n")[1]
        GRBalpha_name = line[line.find(":") + 2 :].strip()

        line = read_text_file(path).split("\n")[2]
        GRBalpha_time = line[line.find(":") + 2 :].strip()

        trig_time = seconds_between_dates(GRBalpha_time, GRBalpha_date)
        # print(trig_time)

        nearst_date_path = get_nearest_date(GRBalpha_date)
        KW_date, KW_x, KW_Y1, KW_Y2 = parse_KW_data(nearst_date_path)
        GRBalpha_date, GRBalpha_x, GRBalpha_Y, T90 = parse_GRBalpha_data(path)

        delta = seconds_between_dates(KW_date, GRBalpha_date)
        KW_x += delta

        t_start = np.min(GRBalpha_x)
        t_end = np.max(GRBalpha_x)

        KW_x, KW_Y1, KW_Y2 = format_KW_data(KW_x, KW_Y1, KW_Y2, t_start, t_end)

        if not len(KW_x):
            continue

        KW_S1_background = get_KW_background(KW_x, KW_Y1, KW_Y2, trig_time, 0)
        KW_S2_background = get_KW_background(KW_x, KW_Y1, KW_Y2, trig_time, 1)

        idx_det = choose_det(KW_S1_background[0], KW_S2_background[0], KW_Y1)

        det = "S1"
        det_col = "r"
        if idx_det == 1:
            det = "S2"
            det_col = "b"

        KW_background = get_KW_background(KW_x, KW_Y1, KW_Y2, trig_time, idx_det)
        GRBalpha_background = get_GRBalpha_background(
            GRBalpha_x, GRBalpha_Y, trig_time, T90
        )
        # print(KW_background)
        # print(GRBalpha_background)

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
        )

        axis[2].set_xlabel(f"seconds since {GRBalpha_date} UT")

        x_min, x_max = np.min(GRBalpha_x), np.max(GRBalpha_x)
        axis[2].set_xlim(x_min, x_max)
        y_both = np.concatenate((KW_Y1[0], KW_Y1[1]))

        set_yticks(y_both, axis[2])
        set_yticks(y_both, twin)

        axis[0].set_title(f"{GRBalpha_name}, {GRBalpha_time}")

        fig.savefig(
            os.path.join(save_folder, f"{index:03d}_{clear_name(GRBalpha_name)}.png"),
            bbox_inches="tight",
        )
        plt.close()
        print(f"Done {clear_name(GRBalpha_name)}")


def main():

    GRB_save_folder = "../../reports/figures/GRB"
    GRB_path = "../../data/interim/GRBalpha/GRB"

    Solar_flare_save_folder = "../../reports/figures/Solar flare"
    Solar_flare_path = "../../data/interim/GRBalpha/Solar flare"

    draw_match(GRB_path, GRB_save_folder)
    draw_match(Solar_flare_path, Solar_flare_save_folder)


if __name__ == "__main__":
    main()
