#!/usr/bin/bash 

if [ $# -ne 1 ]; then
	echo "USAGE: resnet34 or ssd"
	exit 1
fi

type=$1

if [ ${type} == "resnet34" ]; then
	echo "resnet34"
	cp config/dl_image_manager_config_resnet34.py lib/dl_image_manager_config.py
elif [ ${type} == "ssd" ]; then
	echo "ssd"
	cp config/dl_image_manager_config_ssd.py lib/dl_image_manager_config.py
fi

./change_projects.sh ${type}

./bin/clear_project.sh
./bin/build_all.py
./bin/build_data_set.py
