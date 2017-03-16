from glob import glob
import os
import psr_utils
import sys
from cStringIO import StringIO

wrk_dir = "/home/michilli/LOTAAS_Timing/pulsars"


def table_line(folder='.'):
  #Read .par file
  par_file = glob(os.path.join(folder,'*.par'))[0]
  with open(par_file) as f:
    par = f.readlines()
  idx = [r.split()[0] for r in par]
  par = [r.split() for r in par]

  #Read parameters
  PSRJ = par[idx.index('PSRJ')][1]
  RAJ = par[idx.index('RAJ')][1][:11]
  DECJ = par[idx.index('DECJ')][1][:11]
  F0 = float(par[idx.index('F0')][1])
  F0_err = float(par[idx.index('F0')][-1])
  F1 = float(par[idx.index('F1')][1])
  F1_err = float(par[idx.index('F1')][-1])
  EPOCH = int(float(par[idx.index('PEPOCH')][1]))
  DM = float(par[idx.index('DM')][1])
  START = int(float(par[idx.index('START')][1]))
  FINISH = int(float(par[idx.index('FINISH')][1]))
  NTOA = int(par[idx.index('NTOA')][1])
  RES = float(par[idx.index('TRES')][1])

  #Derive quantities
  class Capturing(list):
    def __enter__(self):
      self._stdout = sys.stdout
      sys.stdout = self._stringio = StringIO()
      return self
    def __exit__(self, *args):
      self.extend(self._stringio.getvalue().splitlines())
      del self._stringio    # free up some memory
      sys.stdout = self._stdout
  with Capturing() as derq:
    psr_utils.psr_info(F0, F1, input='f')
  #derq = [r for r in derq if len(r) > 0]
  #idx = [r.split()[0] for r in derq]
  #derq = [r.split() for r in derq]

  #Read parameters
  E1 = float(derq[5].split()[2])
  B = float(derq[6].split()[4])
  T = float(derq[7].split()[3])

  return "{PSR} &\t{RA} &\t{DEC} &\t{F:.3f} $\\pm$ {F_err:.1e} &\t{F1:.3f} $\\pm$ {F1_err:.4f} &\t{EPOCH} &\t{NTOA} &\t{START} - {FINISH} &\t{RES:.0f} &\t{DM:.1f} &\t{E1:.1e} &\t{B:.1e} &\t{T:.1e} \\\\".format(PSR=PSRJ, RA=RAJ, DEC=DECJ, F=F0, F_err=F0_err, F1=F1*1e15, F1_err=F1_err*1e15, EPOCH=EPOCH, NTOA=NTOA, START=START, FINISH=FINISH, RES=RES, DM=DM, E1=E1, B=B, T=T)


if __name__ == '__main__':
  psr_list = glob(os.path.join(wrk_dir,"J???????*"))
  tex_table = []
  for psr in psr_list:
    if os.path.isfile("{}/{}.par".format(psr, os.path.basename(psr))):
      tex_table.append(table_line(folder=psr))
  with open(os.path.join(wrk_dir, 'psr_params.tex'), 'w') as tex:
    tex.write("%PSRJ & RA & DEC & F0 (Hz) & F1 ($10^{-15}$s$^{-2}$) & Epoch & Ntoa & Timespan & Residuals ($\mu$s) & DM (pc/cc) & E1 (ergs/s) & B (gauss) & Age (yr)\\\\\n")
    for line in tex_table:
      tex.write(line+"\n")



