import os
import sys

sys.path.append("..")
from utility import read_text_file, parse_date, get_date_after_delta


def main():
    data_folder = "../../data/raw/KW"
    save_folder = "../../data/interim/KW"
    for file in os.listdir(data_folder):
        data_path = os.path.join(data_folder, file)
        str_data = read_text_file(data_path).split("\n")
        lst_data = [list(map(float, s.split())) for s in str_data if len(s)]
        if not len(lst_data):
            continue
        with open(os.path.join(save_folder, file), "w") as save_file:
            start_time = parse_date(file[2:-4])
            start_time = get_date_after_delta(start_time, lst_data[0][0])

            print(f"(Start time): {start_time}", file=save_file)
            print(
                "{:>15}      {:>15}      {:>15}      {:>15}      {:>15}".format(
                    "sec_from_start",
                    "~80-400keV S1",
                    "~400-950keV S1",
                    "~80-400keV S2",
                    "~400-950keV S2",
                ),
                file=save_file,
            )
            print(
                "{:>15}      {:>15}      {:>15}      {:>15}      {:>15}".format(
                    "---", "---", "---", "---", "---"
                ),
                file=save_file,
            )
            print(
                "{:>15}      {:>15}      {:>15}".format(
                    "(s)", "(cnt/s)", "(cnt/s)", "(cnt/s)", "(cnt/s)"
                ),
                file=save_file,
            )

            time_delta = lst_data[0][0]
            for data in lst_data:
                cur_second = data[0] - time_delta
                dt = data[1] - data[0]
                count_rate_80_400_S1 = data[3] / dt
                count_rate_400_950_S1 = data[4] / dt

                count_rate_80_400_S2 = data[6] / dt
                count_rate_400_950_S2 = data[7] / dt

                print(
                    f"{cur_second:>15f}      {count_rate_80_400_S1:>15f}      {count_rate_400_950_S1:>15f}      {count_rate_80_400_S2:>15f}      {count_rate_400_950_S2:>15f}",
                    file=save_file,
                )


if __name__ == "__main__":
    main()
