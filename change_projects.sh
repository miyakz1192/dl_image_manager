#!/bin/bash

if [ $# -ne 1 ]; then
	echo "USAGE: dl_type (ex: ssd , resnet34)"
	exit 1
fi

dl_type=$1

if [ ${dl_type} == "resnet34" ]; then
	echo "[resnet34] replacing projects/* data for specified algo"
	rm -rf projects/*
	cp -r projects_store/common/* projects/
	cp -r projects_store/resnet34/* projects/
elif [ ${dl_type} == "ssd" ]; then
	echo "[ssd] replacing projects/* data for specified algo"
	rm -rf projects/*
	cp -r projects_store/common/* projects/
	cp -r projects_store/ssd/* projects/
fi

echo "finished for replacing projects data"

