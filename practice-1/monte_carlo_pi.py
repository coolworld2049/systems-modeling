import datetime
import json
import math
import pathlib
import random
import time


def calc_pi(exp_nmb, _x0, _y0, _r0):
    """Вычисление значения числа pi"""
    x_min = _x0 - _r0
    x_max = _x0 + _r0
    y_min = _y0 - _r0
    y_max = _y0 + _r0
    m = 0
    for exp in range(exp_nmb):
        p = random.random()
        x = (x_max - x_min) * p + x_min
        p = random.random()
        y = (y_max - y_min) * p + y_min
        if (x - _x0) ** 2 + (y - _y0) ** 2 < _r0 ** 2:
            m += 1
    return 4 * m / exp_nmb


def calc_pi_for_circle(exp_nmb_power, _x0, _y0, _r0):
    return {"exp_pi": calc_pi(10 ** exp_nmb_power, _x0, _y0, _r0)}


def create_series(_series_num, _exp_nmb_power_start, _exp_nmb_power_end, _x0, _y0, _r0):
    _series = []
    for seria in range(_series_num):
        _series.append(
            {
                f"10 ** {power}": calc_pi_for_circle(power, _x0, _y0, _r0)
                for power in range(_exp_nmb_power_start, _exp_nmb_power_end + 1)
            })
    return _series


def calc_inaccuracy(_series: list[dict[dict]]):
    """Расчет погрешности вычислений pi для каждой серии экспериментов"""
    for _seria in _series:
        for key in _seria.keys():
            formula = math.fabs((_seria[key]['exp_pi'] - math.pi) / math.pi)
            _seria[key]['inaccuracy'] = formula
    return _series


def calc_inaccuracy_for_average_values(_series: list[dict]):
    """Расчет погрешности вычислений для усредненного значения для каждой серии экспериментов"""
    for _seria in _series:
        sum_seria = sum(list([_seria[k]['exp_pi'] for k in _seria.keys()]))
        avg_values = sum_seria / len(_series)
        formula = math.fabs((avg_values - math.pi) / math.pi)
        _seria['average_inaccuracy'] = formula
    return _series


def init():
    cwd = pathlib.Path().cwd()
    exp_path = f"{cwd}/monte_carlo_pi"
    pathlib.Path(exp_path).mkdir(0o777, exist_ok=True)
    exp_file = f'{exp_path}/exp_{datetime.datetime.timestamp((datetime.datetime.now()))}'
    pathlib.Path(exp_file).mkdir(0o777)
    return exp_file


def main(exp_file: str):
    series_num = 5
    exp_nmb_power_start = 4
    exp_nmb_power_end = 8
    x0 = 1
    y0 = 2
    r0 = 5
    with open(f"{exp_file}/input.json", "w") as wf_1:
        _input = {
            'series_num': series_num,
            'exp_nmb_power_start': exp_nmb_power_start,
            'exp_nmb_power_end': exp_nmb_power_end,
            'x_0': x0,
            'y_0': y0,
            'r_0': r0
        }
        json.dump(_input, wf_1, indent=4)
    with open(f"{exp_file}/input.json", "w") as wf_2:
        json.dump(_input, wf_2, indent=4)
    series = create_series(series_num, exp_nmb_power_start, exp_nmb_power_end, x0, y0, r0)
    calc_inaccuracy(series)
    series_with_inaccuracy_for_averaged_values = calc_inaccuracy_for_average_values(series)
    with open(f"{exp_file}/output.json", "w") as wf_3:
        json.dump(series_with_inaccuracy_for_averaged_values, wf_3, indent=4)


if __name__ == '__main__':
    start = time.perf_counter()
    path = init()
    main(path)
    end = time.perf_counter()
    main_end = time.perf_counter()
    with open(f"{path}/details.json", "w") as wf_4:
        elapsed_time = {'elapsed time': f"{end - start:0.5f}"}
        json.dump(elapsed_time, wf_4, indent=4)
