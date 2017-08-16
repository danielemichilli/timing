#!/bin/bash -x

if [ "$1" == "-h" ]; then
echo """
Process Apollo data.
User should provide ObsID (e.g. 57000_001100)
"""
exit
fi

cd "/home/michilli/LOTAAS_Timing/pulsars/J0139+33/fil"

if [ -e $1 ]; then
  echo "$1 already exists, it will be reprocessed"
  cd $1
else
  mkdir $1
  cd $1
  scp "ftp.astron.nl:/ftp/pub/anonymous/outgoing/bassa/fil/$1*.fil" .
fi

if ! ls *.ar 1> /dev/null 2>&1; then
  for fil in $1*.fil; do 
    dspsr -K -s -A -k 8 -E /home/michilli/LOTAAS_Timing/pulsars/J0139+33/0139+33.par -O ${fil%.fil} $fil
  done
fi

if ! ls *.clean 1> /dev/null 2>&1; then
  paz -r -e paz *.ar
  for ar in *.paz; do 
    clean.py -F surgical -o ${ar}.clean $ar
  done
fi

if ! ls ../$1*.si* 1> /dev/null 2>&1; then
  for ar in *.clean; do
    psrspa -a above:threshold=10 $ar
    awk '{print $2}' psrspa_pulses.dat > subint_list
    for subint in `cat subint_list`; do 
      pam -e clean.si --setnchn 2 -x "$subint $subint" $ar
      mv ${ar}.si ${ar}.si${subint}.F2
      pam -e F -F ${ar}.si${subint}.F2
      mv ${ar}.si${subint}.F ${ar}.si${subint}
    done
  done
  mv *.si* ..
  cd ..
  mv *.F2 F2
fi


