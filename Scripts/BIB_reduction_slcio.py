from pyLCIO import IOIMPL
from pyLCIO import EVENT, UTIL
from math import *
from array import array
import numpy as np
import pickle

def defineBranches(reader):

    hitCollection = event.getCollection('VertexBarrelCollection')

    if len(hitCollection)==0:
        return [],0,0,0,0,0,0,0,0,0

    mcpCollection = event.getCollection('MCParticle')

    print(f"  Hits: {len(hitCollection)}")
    print(f"  MCPs: {len(mcpCollection)}")

    PoX = np.array([])
    PoY = np.array([])
    PoZ = np.array([])
    MoX = np.array([])
    MoY = np.array([])
    MoZ = np.array([])
    Time= np.array([])
    
    Link = np.full(len(hitCollection),-1)
    Link_list = []

    for hit in hitCollection:
        PoX = np.append(PoX,hit.getPosition()[0])
        PoY = np.append(PoY,hit.getPosition()[1])
        PoZ = np.append(PoZ,hit.getPosition()[2])
        MoX = np.append(MoX,hit.getMomentum()[0])
        MoY = np.append(MoY,hit.getMomentum()[1])
        MoZ = np.append(MoZ,hit.getMomentum()[2])
        Time=np.append(Time,hit.getTime())

        Link_list.append(hit.getMCParticle())

        hit_pT = np.sqrt(np.square(hit.getMomentum()[0]) + np.square(hit.getMomentum()[1]))
        mc_pT  = np.sqrt(np.square(hit.getMCParticle().getMomentum()[0]) + np.square(hit.getMCParticle().getMomentum()[1]))

    pdg = np.array([])

    Parent_dict = {}

    Parent_list = np.array([], dtype=int)

    Nummpcs = len(mcpCollection)
    imcp = Nummpcs

    for mcp in reversed(mcpCollection):

        imcp -= 1

        pdg = np.append(pdg,mcp.getPDG())
        
        if len(mcp.getParents()) != 0:
            Parent_dict[imcp] = mcp.getParents()[0]
            Parent_list = np.append(Parent_list,0)
        else:
            Parent_list = np.append(Parent_list,-1)

        keys_arr   = np.asarray(list(Parent_dict.keys()))
        values_arr = np.asarray(list(Parent_dict.values()))

        indices_with_parent = keys_arr[values_arr==mcp]
        for index in indices_with_parent:
            Parent_list[Nummpcs-int(index)-1] = imcp
            del Parent_dict[index]
        
        if mcp in Link_list:
            for ilink, link in enumerate(Link_list):
                if mcp==link:
                    Link[ilink] = imcp

    pdg = pdg[::-1]

    mcP = np.asarray(Parent_list)[::-1]
    
    return PoX,PoY,PoZ,MoX,MoY,MoZ,Time,Link,pdg,mcP

def getDescendantIndexes(MCParent_Array,Parent_Indexes):
    descendant_indexes = np.array([], dtype=int)
    for index in Parent_Indexes:
        descendant_indexes = np.append(descendant_indexes,np.nonzero(MCParent_Array == index)[0])
    return descendant_indexes

SpeedOfLight = 299792458/1e6 # mm/ns

Processes = []

for mass in range(60,61,20):
    for decay in range(1,2):
        Processes.append(f"m{mass}_d{decay}")

reader = IOIMPL.LCFactory.getInstance().createLCReader()
reader.setReadCollectionNames(["VertexBarrelCollection","MCParticle"])

for Process in Processes:

    Theta_arr = np.array([])
    ThEx_arr = np.array([])
    DelTh_arr = np.array([])
    Time_arr = np.array([])
    TEx_arr = np.array([])
    DelT_arr = np.array([])
    DelTAbs_arr = np.array([])
    PoX_arr = np.array([])
    PoY_arr = np.array([])
    PoZ_arr = np.array([])
    MoX_arr = np.array([])
    MoY_arr = np.array([])
    MoZ_arr = np.array([])
    mcmx_arr= np.array([])
    mcmy_arr= np.array([])
    mcmz_arr= np.array([])

    for ifile in range(1,101):

        print(ifile)

        reader.open(f"LLP_sim_files/{Process}_1-1000/SimHits_{Process}_bb_{ifile}.slcio")
        #reader.setReadCollectionNames(["VertexBarrelCollection"])

        for ievt, event in enumerate(reader):

            print(f"  Event Num: {event.getEventNumber()}")

            PoX,PoY,PoZ,MoX,MoY,MoZ,Time,Link,pdg,mcP = defineBranches(reader)
            
            if len(PoX)==0:
                continue

            LinkFilter = Link != -1

            PoX = PoX[LinkFilter]
            PoY = PoY[LinkFilter]
            PoZ = PoZ[LinkFilter]
            MoX = MoX[LinkFilter]
            MoY = MoY[LinkFilter]
            MoZ = MoZ[LinkFilter]
            Time=Time[LinkFilter]
            Link=Link[LinkFilter]

            MoR = np.sqrt(np.square(MoX) + np.square(MoY))
            MomentumFilter = MoR > 1

            PoX = PoX[MomentumFilter]
            PoY = PoY[MomentumFilter]
            PoZ = PoZ[MomentumFilter]
            MoX = MoX[MomentumFilter]
            MoY = MoY[MomentumFilter]
            MoZ = MoZ[MomentumFilter]
            Time=Time[MomentumFilter]
            Link=Link[MomentumFilter]

            if len(Link)==0:
                continue
            
            LinkedToDescendantFilter = []

            for hit in Link:
            
                hs_flag = False

                parent_index = mcP[hit]

                while parent_index != -1:
                    
                    if pdg[parent_index] == 25:
                        hs_flag = True

                    parent_index = mcP[parent_index]
            
                LinkedToDescendantFilter.append(hs_flag)

            LinkedToDescendantFilter = np.asarray(LinkedToDescendantFilter)

            PoX = PoX[LinkedToDescendantFilter]
            PoY = PoY[LinkedToDescendantFilter]
            PoZ = PoZ[LinkedToDescendantFilter]
            MoX = MoX[LinkedToDescendantFilter]
            MoY = MoY[LinkedToDescendantFilter]
            MoZ = MoZ[LinkedToDescendantFilter]
            Time=Time[LinkedToDescendantFilter]
            

            MoR = np.sqrt(np.square(MoX) + np.square(MoY))
            PoR = np.sqrt(np.square(PoX) + np.square(PoY))
            Pos = np.sqrt(np.square(PoX) + np.square(PoY) + np.square(PoZ))
            Theta = np.arctan2(MoR,MoZ)
            ThEx = np.arctan2(PoR,PoZ)
            DelTh = np.absolute(np.subtract(Theta,ThEx))
            TEx = Pos/SpeedOfLight
            DelT = np.subtract(Time,TEx)
            DelTAbs = np.absolute(DelT)

            Theta_arr = np.append(Theta_arr,Theta)
            ThEx_arr = np.append(ThEx_arr,ThEx)
            DelTh_arr = np.append(DelTh_arr,DelTh)
            Time_arr = np.append(Time_arr,Time)
            TEx_arr = np.append(TEx_arr,TEx)
            DelT_arr = np.append(DelT_arr,DelT)
            DelTAbs_arr = np.append(DelTAbs_arr,DelTAbs)
            PoX_arr = np.append(PoX_arr,PoX)
            PoY_arr = np.append(PoY_arr,PoY)
            PoZ_arr = np.append(PoZ_arr,PoZ)
            MoX_arr = np.append(MoX_arr,MoX)
            MoY_arr = np.append(MoY_arr,MoY)
            MoZ_arr = np.append(MoZ_arr,MoZ)


    pickleoutput = [Theta_arr,ThEx_arr,DelTh_arr,Time_arr,TEx_arr,DelT_arr,DelTAbs_arr,PoX_arr,PoY_arr,PoZ_arr,MoX_arr,MoY_arr,MoZ_arr]
    picklefilename = f"HitInfoPickles/bb_{Process}_1-1000_ThExDelTExDelAbsPxyzMxyz_barrel.pickle"
    with open(picklefilename, 'wb') as f:
        pickle.dump(pickleoutput,f)

reader.close()

#pickleoutput = [Theta_arr,ThEx_arr,DelTh_arr,Time_arr,TEx_arr,DelT_arr,DelTAbs_arr,PoX_arr,PoY_arr,PoZ_arr,MoX_arr,MoY_arr,MoZ_arr]
#picklefilename = f"HitInfoPickles/Dihiggs_ThExDelTExDelAbsPxyzMxyz_barrel.pickle"
#with open(picklefilename, 'wb') as f:
#    pickle.dump(pickleoutput,f)

'''
totalpickleoutput = [[]]*13
totalpickleoutput = np.asarray(totalpickleoutput)

for ifile in range(1,101):
    print(ifile)
    with open(f"HitInfoPickles/Dihiggs_ThExDelTExDelAbsPxyzMxyz_{ifile}_barrel.pickle", 'rb') as f:
        content = pickle.load(f)
        content = np.asarray(content)
    totalpickleoutput = np.append(totalpickleoutput,content,axis=1)

with open('HitInfoPickles/Dihiggs_ThExDelAbsPxyzMxyz_barrel.pickle', 'wb') as out:
    pickle.dump(totalpickleoutput, out, protocol=pickle.HIGHEST_PROTOCOL)


#Create ROC Dicts

print(f"Max DelTh: {max(DelTh_arr)}")
print(f"Max DelT:  {max(DelT_arr)}")

tDeltaValues = np.linspace(0.001,0.3,100)
thetaDeltaValues = np.linspace(0.01,2.7,100)

NumEntries = len(Theta_arr)

EffDict = {}

for tVal in tDeltaValues:

    DelTimeCut = np.where(DelTAbs_arr < tVal)

    EfficiencyVals = np.array([])

    for thetaVal in thetaDeltaValues:

        DelThetaCut = np.where(DelTh_arr < thetaVal)

        NumKeptEntries = len(np.intersect1d(DelTimeCut,DelThetaCut))
        Efficiency = NumKeptEntries/NumEntries
        EfficiencyVals = np.append(EfficiencyVals,Efficiency)

    EffDict[tVal] = EfficiencyVals

pickleoutput = [EffDict,NumEntries]
picklefilename = f"EffDictPickles/DiHiggs_EffDicts_barrel.pickle"
with open(picklefilename,'wb') as f:
    pickle.dump(pickleoutput,f)
'''
