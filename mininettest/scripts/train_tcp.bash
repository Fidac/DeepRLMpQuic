#!/usr/bin/env bash

CONGESTION_TEST="python /App/mininettest/congestiontest.py --train";
WEIGHT_FILE="/App/offline_agent/blank_weights.h5"

usage(){
    echo "train.bash <delta_rtt> <steps> [allowed_congestion]"
}

main(){
    echo "$1","$2","$3"
    if [ -z $3 ]
    then
    ALLOWED=0
    else
    ALLOWED=$3
    fi

    MAX_STEPS=$2
    rm /App/mininettest/weight*.h5
    rm /App/output/*.csv
    STEPS=0
    rm -rf /App/output/train_$1/
    rm /App/output/aggregated_$1.csv
    mkdir -p /App/output/train_$1/

    while [ $STEPS -lt $MAX_STEPS ]
    do
        EPSILON=$(bc <<< "scale=2; 1. - (0.1 + $STEPS/$MAX_STEPS * 0.8)")
        echo "$STEPS/$MAX_STEPS using $WEIGHT_FILE with epsilon=$EPSILON"

        while :
        do
           cd /App/mininettest/ && $CONGESTION_TEST --weight_file $WEIGHT_FILE --epsilon 0$EPSILON --rtt $1 --valid_congestion  $ALLOWED
           NSTEP=$(cat /App/output/episode_*.csv|wc -l)
	   echo $NSTEP
           if [ $NSTEP -gt 6000 ]
           then
             break
           fi
        done
        LINE=$(tail -n 1 /App/output/episode_*.csv)

        python /App/mininettest/summary.py "$LINE"
        NSTEP=$(cat /App/output/episode_*.csv|wc -l)

        STEPS=$((STEPS + NSTEP))
        cat /App/output/episode_*.csv >> /App/output/aggregated_$1.csv
        rm /App/output/episode_*.csv

        mv $WEIGHT_FILE /App/output/train_$1/
        python3 /App/offline_agent/trainModel.py /App/output/aggregated_$1.csv
        WEIGHT_FILE=$(ls $PWD/weight*)
    done
    mv $WEIGHT_FILE /App/output/train_$1/
}

if [ $# -ge 2 ]
then
    main $1 $2 $3
else
    usage
fi