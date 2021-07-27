#!/usr/bin/env bash

./scripts/client_clear_delay.bash
echo "Setting delay "$1" for client-eth0 and loss rate "$2""
tc qdisc add dev client-eth0 parent 5:1 netem delay $1ms
tc qdisc change dev client-eth0 parent 5:1 netem loss $2%
tc qdisc change dev client-eth1 parent 5:1 netem loss $3%