import sys
import requests
from bs4 import BeautifulSoup as bs

sys.path.append("..")
from utility import create_folder, clear_name


def main():
    baseurl = "https://monoceros.physics.muni.cz/hea/GRBAlpha/"
    r = requests.get(baseurl)
    soup = bs(r.content)

    # len(soup.find_all("table")) = 1
    # This means, that the first one in necessary data
    table = soup.find("table")

    headers = [
        "Event type/name",
        "Peak time (UTC)",
        "T90 [s]",
        "Peak count rate [cnt/s]",
        "Band [keV]",
        "S/N [sigma]",
        "Raw LC",
        "Bkg-sub LC",
        "LC res. [s]",
        "GCN circ.",
        "References",
        "Comment",
    ]

    for index, row in enumerate(table.find_all("tr")):
        if index == 0:  # Headers
            continue
        columns = row.select("td")

        event_name = columns[0].string
        peak_time = columns[1].string

        event_type = event_name.split()[0]
        data_folder = "../../data/raw/"
        current_folder = f"{data_folder}{clear_name(event_name)}_{index:03d}/"

        create_folder(current_folder)

        with open(f"{current_folder}info.txt", "w") as info_file:
            info_columns = [0, 1, 2, 3, 4, 5]
            for column in info_columns:
                print(f"({headers[column]}): {columns[column].string}", file=info_file)

        for link in row.find_all("a"):
            full_url = baseurl + str(link.get("href"))
            if full_url.endswith(".txt"):
                print(full_url)
                link = requests.get(full_url)
                with open(f"{current_folder}data.txt", "w") as save_file:
                    save_file.write(str(link.content))


if __name__ == "__main__":
    main()
