from glob import glob
import os
import numpy as np
import psrchive
from psr_utils import ra_to_rad, dec_to_rad

from output_table import table_line

wrk_dir = "/home/michilli/LOTAAS_Timing/pulsars"


def par_diff(params_new, folder):
  ar = glob(os.path.join(folder, "*.ar"))[-1]
  load_archive = psrchive.Archive_load(ar)
  par = load_archive.get_ephemeris()
  psr = par.get_value('PSR')
  if psr == "": psr = par.get_value('PSRJ')
  print "PSR ", psr
  print "P0 diff: {:.2e} s".format(params_new['P0'] - float(par.get_value('P0')))
  print "DM diff: {:.2e} pc/cc".format(params_new['DM'] - float(par.get_value('DM')))
  
  dist = 60. * np.rad2deg(np.sqrt( (ra_to_rad(par.get_value('RAJ'))-ra_to_rad(params_new['RAJ']))**2 + (dec_to_rad(par.get_value('DECJ'))-dec_to_rad(params_new['DECJ']))**2 ))
  print "Distance: {:.3f}'".format(dist)
  print ""
  return

if __name__ == '__main__':
  print ""
  psr_list = glob(os.path.join(wrk_dir,"J???????*"))
  for psr in psr_list:
    if os.path.isfile(os.path.join(psr, os.path.basename(psr)+".par")):
      params_new = table_line(folder=psr)
      par_diff(params_new, psr)


