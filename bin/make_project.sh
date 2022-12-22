#!/bin/bash

if [ $# -ne 1 ]; then
	echo "USAGE: project_name"
	exit 1
fi

project_name=$1
mkdir -p projects/${project_name}/master
mkdir -p projects/${project_name}/build
touch projects/${project_name}/README.md
