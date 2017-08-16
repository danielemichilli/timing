#!/bin/bash -x

if [ "$1" == "-h" ]; then
echo """
Read an obsID_list.txt file in the current directory and download the indicated observations from the LTA.
obsID_list.txt must have a first column with pipeID and a second with projectIDs of observations to download.
"""
exit
fi

while read -r obsID projectID; do
  if [ ! -e *${obsID::4}*.ar ]; then
    if [ ! -e bad_obs/*${obsID::4}*.ar ]; then
      lta-retrieve.py -p $projectID --query $obsID
    fi
  fi
done < obsID_list.txt


