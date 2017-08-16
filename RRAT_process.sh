#!/bin/bash -x

#Clean the archives
cd fil
for obs in *.fits; do
  dspsr -A -K -s -E par0 -O ${obs%.fits} $obs
done
paz -r -m *.ar
pam -m --setnchn 640 --setnbin 512 *.ar
for ar in *.ar; do clean.py -F surgical -o ${ar}.clean $ar; done
rm *.ar

pam -e clean.F -F *.clean
pam -e clean.F2 --setnchn 2 *.clean
for ar in *.F; do
  psrspa -a above:threshold=10 $ar
  awk '{print $2}' psrspa_pulses.dat > subint_list
  for subint in `cat subint_list`; do
    pam -e F.si${subint} -x "$subint $subint" ${ar}
    pam -e F2.si${subint} -x "$subint $subint" ${ar}2
  done
done


#rm *.clean
#rm *.F

cd ..
mv fil/*.si* .

#Create par file
vap -E `ls *.ar | tail -1` > par1



