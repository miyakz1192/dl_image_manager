#!/bin/bash

if [ $# -ne 1 ]; then
	echo "USAGE: project_name"
	exit 1
fi

set -x
project_name=$1
mkdir -p projects/${project_name}/master
mkdir -p projects/${project_name}/build
mkdir -p projects/${project_name}/data_augmentation
mkdir -p projects/${project_name}/jupyer_notebook

echo ${project_name} | grep "^ru_" >& /dev/null
if [ $? -eq 0 ];
	echo "INFO: ru_ mode"
	cp ./sample/ru_daug.py projects/${project_name}/data_augmentation/daug.py
elif
	echo "INFO: lu_ mode(default)"
	cp ./sample/daug.py projects/${project_name}/data_augmentation/daug.py
fi
chmod 766 projects/${project_name}/data_augmentation/daug.py
touch projects/${project_name}/README.md
