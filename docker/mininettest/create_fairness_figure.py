from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

def compute_ms_tdelta(time1,time2):
    tdelta = time2-time1
    ms_tdelta = tdelta.seconds*1000000 + tdelta.microseconds
    return ms_tdelta
tcp = open("/App/logs/tcp_packets_timesize.logs", "r")
mpquic = open("/App/logs/mpquic_packets_timesize.logs", "r")
tcp_start = 0
mpquic_start = 0
count = 0
prev_time = 0
tcp_time = []
tcp_tp = []
sum_tcp_tp = 0
for x in tcp:
    temp = x.split(' ')
    time = temp[0]
    time = datetime.strptime(time,"%H:%M:%S.%f")
    size = int(temp[1][0:len(temp[1])])
    sum_tcp_tp += size
    if(count == 0):
        tcp_start = time
    else:
        ms_tdelta = compute_ms_tdelta(prev_time,time)
        ms_tdelta_total = compute_ms_tdelta(tcp_start,time)
        tcp_time.append(ms_tdelta_total)
        tcp_tp.append(sum_tcp_tp*8/ms_tdelta_total)
        #tcp_tp.append(size*0.0000001/ms_tdelta)
    prev_time = time
    count += 1

count = 0
prev_time = 0
mpquic_time = []
mpquic_tp = []
sum_mpquic_tp = 0
for x in mpquic:
    temp = x.split(' ')
    time = temp[0]
    time = datetime.strptime(time,"%H:%M:%S.%f")
    size = int(temp[1][0:len(temp[1])])
    sum_mpquic_tp += size
    if(count == 0):
        mpquic_start = time
    else:
        ms_tdelta = compute_ms_tdelta(prev_time,time)
        ms_tdelta_total = compute_ms_tdelta(mpquic_start,time)
        mpquic_time.append(ms_tdelta_total)
        mpquic_tp.append(sum_mpquic_tp*8/ms_tdelta_total)
        #mpquic_tp.append(size*0.0000001/ms_tdelta)
    prev_time = time
    count += 1
tcp_time = np.array(tcp_time)
mpquic_time = np.array(mpquic_time)
tcp_tp = np.array(tcp_tp)
mpquic_tp = np.array(mpquic_tp)

if(mpquic_start > tcp_start):
    tdelta = compute_ms_tdelta(tcp_start,mpquic_start)
    mpquic_time = mpquic_time + tdelta
else:
    tdelta = compute_ms_tdelta(mpquic_start,tcp_start)
    tcp_time = tcp_time + tdelta
start_at = 10
fig = plt.figure()
plt.title("Throughput of TCP and MPQUIC over time")
plt.xlabel("Time(s)")
plt.ylabel("Throughput(Mbps)")
plt.plot(tcp_time[start_at:]/1000000,tcp_tp[start_at:],mpquic_time[start_at:]/1000000,mpquic_tp[start_at:])
plt.legend(["TCP","MPQUIC"])
fig.savefig("/App/output/tcp_mpquic.png")
