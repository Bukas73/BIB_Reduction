import uproot
import random
import awkward as ak
#from uproot_methods import TLorentzVectorArray
from collections import OrderedDict
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys, os
#from scipy import constants
import math
from math import pi
import matplotlib.animation as animation
import pandas
import seaborn as sns

import pickle
import sys
from awkward.layout import ListOffsetArray64

# TimeResList = [0.03,0.05,0.1]
# ThetaResList = [0.015,0.025,0.035]

import matplotlib.cm as cm

#palette = sns.husl_palette(6,l=0.5,s=1)
palette = sns.color_palette("bright", as_cmap=True)
print(palette)

cmaps = [
    sns.light_palette(palette[0],n_colors=50,reverse=True,as_cmap=True),
    sns.light_palette(palette[3],n_colors=50,reverse=True,as_cmap=True),
    sns.light_palette(palette[1],n_colors=50,reverse=True,as_cmap=True),
    sns.light_palette(palette[4],n_colors=50,reverse=True,as_cmap=True),
    sns.light_palette(palette[2],n_colors=50,reverse=True,as_cmap=True),
    sns.light_palette(palette[8],n_colors=50,reverse=True,as_cmap=True),
]
print(cmaps[0])

'''
cmaps = [
    # cm.get_cmap("spring"),
    # cm.get_cmap("summer"),
    # cm.get_cmap("autumn"),
    # cm.get_cmap("winter"),

    cm.get_cmap("Reds_r"),
    cm.get_cmap("Blues_r"),
    cm.get_cmap("Greys_r"),
    cm.get_cmap("Greens_r"),
    cm.get_cmap("Purples_r"),
    cm.get_cmap("Oranges_r"),
    ]
print(cmaps[0])
'''

#for mass in masses:
#    for decay in decays:

Files = []
BIBFiles = []

#Files.append(f"EffDictPickles_sim/DiHiggs_EffDicts_barrel.pickle")
Files.append(f"EffDictPickles_sim/ll_m60_d5_EffDicts_barrel.pickle")
Files.append(f"EffDictPickles_sim/ll_m20_d5_EffDicts_barrel.pickle")
Files.append(f"EffDictPickles_sim/ll_m20_d3_EffDicts_barrel.pickle")
Files.append(f"EffDictPickles_sim/ll_m60_d3_EffDicts_barrel.pickle")
Files.append(f"EffDictPickles_sim/ll_m60_d1_EffDicts_barrel.pickle")
Files.append(f"EffDictPickles_sim/ll_m20_d1_EffDicts_barrel.pickle")

#Files.append(f"EffDictPickles_sim/ll_m40_d4_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles_sim/m40_d4_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles_sim/DiHiggs_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/bb_m60_d5_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/bb_m20_d5_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/bb_m20_d2_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/MonoHiggs_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/{process}_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/DiHiggs_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/bb_{process}_EffDicts_barrel.pickle")
#Files.append(f"EffDictPickles/{process}_EffDicts_barrel.pickle")
BIBFiles.append(f"EffDictPickles/BIB_EffDicts_barrel.pickle")

# starttimecut=0
# # endtimecut=starttimecut+200""""""""""""""
# endtimecut=-1

fig, ax = plt.subplots(nrows=1, ncols=1)

# https://matplotlib.org/stable/gallery/subplots_axes_and_figures/zoom_inset_axes.html

for imap, file in enumerate(Files):

    # with open(f"fromLarry_052722/EffDict_{TimeRes}_{ThetaRes}.pickle","rb") as f:
    with open(file,"rb") as f:
    # with open(sys.argv[1],"rb") as f:
        sig_object_file = pickle.load(f)

    with open(BIBFiles[0],"rb") as f:
        bg_object_file = pickle.load(f)

    [sigEffsDict,bgEffsDict] = [sig_object_file[0],bg_object_file[0]]

    colors = cmaps[imap](np.linspace(0.15, 0.8, len(bgEffsDict) ) )
    icolor=0
    timecutlist = list(sigEffsDict.keys() )
    #start,end = 0,-1
    #if (TimeRes,ThetaRes)==(0,0):
    #    timecutlist = timecutlist[1:]
        # colors = cmaps[imap](np.linspace(-2.0, 0.8, len(bgEffsDict) ) )

    for i,timecut in enumerate(timecutlist[:-1]):
        #sigEffsDict[timecutlist[i]] = sigEffsDict[timecutlist[i]][1:]
        #bgEffsDict[timecutlist[i]] = bgEffsDict[timecutlist[i]][1:]
        #nonzero_filter = np.where(bgEffsDict[timecutlist[i]] == 0, True, False)
        #sigEffsDict[timecutlist[i]] = sigEffsDict[timecutlist[i]][nonzero_filter]
        #bgEffsDict[timecutlist[i]] = bgEffsDict[timecutlist[i]][nonzero_filter]
        ribbon = plt.fill(
            np.append(
                sigEffsDict[timecutlist[i]][:],
                sigEffsDict[timecutlist[i+1]][-1::-1]
                ),
            np.append(
                bgEffsDict[timecutlist[i]][:],
                bgEffsDict[timecutlist[i+1]][-1::-1]
                ),
            c=colors[icolor],alpha=1.0
        )
        icolor+=1

    ax.set_xlabel("Collision Product Efficiency")
    ax.set_ylabel("BIB Efficiency")
    ax.set_yscale('log')

    # ax.set_xlim(0.7, 1.01)
    # ax.set_ylim(5e-4, 1.5e0)
    # ax.set_xscale('log')



    ax.set_xlim(0.5, 1.02)
    ax.set_ylim(5e-3, 1.5e0)
    #ax.set_xlim(0.0, 1.02)
    #ax.set_ylim(1.7e-4, 1.6)

    

    # inset axes....
    axins = ax.inset_axes([0.08, 0.65, 0.35, 0.33])

    for imap,file in enumerate(Files):

        # with open(f"fromLarry_052722/EffDict_{TimeRes}_{ThetaRes}.pickle","rb") as f:
        with open(file,"rb") as f:
            sig_object_file = pickle.load(f)

        with open(BIBFiles[0],"rb") as f:
            bg_object_file = pickle.load(f)

        sigEffsDict = sig_object_file[0]
        bgEffsDict = bg_object_file[0] 

        colors = cmaps[imap](np.linspace(0.15, 0.8, len(bgEffsDict) ) )
        icolor=0
        timecutlist = list(sigEffsDict.keys() )
        start,end = 0,-1
        #if (TimeRes,ThetaRes)==(0,0):
        #    timecutlist = timecutlist[1:]
            # colors = cmaps[imap](np.linspace(-2.0, 0.8, len(bgEffsDict) ) )

        for i,timecut in enumerate(timecutlist[:-1]):
            sigEffsDict[timecutlist[i]] = sigEffsDict[timecutlist[i]][start:end]
            bgEffsDict[timecutlist[i]] = bgEffsDict[timecutlist[i]][start:end]
            axins.fill(
                np.append(
                    sigEffsDict[timecutlist[i]][:],
                    sigEffsDict[timecutlist[i+1]][-2::-1]
                    ),
                np.append(
                    bgEffsDict[timecutlist[i]][:],
                    bgEffsDict[timecutlist[i+1]][-2::-1]
                    ),
                c=colors[icolor],alpha=1.0
            )
            icolor+=1

    # sub region of the original image
    x1, x2, y1, y2 = 0.96,1.00,8e-2,4e-1
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_yscale('log')
    axins.set_yticks([0.1,0.2,0.3,0.4],[0.1,0.2,0.3,0.4])
    #axins.set_yticklabels([0.1,0.2,0.3,0.4],minor=True)
    #axins.get_yaxis().set_major_formatter(mpl.ticker.ScalarFormatter())


    # axins.plot([0.99,0.99], [1e-3,1e-0],    "--",c="k",lw=1.5)
    # axins.plot([0.98,0.99], [1.8e-2,1.8e-2],"--",c="k",lw=1.5)
    # axins.plot([0.98,0.99], [y:=0.14,y],"--",c="k",lw=1.5)
    # axins.plot([0.98,0.99], [y:=0.55,y],"--",c="k",lw=1.5)


    rect,c = ax.indicate_inset_zoom(axins, edgecolor="black",alpha=0.8,lw=0.5)
    plt.setp(c, lw=0.3,alpha=0.4)


    



# imap=1
# with open(f"fromLarry/EffDict_0.02_0.01.pickle","rb") as f:
#     object_file = pickle.load(f)
# [sigEffsDict,bgEffsDict] = object_file
# colors = cmaps[imap](np.linspace(0.15, 0.8, len(bgEffsDict) ) )
# icolor=0
# timecutlist = list(sigEffsDict.keys() )
# icut = 30
# jcut = 8
# x,y=sigEffsDict[timecutlist[icut]][jcut], bgEffsDict[timecutlist[icut]][jcut]
# thetaCut = np.linspace(0.5*ThetaRes,10*ThetaRes,20)[jcut] #fix
# # axins.plot( x,y, "ow",mew=0.5,mec="k" )
# axins.annotate(
#     rf'$|t_\Delta|<{timecutlist[icut]:0.3f}$, $|\theta_\Delta|<{thetaCut:0.3f}$',
#     xy=(x,y),  xycoords='data',
#             xytext=(1.1, 0.25), textcoords='axes fraction',
#             arrowprops=dict(arrowstyle="simple,head_width=0.5,head_length=0.5,tail_width=0.1",
#                             connectionstyle="arc3,rad=-0.1",facecolor="k"),
#             horizontalalignment='left', verticalalignment='top',
#             )


# imap=4
# with open(f"fromLarry/EffDict_0.05_0.05.pickle","rb") as f:
#     object_file = pickle.load(f)
# [sigEffsDict,bgEffsDict] = object_file
# colors = cmaps[imap](np.linspace(0.15, 0.8, len(bgEffsDict) ) )
# icolor=0
# timecutlist = list(sigEffsDict.keys() )
# icut = 63
# jcut = 19
# x,y=sigEffsDict[timecutlist[icut]][jcut], bgEffsDict[timecutlist[icut]][jcut]
# print(x,y)
# thetaCut = np.linspace(0.5*ThetaRes,10*ThetaRes,20)[jcut]
# # axins.plot( x,y, "ow",mew=0.5,mec="k" )
# axins.annotate(
#     rf'$|t_\Delta|<{timecutlist[icut]:0.3f}$, $|\theta_\Delta|<{thetaCut:0.3f}$',
#     xy=(x,y),  xycoords='data',
#             xytext=(1.2, 0.65), textcoords='axes fraction',
#             arrowprops=dict(arrowstyle="simple,head_width=0.5,head_length=0.5,tail_width=0.1",
#                             connectionstyle="arc3,rad=-0.05",facecolor="k"),
#             horizontalalignment='left', verticalalignment='top',
#             )










# legend
def drawLegendEntry(x,y,label,cmap):
    ax.text(x,y, label,
            verticalalignment='center', horizontalalignment='left',
            multialignment="left", transform=ax.transAxes, fontsize=10, c="k")
    plt.plot([x-0.03],[y+0.004],"s",c=palette[cmap],ms=6,mew=0.5,mec="k",alpha=1.0,transform=ax.transAxes)



# (0.02,0.1),
# (0.05,0.1),
# (0.1,0.1),
# (0.05,2),

#h_bar = 6.58212e-16 #GeV*ns==eV*s

#Decays = {}
#Decays[decay] = pow(10,3-decay)

#plt.title(f"m = {mass} GeV, "+r"$c\tau$ = "+"{:1.1e}".format(Decays[decay])+" mm")

drawLegendEntry(0.55,0.02+0.01,r"$m=20$ [GeV], $c\tau=0.01$ [mm]",3)
drawLegendEntry(0.55,0.06+0.01,r"$m=60$ [GeV], $c\tau=0.01$ [mm]",0)
drawLegendEntry(0.55,0.10+0.01,r"$m=20$ [GeV], $c\tau=1$ [mm]",1) 
drawLegendEntry(0.55,0.14+0.01,r"$m=60$ [GeV], $c\tau=1$ [mm]",4)
drawLegendEntry(0.55,0.18+0.01,r"$m=20$ [GeV], $c\tau=100$ [mm]",8)
drawLegendEntry(0.55,0.22+0.01,r"$m=60$ [GeV], $c\tau=100$ [mm]",2)
#drawLegendEntry(0.5,0.14+0.03,r"$m=60$ [GeV], $c\tau=10$ [mm]",cmaps[3])
#f"m = {processes[1][4]}0 GeV, "+r"$\tau$ = "+"{:1.3e}".format(Decays[decay])+" ns",cmaps[idecay+1])
#drawLegendEntry(0.3,0.14+0.03,r"$\mu \mu \rightarrow H^0 \rightarrow h_s h_s \rightarrow b b b b, m=20GeV, c\tau=.01mm$",cmaps[3])
#drawLegendEntry(0.3,0.14+0.03,r"$\mu \mu \rightarrow H^0 \rightarrow h_s h_s \rightarrow b b b b, m=60GeV, c\tau=10mm$",cmaps[0])
#drawLegendEntry(0.3,0.18+0.03,r"$\mu \mu \rightarrow H^0 \rightarrow h_s h_s \rightarrow b b b b, m=60GeV, c\tau=.01mm$",cmaps[2])

#drawLegendEntry(0.6,0.18+0.03,r"$\sigma(t)=50$ ps, $\sigma(\theta)=2$ rad",cmaps[4])
#plt.legend()

#colors=["#00f","#30c","#60a","#909","#a06","#c03","#f00"]

#for inum, num in enumerate([1,40,60,75,90,95,99]):

#    curve=np.array([sigEffsDict[timecutlist[-1*num]],bgEffsDict[timecutlist[-1*num]]])
#    ax.plot(curve[0],curve[1],'-',c=colors[inum])[0]


# (0.0,0.0),
# (0.01,0.01),
# (0.02,0.01),
# (0.05,0.01),
# # (0.02,0.05),
# (0.05,0.05),

# drawLegendEntry(0.6,0.18+0.03,r"$\sigma(t)=0$ ps, $\sigma(\theta)=0$ rad",cmaps[0])
# drawLegendEntry(0.6,0.14+0.03,r"$20$ ps, $0.01$ rad",cmaps[1])
# drawLegendEntry(0.6,0.10+0.03,r"$20$ ps, $0.05$ rad",cmaps[2])
# drawLegendEntry(0.6,0.06+0.03,r"$50$ ps, $0.01$ rad",cmaps[3])
# drawLegendEntry(0.6,0.02+0.03,r"$50$ ps, $0.05$ rad",cmaps[4])


# ax.text(0.98, 0.94, r"$\sqrt{s}=1.5$ TeV Circular Muon Collider",
#         verticalalignment='bottom', horizontalalignment='right',
#         transform=ax.transAxes, fontsize=10, c="k")
'''
ax.text(0.98, 0.84, r"$\sqrt{s}=1.5$ "+"TeV Circular Muon Collider\nMARS15 BIB, CLIC_o3_v14_mod4\nVertex Detector",
        verticalalignment='bottom', horizontalalignment='right',
        transform=ax.transAxes, fontsize=10, c="k",backgroundcolor='1')
'''




#plt.tight_layout()
plt.title("ll decay")

plt.savefig(f"ROC_Ribbons/ll_decays.png")
plt.clf()