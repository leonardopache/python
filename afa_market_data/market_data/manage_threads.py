#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import threading


def prepare_df_to_threading(num_threads, target_df):
    size = len(target_df)
    split_size = int(size / num_threads)
    ini =0
    pivot = 0
    arr = []
    for i in range(num_threads-1):
        pivot += split_size
        arr.append(target_df.iloc[ini:pivot])
        ini = pivot
    arr.append(target_df.iloc[ini:])
    return arr


def thread_run(arr_values, pbar, method_target):
    threads = []
    index = 0
    for df in arr_values:
        index += 1
        t = threading.Thread(name='T' + str(index), target=method_target, args=(df, pbar))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return threads
