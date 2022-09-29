import datetime
import pathlib
import time

from icecream import ic


def rand(a, b, m, x=None):
    x = (a * x + b) % m
    rand(a, b, m, x + 1)


if __name__ == '__main__':
    main_start = time.perf_counter()
    ic(pathlib.Path().cwd().name)
    exp_file = f'exp_{datetime.datetime.timestamp((datetime.datetime.now()))}'
    pathlib.Path(exp_file).mkdir(0o777)

    rand(22695477, 1, 2 ** 32)

    main_end = time.perf_counter()
    elapsed_time = f"main.py: elapsed time: {main_end - main_start:0.5f}"
    ic(elapsed_time)
