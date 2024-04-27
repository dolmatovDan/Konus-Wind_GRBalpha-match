import os
import sys

sys.path.append("..")
from utility import read_text_file


def main():
    data_folder = "../../data/raw/KW"
    save_folder = "../../data/interim/KW"
    for file in os.listdir(data_folder):
        data_path = os.path.join(data_folder, file)
        str_data = read_text_file(data_path).split("\n")
        lst_data = [list(map(float, s.split())) for s in str_data if len(s)]


if __name__ == "__main__":
    main()
