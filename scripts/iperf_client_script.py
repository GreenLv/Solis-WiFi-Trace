#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2023-11-14 14:24:21
# @Link    : https://github.com/GreenLv/Solis-WiFi-Trace
# @Author  : Green Lv


import os
import time


SERVER_IP = "10.0.0.1"
SERVER_PORT = 8888
INTERVAL = 1    # sec
DURATION = 200  # sec

LOG_DIR = "./iperf_logs/"
TEST_CNT = 20


def mkdir(dir):
    is_exists = os.path.exists(dir)
    if not is_exists:
        os.makedirs(dir)


def test_bw(log_dir=LOG_DIR):

    mkdir(log_dir)

    print(">>>>> Test Info <<<<<")
    print("- Server IP: {}".format(SERVER_IP))
    print("- Server port: {}".format(SERVER_PORT))
    print("- Test interval: {} (s)".format(INTERVAL))
    print("- Test duration: {} (s)".format(DURATION))
    print("- Test count: {}".format(TEST_CNT))

    for i in range(TEST_CNT):
        start_time = time.localtime()
        log_name = "iperf_{}.log".\
            format(time.strftime("%y%m%d-%H%M%S", start_time))
        log_path = os.path.join(log_dir, log_name)

        print("\n")
        print("----- Test [{} of {}] starts at: {} -----".
              format(i, TEST_CNT - 1, time.strftime("%Y-%m-%d %H:%M:%S", start_time)))
        print("Wait for {} seconds to end...".format(DURATION))

        os.system("iperf3 -c {} -p {} -f m -i {} -t {} --logfile {}".
                  format(SERVER_IP, SERVER_PORT, INTERVAL, DURATION, log_path))

        print("----- Test [{} of {}] ends. -----".format(i, TEST_CNT - 1))
        print("log_path: {}".format(log_path))

        if i != TEST_CNT - 1:
            time.sleep(5)

    print("===== All tests end. =====")


if __name__ == '__main__':

    test_bw()
