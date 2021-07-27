from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def compute_ms_tdelta(time1,time2):
    tdelta = time2-time1
    ms_tdelta = tdelta.seconds*1000000 + tdelta.microseconds
    return ms_tdelta


def getTroughputInfo(path):
    info = open(path, "r")
    start = 0
    count = 0
    prev_time = 0
    exp_time = []
    troughput = []
    sum_troughput = 0

    for line in info:
        splitLine = line.split(' ')
        time = splitLine[0]
        time = datetime.strptime(time,"%H:%M:%S.%f")
        size = int(splitLine[1][0:len(splitLine[1])])
        sum_troughput += size
        if(count == 0):
            start = time
        else:
            ms_tdelta = compute_ms_tdelta(prev_time,time)
            ms_tdelta_total = compute_ms_tdelta(start,time)
            exp_time.append(ms_tdelta_total)
            troughput.append(sum_troughput*8/ms_tdelta_total)
            #tcp_tp.append(size*0.0000001/ms_tdelta)
        prev_time = time
        count += 1
    
    return start, exp_time, troughput


def generateFigureIface(tcp_path, mpquic_path, iface):
    tcp_start, tcp_time, tcp_tp = getTroughputInfo(tcp_path)
    mpquic_start, mpquic_time, mpquic_tp = getTroughputInfo(mpquic_path)

    #print("TCP: ", tcp_start, tcp_time, tcp_tp)
    #print("MPQUIC: ", mpquic_start, mpquic_time, mpquic_tp)

    tcp_time = np.array(tcp_time)
    mpquic_time = np.array(mpquic_time)
    tcp_tp = np.array(tcp_tp)
    mpquic_tp = np.array(mpquic_tp)
    
    if(type(mpquic_start) == type(tcp_start)):
        if(mpquic_start > tcp_start):
            tdelta = compute_ms_tdelta(tcp_start,mpquic_start)
            mpquic_time = mpquic_time + tdelta
        else:
            tdelta = compute_ms_tdelta(mpquic_start,tcp_start)
            tcp_time = tcp_time + tdelta

    start_at = 10
    fig = plt.figure()
    plt.title("Throughput of TCP and MPQUIC over time in " + iface)
    plt.xlabel("Time(s)")
    plt.ylabel("Throughput(Mbps)")
    plt.plot(tcp_time[start_at:]/1000000,tcp_tp[start_at:],mpquic_time[start_at:]/1000000,mpquic_tp[start_at:])
    plt.legend(["TCP","MPQUIC"])
    fig.savefig("/App/output/tcp_mpquic_" + iface + ".png")


if __name__ == '__main__':
    generateFigureIface("/App/logs/tcp_packets_timesize_eth1.logs", "/App/logs/mpquic_packets_timesize_eth1.logs", "ETH1")
    generateFigureIface("/App/logs/tcp_packets_timesize_eth0.logs", "/App/logs/mpquic_packets_timesize_eth0.logs", "ETH0")
