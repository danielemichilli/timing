#!/bin/bash -x

if [ "$1" == "-h" ]; then
echo """
Second processing script.
Prepare the archives in the current folders for timing.
Archives are ready for DM fitting.
"""
exit
fi

pam --setnchn 2 -p -T -e pTf2 *.clean
pat -f tempo2 -s paas.std *.pTf2 > TOA2



