#!/bin/bash
cat /App/logs/tcp_packets.logs | sed '/length 0/d' | grep length | cut -d ' ' -f1,21 | sed 's/.$//' > /App/logs/tcp_packets_timesize.logs
cat /App/logs/mpquic_packets.logs | sed '/length 0/d' | grep length | cut -d ' ' -f1,8 > /App/logs/mpquic_packets_timesize.logs
