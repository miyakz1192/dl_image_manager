#!/bin/bash

if [ $# -ne 1 ]; then
	echo "USAGE: project_name"
	exit 1
fi

project_name=$1
mkdir -p projects/${project_name}/master
mkdir -p projects/${project_name}/build
mkdir -p projects/${project_name}/data_augmentation
mkdir -p projects/${project_name}/jupyer_notebook

touch projects/${project_name}/data_augmentation/daug.py
chmod 766 projects/${project_name}/data_augmentation/daug.py
touch projects/${project_name}/README.md
