#!/bin/bash -x

for subint in `cat /home/michilli/LOTAAS_Timing/pulsars/J0139+33/fil/obs_list.dat`; do
  if [ ! -e /home/michilli/LOTAAS_Timing/pulsars/J0139+33/fil/$subint ]; then
    sh /home/michilli/LOTAAS_Timing/software/apollo_process.sh $subint
  fi
  rm /home/michilli/LOTAAS_Timing/pulsars/J0139+33/fil/5*/*.paz* 
  rm /home/michilli/LOTAAS_Timing/pulsars/J0139+33/fil/5*/*.ar
done

