import argparse
import subprocess
import sys
import matplotlib.pyplot as plt
import numpy as np


def plot(par_file, TOA_file='TOA1', p=False, step=False, num=False):
  ephemeris = "PSR {psr}\nRAJ {ra}\nDECJ {dec}\nP0 {{p}}\nP1 {p1}\nPEPOCH {pepoch}\nDM {dm}\nEPHEM {ephem}"
  params = {}

  with open(par_file) as f:
    for line in f:
      x = line.split()
      if len(x) > 0:
        if 'PSR' in x[0]:      params['psr'] = x[1]
        elif x[0] == 'RAJ':    params['ra'] = x[1]
        elif x[0] == 'DECJ':   params['dec'] = x[1]
        elif x[0] == 'P0':     params['p'] = float(x[1])
        elif x[0] == 'P1':     params['p1'] = float(x[1])
        elif x[0] == 'PEPOCH': params['pepoch'] = float(x[1])
        elif x[0] == 'DM':     params['dm'] = float(x[1])
        elif x[0] == 'EPHEM':  params['ephem'] = x[1]
  ephemeris = ephemeris.format(psr=params['psr'], ra=params['ra'], dec=params['dec'], p1=params['p1'], pepoch=params['pepoch'], dm=params['dm'], ephem=params['ephem'])
  
  if not p: p = params['p']
  if not step: step = 0.3 * p / (60 * 60 * 24 * 30 * 3)  #30% of phase over 3 months

  par_file = '/dev/shm/{}_ephemeris'.format(params['psr'])
  start = 'Starting general2 plugin'
  end = 'Finished general2 plugin'

  fig = plt.figure()

  if not num: num = 400.
  flag = 1
  dp_list = np.arange(num) * step - step * num/2
  for count, dp in enumerate(dp_list):
    with open(par_file, 'w') as par:
      par.write(ephemeris.format(p=p+dp))

    output = subprocess.Popen(['tempo2', '-output', 'general2', '-f', par_file, TOA_file, '-s', '{bat} {post}\n'], stdout=subprocess.PIPE)
    out, err = output.communicate()
    idx_start = out.index(start) + len(start) + 1
    idx_end = out.index(end)
    out = out[idx_start:idx_end]
    res = np.array(out.split(), dtype=float).reshape(-1,2).T

    ax = plt.subplot(8, 5, flag)
    ax.plot(res[0], res[1], 'ko')
    ax.text(0, 1, "P = {:.9f}".format((p+dp)), transform=ax.transAxes)
    ax.tick_params(axis='both', labelbottom='off', labelleft='off', top='off', bottom='off', left='off', right='off')  

    if flag == 8*5:
      print "Plotting figure number {} / {}".format(int(count/40.)+1, int(len(dp_list)/40.))
      flag = 1
      plt.get_current_fig_manager().window.showMaximized()
      plt.show()
    else: 
      sys.stdout.write("{:.1f}% completed\r".format(flag * 100. / (8*5)))
      sys.stdout.flush()
      flag += 1

  return 


def parser():
  # Command-line options
  parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                  description="Plot tempo2 fits of P0 varying between P0-step*num/2 and P0+step*num/2.")
  parser.add_argument('-par_file', help="Parameter file to use.", default='par1')
  parser.add_argument('-TOA_file', help="TOA file to use.", default='TOA1')
  parser.add_argument('-p', help="Central period P0. Default is P0 in par_file", default=False, type=float)
  parser.add_argument('-step', help="Step between different period trials. Default is a variation of 0.3 of phase over 3 months.", default=False, type=float)
  parser.add_argument('-num', help="Number of trials to try. 40 trials per plot will be visualised.", default=400, type=float)
  parser.add_argument('-p_range', help="Minimum and maximum values of period to search. Ignore step (or num) and period.", default=False, type=float, nargs=2)
  return parser.parse_args()



if __name__ == "__main__":
  args = parser()
  if args.p_range:
    if args.step:
      args.num = (args.p_range[1] - args.p_range[0]) / args.step
      print "A num value of {} will be used, producing {} plots".format(args.num, int(args.num/40.)+1)
    else: 
      args.step = (args.p_range[1] - args.p_range[0]) / args.num
      print "A step of {:.2e} s will be used".format(args.step)

    args.p = (args.p_range[1] + args.p_range[0]) / 2.
    print "A period of {} s will be used".format(args.p)

  plot(args.par_file, TOA_file=args.TOA_file, p=args.p, step=args.step, num=args.num)


