import os
import sys

sys.path.append("..")
from utility import read_text_file, transfrom_to_dateobj


def parse_date(folder):
    str_data = read_text_file(os.path.join(folder, "info.txt")).split("\n")
    name = str_data[0][str_data[0].find(":") + 2 :].strip()
    date = str_data[1][str_data[1].find(":") + 2 :].strip()
    return date, name


def main():
    GRBalpha_folder = "../../data/raw/GRBalpha/"
    lst_date_name = []
    for folder in os.listdir(GRBalpha_folder):
        lst_date_name.append(parse_date(os.path.join(GRBalpha_folder, folder)))
    lst_date_name = sorted(lst_date_name, key=lambda x: transfrom_to_dateobj(x[0]))

    GRB_order = "../../data/interim/GRBalpha/GRB_order.txt"
    Solar_flare_order = "../../data/interim/GRBalpha/Solar flare_order.txt"

    for x in lst_date_name:
        if x[1].split()[0] == "GRB":
            with open(GRB_order, "a") as save_file:
                print(x[0], file=save_file)
        else:
            with open(Solar_flare_order, "a") as save_file:
                print(x[0], file=save_file)


if __name__ == "__main__":
    main()
