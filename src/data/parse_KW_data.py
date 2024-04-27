import os
import subprocess

DATES_PATH = ""
SAVE_FOLDER_PATH = ""


def read_text_file(name):
    with open(name, "r") as f:
        return f.read()


def parse_dates(folder):
    files = os.listdir(folder)
    res_dates = []
    for file in files:
        with open(folder + file, "r") as f_in:
            str_date = f_in.readlines()[0]
            date = str_date[str_date.find(":") + 2 :].strip()
            res_dates.append(date)
    return res_dates


def get_dates():
    folder_GRB = "../../data/interim/GRB/"
    folder_Solar_flare = "../../data/interim/Solar flare/"
    dates = parse_dates(folder_GRB) + parse_dates(folder_Solar_flare)
    save_file_name = "../../data/dates.txt"
    with open(save_file_name, "w") as save_file:
        for date in dates:
            print(date, file=save_file)


def get_second_num(time):
    # Example: "07:51:59.359589"

    lst_time = list(map(float, time.split(":")))
    cnt_sec = int(lst_time[2] + lst_time[1] * 60 + lst_time[0] * 60 * 60)
    return f"{cnt_sec:05d}"


def main():
    str_data = read_text_file(DATES_PATH).split("\n")
    lst_data = [s.split() for s in str_data if len(s)]
    for data in lst_data:
        # Example ["2023-09-11", "07:51:59.359589"]

        date = "".join(data[0].split("-"))
        time = data[1]

        cur_name = f"kw{date}_{get_second_num(time)}.thc"
        save_file_name = os.path.join(SAVE_FOLDER_PATH, cur_name)

        command = f'kw-th -d{date} -t"{time}" -i-300:300 --notrig'
        with open(save_file_name, "w") as save_file:
            subprocess.run(command, shell=False, stdout=save_file)


if __name__ == "__main__":
    main()
