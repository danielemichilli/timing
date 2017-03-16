#!/bin/bash -x

if [ "$1" == "-h" ]; then
echo """
First processing script.
Prepare the archives in the current folders for timing.
Archives are cleaned, and scrunched.
"""
exit
fi

#Extract archives
mkdir TEMP
for obs in "L*/rawvoltages/SAP0/BEAM0/*_SAP0_BEAM0.ar"; do mv $obs TEMP; done
for obs in "L*/stokes/SAP0/BEAM0/*_SAP0_BEAM0.ar"; do mv $obs TEMP; done
if [ `ls -l TEMP/*.ar | wc -l` -eq `ls -ld L* | wc -l` ]; then
  rm -r L*
else
  echo "Not all archive extracted from observations!"
fi

#Clean the archives
cd TEMP
paz -r -m *.ar
for ar in *.ar; do clean.py -F surgical -o ${ar}.clean $ar; done

#Scrunch archives
pam --setnbin 512 -e FTp -FTp *.clean

#Create TOAs for DM fit
pam --setnchn 2 --setnbin 512 -p -T -e pTf2 *.clean

cd ..
mv TEMP/*.ar .
mv TEMP/*.clean .
mv TEMP/*.FTp .
mv TEMP/*.pTf2 .
if [ ! -n "$(ls -A TEMP)" ]; then
  rm -r TEMP
fi

#Create par file
vap -E `ls *.ar | tail -1` > par1


