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
  P0 = float(derq[1].split()[2])
  P1 = float(derq[2].split()[2])
  E1 = float(derq[5].split()[2])
  B = float(derq[6].split()[4])
  T = float(derq[7].split()[3])

  

  return {'PSRJ': PSRJ, 'RAJ': RAJ, 'DECJ': DECJ, 'F0': F0, 'F0_err': F0_err, 'F1': F1, 'F1_err': F1_err, 'EPOCH': EPOCH, 'DM': DM, 'START': START, 'FINISH': FINISH, 'NTOA': NTOA, 'RES': RES, 'E1': E1, 'B': B, 'T': T, 'P0': P0, 'P1': P1}




if __name__ == '__main__':
  psr_list = glob(os.path.join(wrk_dir,"J???????*"))
  tex_table = []
  for psr in psr_list:
    print "Analysing psr {}".format(os.path.basename(psr))
    if os.path.isfile("{}/{}.par".format(psr, os.path.basename(psr))):
      params = table_line(folder=psr)
      line = "{PSR} &\t{RA} &\t{DEC} &\t{F:.3f} $\\pm$ {F_err:.1e} &\t{F1:.3f} $\\pm$ {F1_err:.4f} &\t{EPOCH} &\t{NTOA} &\t{START} - {FINISH} &\t{RES:.0f} &\t{DM:.1f} &\t{E1:.1e} &\t{B:.1e} &\t{T:.1e} \\\\".format(PSR=params['PSRJ'], RA=params['RAJ'], DEC=params['DECJ'], F=params['F0'], F_err=params['F0_err'], F1=params['F1']*1e15, F1_err=params['F1_err']*1e15, EPOCH=params['EPOCH'], NTOA=params['NTOA'], START=params['START'], FINISH=params['FINISH'], RES=params['RES'], DM=params['DM'], E1=params['E1'], B=params['B'], T=params['T'])
      tex_table.append(line)
  with open(os.path.join(wrk_dir, 'psr_params.tex'), 'w') as tex:
    tex.write("\\begin{table}\n\\centering\n\\caption{}\n\\label{tab:ephemeris}\n\\begin{tabular}{lllllllllllll}\n\\toprule\n")
    tex.write("PSRJ & RA & DEC & F0 (Hz) & F1 ($10^{-15}$s$^{-2}$) & Epoch & Ntoa & Timespan & Residuals ($\mu$s) & DM (pc/cc) & E1 (ergs/s) & B (gauss) & Age (yr)\\\\\n")
    tex.write("\\midrule\n")
    for line in sorted(tex_table):
      tex.write(line+"\n")
    tex.write("\\bottomrule\n\\end{tabular}\n\\end{table}\n")


