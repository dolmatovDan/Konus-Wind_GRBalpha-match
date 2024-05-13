from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import math


def get_delta(y_max, y_min):
    lst_num = [1, 2, 5]
    lst_minor = [0.5, 1, 1]
    n = len(lst_num)
    delta_y = lst_num[0]
    delta_minor = lst_minor[0]

    n_ticks = math.floor((y_max - y_min) / delta_y)

    i = 0
    while n_ticks > 4:
        delta_y = lst_num[i % n] * 10 ** math.floor(i / n)
        delta_minor = lst_minor[i % n] * 10 ** math.floor(i / n)
        n_ticks = math.floor((y_max - y_min) / delta_y)
        i = i + 1
    return delta_y, delta_minor


def main():
    x = np.array([1, 2, 3, 4])
    y = np.array([2, 3, 6, 10])
    plt.plot(x, y)
    max_y = np.max(y)
    min_y = np.min(y)
    fig, axes = plt.subplots(1, 1, figsize=(10, 15))
    delta, delta_minor = get_delta(max_y, min_y)
    print(delta, delta_minor)
    axes.yaxis.set_major_locator(MultipleLocator(delta))
    axes.yaxis.set_minor_locator(MultipleLocator(delta_minor))

    y_max = math.ceil(max_y / delta) * delta + delta / 2.0
    y_min = math.floor(min_y / delta) * delta
    axes.set_ylim(y_min, y_max)
    plt.show()


if __name__ == "__main__":
    main()
