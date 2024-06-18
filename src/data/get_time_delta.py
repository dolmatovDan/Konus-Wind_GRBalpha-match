import os
from PyAstronomy.pyasl import getAngDist
import math
import numpy as np


C = 299792.458  # km/s


def get_tof_solarflare(date, time):

    wind_eph_str = "getephemeris-wind --date=%s --time=%s" % (
        date,
        time,
    )  # эта утилита возвращает координаты и расстояние до Винда
    wind_eph = os.popen(wind_eph_str).read()

    wind_eph = wind_eph.split()
    wind_ra = float(wind_eph[3])
    wind_dec = float(wind_eph[4])
    wind_dist = float(wind_eph[5])

    sun_eph_str = "getephemeris-sun --date=%s --time=%s" % (
        date,
        time,
    )  # эта утилита возвращает координаты Солнца
    sun_eph = os.popen(sun_eph_str).read()

    sun_eph = sun_eph.split()
    sun_ra = float(sun_eph[3])
    sun_dec = float(sun_eph[4])

    ang_distance = getAngDist(wind_ra, wind_dec, sun_ra, sun_dec)
    tof = math.cos(np.deg2rad(ang_distance)) * wind_dist / C

    return tof


def get_tof_grb(date, time, ra, dec):

    wind_eph_str = "getephemeris-wind --date=%s --time=%s" % (date, time)
    wind_eph = os.popen(wind_eph_str).read()

    wind_eph = wind_eph.split()
    wind_ra = float(wind_eph[3])
    wind_dec = float(wind_eph[4])
    wind_dist = float(wind_eph[5])
    ang_distance = getAngDist(wind_ra, wind_dec, ra, dec)
    tof = math.cos(np.deg2rad(ang_distance)) * wind_dist / C

    return -tof


def read_text_file(name):
    with open(name, "r") as f:
        return f.read()


def solar_flare():
    solar_flare_path = "../../data/solar_flare_dates.txt"
    str_dates = read_text_file(solar_flare_path).split("\n")
    lst_dates = [s.split() for s in str_dates if len(s)]

    lst_delta = []
    for date, time in lst_dates:
        lst_delta.append(get_tof_solarflare(date, time))
        print(f"Done {date} {time}")

    with open("solar_flare_delta.txt", "w") as file:
        for index, delta in enumerate(lst_delta):
            print(str_dates[index], delta, file=file)
            print(f"Upload {index}")


def main():
    GRB_path = "../../data/dates_GRB_ra_dec.txt"
    str_dates = read_text_file(GRB_path).split("\n")
    lst_dates = [s.split() for s in str_dates[1:] if len(s)]

    lst_delta = []
    for data in lst_dates:
        date = data[1]
        time = data[2]
        ra = data[3]
        dec = data[4]
        lst_delta.append(get_tof_grb(date, time, ra, dec))
        print(f"Done {date} {time}")

    with open("GRB_delta.txt", "w") as file:
        for index, delta in enumerate(lst_delta):
            print(str_dates[index], delta, file=file)
            print(f"Upload {index}")


if __name__ == "__main__":
    main()
