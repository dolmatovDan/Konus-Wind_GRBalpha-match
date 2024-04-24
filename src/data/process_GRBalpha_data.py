import os
import sys

sys.path.append("..")
from utility import read_text_file, convert_raw_to_interim, clear_name


def parse_event_name(folder_name):
    str_data = read_text_file(f"{folder_name}/info.txt").split("\n")
    pos = str_data[0].find(":")
    return str_data[0][pos + 2 :]


def main():
    data_folder = "../../data/raw/"
    save_folder = "../../data/interim/"

    for folder in os.listdir(data_folder):
        current_folder = data_folder + folder
        str_data = read_text_file(f"{current_folder}/data.txt").split("\\n")
        headers = [
            "start_time",
            "end_time",
            "sec_from_start",
            "exposure",
            "rate_0",
            "rate_1",
            "rate_2",
            "rate_3",
            "rate_sum",
        ]
        data_splitted = [convert_raw_to_interim(s) for s in str_data[3:] if len(s)]
        event_name = parse_event_name(current_folder)
        if event_name.split()[0] == "GRB":
            event_name = "GRB"
        else:
            event_name = "Solar flare"
        save_file_name = f"{save_folder}{event_name}/{folder}.thc"
        with open(save_file_name, "w") as save_file:
            print(f"(Start time): {data_splitted[0][0]}", file=save_file)
            print(
                "{:>14}      {:>10}      {:>10}".format(
                    "sec_from_start", "80-400keV", "400-950keV"
                ),
                file=save_file,
            )
            print(
                "{:>14}      {:>10}      {:>10}".format("---", "---", "---"),
                file=save_file,
            )
            print(
                "{:>14}      {:>10}      {:>10}".format("(s)", "(cnt/s)", "(cnt/s)"),
                file=save_file,
            )
            for data in data_splitted:
                if len(data) != 9:
                    continue
                print(
                    f"{float(data[2]):>14f}      {float(data[4]) + float(data[5]):>10f}      {float(data[6]) + float(data[7]):>10f}",
                    file=save_file,
                )


if __name__ == "__main__":
    main()
