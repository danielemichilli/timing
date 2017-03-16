#!/bin/bash -x

if [ "$1" == "-h" ]; then
echo """
Second processing script.
Prepare the archives in the current folders for timing.
Archives are cleaned, and scrunched.
"""
exit
fi


pam --setnbin 512 -Tp -e Tp *.clean
pam -E par1 -m *.Tp

echo " " > dm.list
for ar in *.Tp; do
  pdmp=`pdmp -g None ${ar}`
  dm=${pdmp#*Best DM = }
  dm=${dm% Correction =*}
  pam -m -d $dm $ar
  echo -dm $dm >> dm.list
done

pam -e FTp -F *.Tp
rm *.Tp

paste -d' ' TOA1 dm.list > TOA2
