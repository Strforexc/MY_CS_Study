#!/bin/bash
comand=$1
count=0
while true
do
	count=$((count+1))
	res=$($1 2>error)
	if [[ $? -eq 1 ]];then
		echo "$count"
		echo "$res" > res
		exit 0
	fi
	echo "test"
done
	

