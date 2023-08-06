
import os, sys, glob, pickle
import optparse
import numpy as np
from scipy.interpolate import interpolate as interp
import scipy.stats

from astropy.table import Table, Column

import matplotlib
#matplotlib.rc('text', usetex=True)
matplotlib.use('Agg')
#matplotlib.rcParams.update({'font.size': 20})
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm 
plt.rcParams['xtick.labelsize']=30
plt.rcParams['ytick.labelsize']=30
plt.rcParams["font.family"] = "Times New Roman"

import corner

from gwemlightcurves.sampler import *
from gwemlightcurves.KNModels import KNTable
from gwemlightcurves.sampler import run
from gwemlightcurves import __version__
from gwemlightcurves import lightcurve_utils, Global

plotDir = '../plots/gws/Ka2017_combine'
if not os.path.isdir(plotDir):
    os.makedirs(plotDir)

errorbudget = 1.00

plotDir1 = '../plots/gws/Ka2017_FixZPT0/u_g_r_i_z_y_J_H_K/0_14/ejecta/GW170817/1.00/'
pcklFile = os.path.join(plotDir1,"data.pkl")
f = open(pcklFile, 'r')
(data_out, data1, tmag1, lbol1, mag1, t0_best1, zp_best1, n_params1, labels1, best1, truths1) = pickle.load(f)
f.close()

plotDir2 = '../plots/gws/Ka2017x2_FixZPT0/u_g_r_i_z_y_J_H_K/0_14/ejecta/GW170817/1.00/'
pcklFile = os.path.join(plotDir2,"data.pkl")
f = open(pcklFile, 'r')
(data_out, data2, tmag2, lbol2, mag2, t0_best2, zp_best2, n_params2, labels2, best2, truths2) = pickle.load(f)
f.close()

tmag1 = tmag1 + t0_best1
tmag2 = tmag2 + t0_best2

title_fontsize = 30
label_fontsize = 30

filts = ["u","g","r","i","z","y","J","H","K"]
#colors=cm.jet(np.linspace(0,1,len(filts)))
colors=cm.Spectral(np.linspace(0,1,len(filts)))[::-1]
magidxs = [0,1,2,3,4,5,6,7,8]
tini, tmax, dt = 0.0, 21.0, 0.1    
tt = np.arange(tini,tmax,dt)

color2 = 'coral'
color1 = 'cornflowerblue'

plotName = "%s/data_panels.pdf"%(plotDir)
#plt.figure(figsize=(20,18))
plt.figure(figsize=(20,28))

tini, tmax, dt = 0.0, 21.0, 0.1
tt = np.arange(tini,tmax,dt)

cnt = 0
for filt, color, magidx in zip(filts,colors,magidxs):
    cnt = cnt+1
    vals = "%d%d%d"%(len(filts),1,cnt)
    if cnt == 1:
        ax1 = plt.subplot(eval(vals))
    else:
        ax2 = plt.subplot(eval(vals),sharex=ax1,sharey=ax1)

    if not filt in data_out: continue
    samples = data_out[filt]
    t, y, sigma_y = samples[:,0], samples[:,1], samples[:,2]
    idx = np.where(~np.isnan(y))[0]
    t, y, sigma_y = t[idx], y[idx], sigma_y[idx]
    if len(t) == 0: continue

    idx = np.where(np.isfinite(sigma_y))[0]
    plt.errorbar(t[idx],y[idx],sigma_y[idx],fmt='o',c=color, markersize=16)

    idx = np.where(~np.isfinite(sigma_y))[0]
    plt.errorbar(t[idx],y[idx],sigma_y[idx],fmt='v',c=color, markersize=16)

    plt.ylabel('%s'%filt,fontsize=48,rotation=0,labelpad=40)
    plt.xlim([0.0, 14.0])
    plt.ylim([-17.0,-11.0])
    plt.gca().invert_yaxis()
    plt.grid()

    if cnt == 1:
        ax1.set_yticks([-18,-16,-14,-12,-10])
        plt.setp(ax1.get_xticklabels(), visible=False)
        #l = plt.legend(loc="upper right",prop={'size':36},numpoints=1,shadow=True, fancybox=True)
    elif not cnt == len(filts):
        plt.setp(ax2.get_xticklabels(), visible=False)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)

ax1.set_zorder(1)
plt.xlabel('Time [days]',fontsize=48)
plt.savefig(plotName, bbox_inches='tight')
plt.close()

plotName = "%s/models_panels.pdf"%(plotDir)
#plt.figure(figsize=(20,18))
plt.figure(figsize=(20,28))

tini, tmax, dt = 0.0, 21.0, 0.1
tt = np.arange(tini,tmax,dt)

cnt = 0
for filt, color, magidx in zip(filts,colors,magidxs):
    cnt = cnt+1
    vals = "%d%d%d"%(len(filts),1,cnt)
    if cnt == 1:
        ax1 = plt.subplot(eval(vals))
    else:
        ax2 = plt.subplot(eval(vals),sharex=ax1,sharey=ax1)

    if not filt in data_out: continue
    samples = data_out[filt]
    t, y, sigma_y = samples[:,0], samples[:,1], samples[:,2]
    idx = np.where(~np.isnan(y))[0]
    t, y, sigma_y = t[idx], y[idx], sigma_y[idx]
    if len(t) == 0: continue

    idx = np.where(np.isfinite(sigma_y))[0]
    plt.errorbar(t[idx],y[idx],sigma_y[idx],fmt='o',c=color, markersize=16)

    idx = np.where(~np.isfinite(sigma_y))[0]
    plt.errorbar(t[idx],y[idx],sigma_y[idx],fmt='v',c=color, markersize=16)

    if filt == "w":
        magave1 = (mag1[1]+mag1[2]+mag1[3])/3.0
    elif filt == "c":
        magave1 = (mag1[1]+mag1[2])/2.0
    elif filt == "o":
        magave1 = (mag1[2]+mag1[3])/2.0
    else:
        magave1 = mag1[magidx]

    if filt == "w":
        magave2 = (mag2[1]+mag2[2]+mag2[3])/3.0
    elif filt == "c":
        magave2 = (mag2[1]+mag2[2])/2.0
    elif filt == "o":
        magave2 = (mag2[2]+mag2[3])/2.0
    else:
        magave2 = mag2[magidx]

    ii = np.where(~np.isnan(magave1))[0]
    f = interp.interp1d(tmag1[ii], magave1[ii], fill_value='extrapolate')
    maginterp1 = f(tt)
    #plt.plot(tt,maginterp1+zp_best1,'--',c=color1,linewidth=2,label='1 Component')
    #plt.plot(tt,maginterp1+zp_best1-errorbudget,'-',c=color1,linewidth=2)
    #plt.plot(tt,maginterp1+zp_best1+errorbudget,'-',c=color1,linewidth=2)
    #plt.fill_between(tt,maginterp1+zp_best1-errorbudget,maginterp1+zp_best1+errorbudget,facecolor=color1,alpha=0.2)

    ii = np.where(~np.isnan(magave2))[0]
    f = interp.interp1d(tmag2[ii], magave2[ii], fill_value='extrapolate')
    maginterp2 = f(tt)
    plt.plot(tt,maginterp2+zp_best2,'--',c=color2,linewidth=2,label='2 Component')
    plt.plot(tt,maginterp2+zp_best2-errorbudget,'-',c=color2,linewidth=2)
    plt.plot(tt,maginterp2+zp_best2+errorbudget,'-',c=color2,linewidth=2)
    plt.fill_between(tt,maginterp2+zp_best2-errorbudget,maginterp2+zp_best2+errorbudget,facecolor=color2,alpha=0.2)

    plt.ylabel('%s'%filt,fontsize=48,rotation=0,labelpad=40)
    plt.xlim([0.0, 14.0])
    plt.ylim([-17.0,-11.0])
    plt.gca().invert_yaxis()
    plt.grid()

    if cnt == 1:
        ax1.set_yticks([-18,-16,-14,-12,-10])
        plt.setp(ax1.get_xticklabels(), visible=False)
        #l = plt.legend(loc="upper right",prop={'size':36},numpoints=1,shadow=True, fancybox=True)
    elif not cnt == len(filts):
        plt.setp(ax2.get_xticklabels(), visible=False)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)

ax1.set_zorder(1)
plt.xlabel('Time [days]',fontsize=48)
plt.savefig(plotName, bbox_inches='tight')
plt.close()

print(stop)

plotName = "%s/models_panels_twocomponent.pdf"%(plotDir)
#plt.figure(figsize=(20,18))
plt.figure(figsize=(20,28))

tini, tmax, dt = 0.0, 21.0, 0.1
tt = np.arange(tini,tmax,dt)

cnt = 0
for filt, color, magidx in zip(filts,colors,magidxs):
    cnt = cnt+1
    vals = "%d%d%d"%(len(filts),1,cnt)
    if cnt == 1:
        ax1 = plt.subplot(eval(vals))
    else:
        ax2 = plt.subplot(eval(vals),sharex=ax1,sharey=ax1)

    if not filt in data_out: continue
    samples = data_out[filt]
    t, y, sigma_y = samples[:,0], samples[:,1], samples[:,2]
    idx = np.where(~np.isnan(y))[0]
    t, y, sigma_y = t[idx], y[idx], sigma_y[idx]
    if len(t) == 0: continue

    idx = np.where(np.isfinite(sigma_y))[0]
    plt.errorbar(t[idx],y[idx],sigma_y[idx],fmt='o',c=color, markersize=16)

    idx = np.where(~np.isfinite(sigma_y))[0]
    plt.errorbar(t[idx],y[idx],sigma_y[idx],fmt='v',c=color, markersize=16)

    if filt == "w":
        magave1 = (mag1[1]+mag1[2]+mag1[3])/3.0
    elif filt == "c":
        magave1 = (mag1[1]+mag1[2])/2.0
    elif filt == "o":
        magave1 = (mag1[2]+mag1[3])/2.0
    else:
        magave1 = mag1[magidx]

    if filt == "w":
        magave2 = (mag2[1]+mag2[2]+mag2[3])/3.0
    elif filt == "c":
        magave2 = (mag2[1]+mag2[2])/2.0
    elif filt == "o":
        magave2 = (mag2[2]+mag2[3])/2.0
    else:
        magave2 = mag2[magidx]

    #ii = np.where(~np.isnan(magave1))[0]
    #f = interp.interp1d(tmag1[ii], magave1[ii], fill_value='extrapolate')
    #maginterp1 = f(tt)
    #plt.plot(tt,maginterp1+zp_best1,'--',c=color1,linewidth=2,label='1 Component')
    #plt.plot(tt,maginterp1+zp_best1-errorbudget,'-',c=color1,linewidth=2)
    #plt.plot(tt,maginterp1+zp_best1+errorbudget,'-',c=color1,linewidth=2)
    #plt.fill_between(tt,maginterp1+zp_best1-errorbudget,maginterp1+zp_best1+errorbudget,facecolor=color1,alpha=0.2)

    ii = np.where(~np.isnan(magave2))[0]
    f = interp.interp1d(tmag2[ii], magave2[ii], fill_value='extrapolate')
    maginterp2 = f(tt)
    plt.plot(tt,maginterp2+zp_best2,'--',c=color2,linewidth=2,label='2 Component')
    plt.plot(tt,maginterp2+zp_best2-errorbudget,'-',c=color2,linewidth=2)
    plt.plot(tt,maginterp2+zp_best2+errorbudget,'-',c=color2,linewidth=2)
    plt.fill_between(tt,maginterp2+zp_best2-errorbudget,maginterp2+zp_best2+errorbudget,facecolor=color2,alpha=0.2)

    plt.ylabel('%s'%filt,fontsize=48,rotation=0,labelpad=40)
    plt.xlim([0.0, 14.0])
    plt.ylim([-17.0,-11.0])
    plt.gca().invert_yaxis()
    plt.grid()

    if cnt == 1:
        ax1.set_yticks([-18,-16,-14,-12,-10])
        plt.setp(ax1.get_xticklabels(), visible=False)
        #l = plt.legend(loc="upper right",prop={'size':36},numpoints=1,shadow=True, fancybox=True)
    elif not cnt == len(filts):
        plt.setp(ax2.get_xticklabels(), visible=False)
    plt.xticks(fontsize=32)
    plt.yticks(fontsize=32)

ax1.set_zorder(1)
plt.xlabel('Time [days]',fontsize=48)
plt.savefig(plotName, bbox_inches='tight')
plt.close()
