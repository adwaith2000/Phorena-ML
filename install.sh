#! /bin/bash

ls -l */*/* | grep "yaml" | awk '{print $9}' | while read configFile
do
	microk8s kubectl create -f $configFile;
done;
