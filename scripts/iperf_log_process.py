#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-11-14 15:18:59
# @Link    : https://github.com/GreenLv/Solis-WiFi-Trace
# @Author  : Green Lv

import os
import inspect


LOG_DIR = "./iperf_logs/"
TRACE_DIR = "./iperf_bw_trace/"


def DEBUG(*objects):
    print('[{}]'.format(inspect.stack()[1][3]), end=' ')
    print(*objects)


def mkdir(dir):
    is_exists = os.path.exists(dir)
    if not is_exists:
        os.makedirs(dir)


def read_log_and_gen_trace(log_dir=LOG_DIR, trace_dir=TRACE_DIR):

    if not os.path.exists(log_dir):
        DEBUG("Error! Logs not exist!")
        return

    mkdir(trace_dir)

    for log_file in os.listdir(log_dir):
        if not log_file.endswith(".log") or not log_file.startswith("iperf"):
            continue

        log_path = os.path.join(log_dir, log_file)
        trace_name = "wifi_trace{}.txt".format(log_file[5:-4])
        trace_path = os.path.join(trace_dir, trace_name)

        with open(log_path, "r") as in_file, \
                open(trace_path, "w+", newline="\n") as out_file:

            line_cnt = 0
            bw_sum = 0
            for line in in_file:
                if not line.strip().startswith("[") or not line.strip().endswith("Bytes"):
                    continue

                parse = line.strip().split()
                ts = float((parse[2].split("-"))[0])
                bw = float(parse[6])
                bw_sum += bw
                # print(parse)
                # print(ts, bw)

                out_line = "{}\t{}\n".format(ts, bw)
                out_file.write(out_line)
                line_cnt += 1
                # print(out_line)
                # break
        DEBUG("Generate trace: {}, data points: {}, avg bw: {:.3f}".
              format(trace_path, line_cnt, bw_sum / line_cnt if line_cnt != 0 else 0))


if __name__ == '__main__':

    read_log_and_gen_trace()
