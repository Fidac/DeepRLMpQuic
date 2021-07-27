#!/usr/bin/env bash

./scripts/clear_delay.bash
echo "Setting delay "$1" for s1-eth1 and loss rate "$2"... "
tc qdisc add dev s1-eth1 parent 5:1 netem delay $1ms
# tc qdisc change dev s1-eth1 parent 5:1 netem loss $2%