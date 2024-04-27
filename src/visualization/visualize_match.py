import sys
from matplotlib import pyplot as plt

sys.path.append("..")
from utility import read_text_file, plot_settings


def parse_GRBalpha_data(path):
    str_data = read_text_file(path).split("\n")
    date = str_data[0][str_data[0].find(":") + 2 :]
    lst_data = [list(map(float, s.split())) for s in str_data[4:] if len(s)]
    x = [s[0] for s in lst_data]
    y1 = [s[1] for s in lst_data]
    y2 = [s[2] for s in lst_data]
    return date, x, y1, y2


def main():
    test_path = "../../data/interim/GRB/GRB 210807A_126.thc"
    date, x, y1, y2 = parse_GRBalpha_data(test_path)
    fig, axis = plt.subplots(2, 1, figsize=(16, 10))
    axis[0].plot(x, y1, linewidth=2)
    axis[0].grid(False)
    twin1 = axis[0].twinx()
    twin1.grid(False)
    twin1.plot(x, y2, c="red", linewidth=2)
    axis[0].set_xlabel(f"seconds since {date} UT")
    axis[0].set_ylabel(f"Konus/Wind count rate in ...keV")
    twin1.set_ylabel(f"GRBalpha count rate in 80-400 keV")

    axis[1].plot(x, y1, linewidth=2)
    axis[1].grid(False)
    twin2 = axis[1].twinx()
    twin2.grid(False)
    twin2.plot(x, y2, c="red", linewidth=2)
    axis[1].set_xlabel(f"seconds since {date} UT")
    axis[1].set_ylabel(f"Konus/Wind count rate in ...keV")
    twin2.set_ylabel(f"GRBalpha count rate in 80-400 keV")

    plt.show()


if __name__ == "__main__":
    main()
