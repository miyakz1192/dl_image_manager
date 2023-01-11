#!/bin/bash

ls projects | while read proj
do
	echo clearing ${proj}
	rm -rf projects/${proj}/build/*
done
