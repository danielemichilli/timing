import subprocess
import sys
import matplotlib.pyplot as plt
import numpy as np

ephemeris = "PSR {psr}\nRAJ {ra}\nDECJ {dec}\nP0 {{p}}\nP1 {p1}\nPEPOCH {pepoch}\nDM {dm}\nEPHEM {ephem}"
params = {}

with open('par1') as f:
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

p = params['p']
step = 0.5 * p / (60 * 60 * 24 * 30 * 4)  #50% of phase over 4 months

par_file = '/dev/shm/{}_ephemeris'.format(params['psr'])
start = 'Starting general2 plugin'
end = 'Finished general2 plugin'

fig = plt.figure()

flag = 1
for dp in np.arange(200.) * step - step * 100:
  with open(par_file, 'w') as par:
    par.write(ephemeris.format(p=p+dp))

  output = subprocess.Popen(['tempo2', '-output', 'general2', '-f', par_file, 'TOA1', '-s', '{bat} {post}\n'], stdout=subprocess.PIPE)
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
    flag = 1
    plt.get_current_fig_manager().window.showMaximized()
    plt.show()
  else: 
    sys.stdout.write("{:.1f}% completed\r".format(flag * 100. / (8*5)))
    sys.stdout.flush()
    flag += 1





