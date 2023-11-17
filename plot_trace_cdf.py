import matplotlib.pyplot as plt
import numpy as np
import sys
import os


CURR_DIR = os.path.dirname(os.path.abspath(__file__))

LOC_LIST = ['cafe', 'campus', 'office', 'restr']
COLORS = ['C0', 'C1', 'C2', 'C3']
LINESTYLES = ['--', '-.', '-', ':']


def cal_avg_bw(trace_path):

    all_bw = []
    with open(trace_path, 'rb') as f:
        for line in f:
            parse = line.split()
            all_bw.append(float(parse[1]))  # Mbps

    return np.mean(all_bw)


def gen_data_summary(data):

    min_bw = np.min(np.array(data))
    max_bw = np.max(np.array(data))
    print('All trace bandwidth range: [{:.3f}]~[{:.3f}] Mbps'.format(min_bw, max_bw))
    print('-' * 50)

    print('Loc\tCount\tAvg BW\tStd BW\tRange')
    for loc_idx, loc_bw in enumerate(data):
        print('{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}~{:.3f}'.
              format(LOC_LIST[loc_idx], len(loc_bw), np.mean(loc_bw),
                     np.std(loc_bw), np.min(loc_bw), np.max(loc_bw)))

    return max_bw


def data_to_cdf(data):

    n = len(data)
    x = np.sort(data)
    y = np.arange(1, n + 1) / n

    return x, y


def plot_cdf(data, max_value):

    plt.rcParams['xtick.labelsize'] = 14
    plt.rcParams['ytick.labelsize'] = 14
    fig, ax = plt.subplots(figsize=(4, 3))

    for loc_idx, loc_bw in enumerate(data):
        x, y = data_to_cdf(loc_bw)
        ax.plot(x, y, label=LOC_LIST[loc_idx], color=COLORS[loc_idx],
                linestyle=LINESTYLES[loc_idx], linewidth=3)

    ax.set_xlabel('Average Bandwidth (Mbps)', fontsize=16)
    ax.set_ylabel('CDF of Traces', fontsize=16)

    min_xlim = 1
    max_xlim = max_value if max_value > 100 else 100
    ax.set_xlim((min_xlim, max_xlim))
    ax.set_ylim((0, 1))
    # ax.set_xscale('log')

    ax.grid()
    ax.legend(labelspacing=0, fontsize=12)

    fig.savefig(os.path.join(CURR_DIR, 'avg_bw_cdf.png'), dpi=300, bbox_inches='tight')
    plt.close()


def read_trace_and_plot():

    trace_dir = os.path.join(CURR_DIR, 'traces')
    trace_file_list = os.listdir(trace_dir)

    all_trace_bw = [[] for _ in range(len(LOC_LIST))]
    for trace_file in trace_file_list:
        if not trace_file.startswith('wifi') or not trace_file.endswith('.txt'):
            continue

        location = (trace_file.split('_'))[1]
        assert(location in LOC_LIST), 'Trace name error: {}'.format(location)
        loc_idx = LOC_LIST.index(location)

        trace_bw = cal_avg_bw(os.path.join(trace_dir, trace_file))
        all_trace_bw[loc_idx].append(trace_bw)
        # print(location, loc_idx, all_trace_bw[loc_idx][-1])

    max_bw = gen_data_summary(all_trace_bw)

    plot_cdf(all_trace_bw, max_bw)


if __name__ == '__main__':

    read_trace_and_plot()
