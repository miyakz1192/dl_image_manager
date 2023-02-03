#!/usr/bin/bash 

if [ $# -ne 1 ]; then
	echo "USAGE: resnet34 or ssd"
	exit 1
fi

type=$1

./build.sh ${type}

if [ ${type} == "resnet34" ]; then
	echo "resnet34"
	./send_data_set_and_run_resnet34.sh
elif [ ${type} == "ssd" ]; then
	echo "ssd"
	./send_data_set_and_run_ssd.sh
fi

