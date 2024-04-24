import sys
from matplotlib import pyplot as plt

sys.path.append("..")
from utility import read_text_file


def parse_GRBalpha_data(path):
    str_data = read_text_file(path).split("\n")
    date = str_data[0][str_data[0].find(":") + 2]
    lst_data = [list(map(float, s.split())) for s in str_data[4:] if len(s)]
    return date, lst_data


def main():
    pass


if __name__ == "__main__":
    main()
