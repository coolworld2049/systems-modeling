import datetime
import json
import math
import pathlib
import random as random
import time

from icecream import ic


def __calc_integral(exp_nmb, fc, a, b):
    x_max = b
    x_min = a
    y_max = fc(b)
    y_min = 0
    m = 0
    for i in range(exp_nmb):
        p = random.random()
        x_p = (x_max - x_min) * p + x_min
        p = random.random()
        y_p = (y_max - y_min) * p + y_min
        if fc(x_p) > y_p:
            m += 1
    return m * (b - a) * fc(b) / exp_nmb


def calc_integral(seria_num, exp_nmb_power, fc, a, b):
    st = time.perf_counter()
    experiment = {"exp_integral": __calc_integral(10 ** exp_nmb_power, fc, a, b)}
    end = time.perf_counter()
    log = f"calc_integral: exp_nmb_power: seria_num: {seria_num}: 10^{exp_nmb_power}: elapsed time: {end - st:0.5f}"
    ic(log)
    return experiment


def calc_inaccuracy(_series: list[dict[dict]]):
    for _seria in _series:
        for key in _seria.keys():
            _seria[key]['inaccuracy'] = math.fabs(((_seria[key]['exp_integral'] - 6) / 6))
    return _series


def calc_inaccuracy_for_average_series(_series: list[dict]):
    for _seria in _series:
        intg_list = list([_seria[k]['exp_integral'] for k in _seria.keys()])
        avg_series = sum(intg_list) / len(intg_list)
        _seria['average_inaccuracy'] = math.fabs((avg_series - 6) / 6)
    return _series


def calc_series(_series_num, _exp_nmb_power_start, _exp_nmb_power_end, fc, a, b):
    _series = list()
    for seria in range(_series_num):
        _series.append(
            {
                f"10 ** {power}": calc_integral(seria, power, fc, a, b)
                for power in range(_exp_nmb_power_start, _exp_nmb_power_end + 1)
            })
    return _series


def main(exp_file: str):
    series_num = 3
    exp_nmb_power_start = 4
    exp_nmb_power_end = 7

    def myfunc(x):
        f = x ** 3 + 1
        return f

    _a = 0
    _b = 2

    with open(f"{exp_file}/input.json", "w") as wf:
        _input = {
            'series_num': 1,
            'exp_nmb_power_start': 4,
            'exp_nmb_power_end': 7,
            'func': ' x ** 3 + 1',
            'a': 0,
            'b': 2,
        }
        json.dump(_input, wf, indent=4)

    series = calc_series(series_num, exp_nmb_power_start, exp_nmb_power_end, myfunc, _a, _b)
    calc_inaccuracy(series)
    res = calc_inaccuracy_for_average_series(series)

    with open(f"{exp_file}/output.json", "w") as wf_1:
        json.dump(res, wf_1, indent=4)


def init():
    cwd = pathlib.Path().cwd()
    exp_path = f"{cwd}/monte_carlo_integral"
    pathlib.Path(exp_path).mkdir(0o777, exist_ok=True)
    exp_file = f'{exp_path}/exp_{datetime.datetime.timestamp((datetime.datetime.now()))}'
    pathlib.Path(exp_file).mkdir(0o777)
    return exp_file


if __name__ == '__main__':
    start = time.perf_counter()
    path = init()
    main(path)
    end = time.perf_counter()
    with open(f"{path}/details.json", "w") as wf_2:
        elapsed_time = {'elapsed time': f"{end - start:0.5f}"}
        json.dump(elapsed_time, wf_2, indent=4)
