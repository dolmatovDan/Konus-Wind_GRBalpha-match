import os
import sys

sys.path.append("..")
from utility import read_text_file, convert_raw_to_interim, clear_name


def parse_event_name(folder_name):
    str_data = read_text_file(f"{folder_name}/info.txt").split("\n")
    pos = str_data[0].find(":")
    return str_data[0][pos + 2 :]


def parse_event_time(folder_name):
    str_data = read_text_file(f"{folder_name}/info.txt").split("\n")
    pos = str_data[1].find(":")
    return str_data[1][pos + 2 :]


def main():
    data_folder = "../../data/raw/GRBalpha/"
    save_folder = "../../data/interim/GRBalpha/"

    for index, folder in enumerate(os.listdir(data_folder)):

        current_folder = os.path.join(data_folder, folder)

        str_data = read_text_file(os.path.join(current_folder, "data.txt")).split("\n")
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
        full_name = event_name
        event_time = parse_event_time(current_folder)

        if event_name.split()[0] == "GRB":
            event_name = "GRB"
        else:
            event_name = "Solar flare"
        save_file_name = os.path.join(save_folder, event_name, f"{folder.strip()}.thc")

        with open(save_file_name, "w") as save_file:
            print(f"(Start time): {data_splitted[0][0]}", file=save_file)
            print(f"(Event name): {full_name}", file=save_file)
            print(f"(Event time): {event_time}", file=save_file)
            print(
                "{:>15}      {:>15}      {:>15}".format(
                    "sec_from_start", "~80-400keV", "~400-950keV"
                ),
                file=save_file,
            )
            print(
                "{:>15}      {:>15}      {:>15}".format("---", "---", "---"),
                file=save_file,
            )
            print(
                "{:>15}      {:>15}      {:>15}".format("(s)", "(cnt/s)", "(cnt/s)"),
                file=save_file,
            )
            for data in data_splitted:
                if len(data) == 9:  # Example: ../../data/raw/GRB 221206B_099/data.txt
                    count_rate_70_370 = float(data[4]) + float(data[5])
                    count_rate_400_950 = float(data[6]) + float(data[7])
                    print(
                        f"{float(data[2]):>15f}      {count_rate_70_370:>15f}      {count_rate_400_950:>15f}",
                        file=save_file,
                    )
                elif (
                    len(data) == 18
                ):  # Example: ../../data/raw/GRB 221009A_113/data.txt
                    count_rate_70_370 = sum(list(map(float, data[4:]))[:5])
                    count_rate_400_950 = sum(list(map(float, data[4:]))[5:-1])
                    print(
                        f"{float(data[2]):>15f}      {count_rate_70_370:>15f}      {count_rate_400_950:>15f}",
                        file=save_file,
                    )
                elif len(data) == 8:  # Example: ../../data/raw/GRB 211018A_123/data.txt
                    count_rate_70_370 = sum(list(map(float, data[4:]))[:2])
                    count_rate_400_950 = list(map(float, data[4:]))[2]
                    print(
                        f"{float(data[2]):>15f}      {count_rate_70_370:>15f}      {count_rate_400_950:>15f}",
                        file=save_file,
                    )
                elif (
                    len(data) == 12
                ):  # Example: ../../data/raw/GRB 220826B_119/data.txt
                    count_rate_70_370 = sum(list(map(float, data[4:]))[:3])
                    count_rate_400_950 = sum(list(map(float, data[4:]))[3:-1])
                    print(
                        f"{float(data[2]):>15f}      {count_rate_70_370:>15f}      {count_rate_400_950:>15f}",
                        file=save_file,
                    )
                elif len(data) == 10:
                    count_rate_70_370 = sum(list(map(float, data[4:]))[:5])
                    count_rate_400_950 = sum(list(map(float, data[4:]))[3:-1])
                    print(
                        f"{float(data[2]):>15f}      {count_rate_70_370:>15f}      {count_rate_400_950:>15f}",
                        file=save_file,
                    )


if __name__ == "__main__":
    main()
