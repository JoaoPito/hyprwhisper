#!/bin/bash

echo "> Hyprwhisper"


request_cmd="curl -s http://localhost:5000"
recording_str="> Recording"

result=$($request_cmd)
echo "$result"

if [ "$result" == "$recording_str" ]; then
	sleep 5
else

	sleep 30
fi
