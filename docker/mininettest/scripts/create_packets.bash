#!/bin/bash
cat /App/logs/tcp_packets_eth1.logs | sed '/length 0/d' | grep length | cut -d ' ' -f1,21 | sed 's/.$//' > /App/logs/tcp_packets_timesize_eth1.logs
cat /App/logs/mpquic_packets_eth1.logs | sed '/length 0/d' | grep length | cut -d ' ' -f1,8 > /App/logs/mpquic_packets_timesize_eth1.logs
cat /App/logs/tcp_packets_eth0.logs | sed '/length 0/d' | grep length | cut -d ' ' -f1,21  > /App/logs/tcp_packets_timesize_eth0.logs
cat /App/logs/mpquic_packets_eth0.logs | sed '/length 0/d' | grep length | cut -d ' ' -f1,8 > /App/logs/mpquic_packets_timesize_eth0.logs
