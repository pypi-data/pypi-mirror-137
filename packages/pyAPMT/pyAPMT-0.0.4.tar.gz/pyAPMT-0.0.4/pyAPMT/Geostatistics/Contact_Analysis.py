# -*- coding: utf-8 -*-
"""
Contact analysis

"""

# Author: Sebastian Avalos <sebastian.avalos@apmodtech.com>
#         Advanced Predictive Modeling Technology
#         www.apmodtech.com/pyAPMT/
#         Jan-2022
#
# License: MIT License


# All submodules and packages
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

font = {'family' : 'DejaVu Sans',
        'size'   : 8}

matplotlib.rc('font', **font)
#sns.set()
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

def ElementsInCategory(DF):
	'''Categorical elements as list on a selected column'''
	Cat = []
	for ii in DF:
		if ii not in Cat:
			Cat.append(ii)
	return Cat
#
def ExtractDataPerCategory(DF, East, North, Elevation, Element, Category, \
                           V1):
	'''Extract subset of the drill hole database per category as numpy array'''
	SubSet1 = DF[DF[Category] == V1]
	V1_m = SubSet1[[East, North, Elevation, Element]].to_numpy()
	return V1_m
#
def DistancesAndValues(M1, M2):
	'''Left-Right matrices with Distance, Element value'''
	L_Mat = np.zeros((len(M1[:,0])*len(M2[:,0]),3))
	R_Mat = np.zeros((len(M1[:,0])*len(M2[:,0]),3))
	L_Mat[:,2], R_Mat[:,2] = 1, 1
	count = 0
	for d_1 in range(len(M1[:,0])):
		for d_2 in range(len(M2[:,0])):	
			Dis = np.linalg.norm(M1[d_1,0:3]-M2[d_2,0:3])
			#print(Dis)
			L_Mat[count,0], R_Mat[count,0] = -Dis/2, Dis/2
			L_Mat[count,1], R_Mat[count,1] = M1[d_1,3], M2[d_2,3]
			#L_Mat[count,2], R_Mat[count,2] = M1[d_1,4], M2[d_2,4]
			count += 1
	L_Mat = L_Mat[np.argsort(L_Mat[:, 0])][::-1]
	R_Mat = R_Mat[np.argsort(R_Mat[:, 0])]
	return L_Mat, R_Mat
#
def MovingWindow(Vec, space=5, MaxDist=50):
	Left = False
	if np.sum(Vec[:,0]) < 0:
		Left = True
		Vec[:,0] = Vec[:,0]*-1
	delta = np.around(space/2, decimals=1)
	TotalSteps = np.arange(delta, MaxDist+delta, delta)
	VecVals = np.zeros((len(TotalSteps), 2))
	VecVals[:,0] = TotalSteps
	VecVals[:,1] = np.NaN 
	count = 0
	for ind_p in TotalSteps:
		tVec = Vec[(ind_p - delta <= Vec[:,0]) & (Vec[:,0] <= ind_p + delta)]
		if tVec.size != 0:
			VecVals[count, 1] = np.sum(np.multiply(tVec[:,1], tVec[:,2]))/np.sum(tVec[:,2])
		count += 1
	if Left == True:
		VecVals[:,0] = VecVals[:,0]*-1
	return VecVals
#
def PlotContacs(DH_DB, Domains, East, North, \
                Elevation, Element, MaxDistance, Zones = None, ImName=None):

	if Zones == None:
		Zones = ElementsInCategory(DF=DH_DB[Domains])
	
	Num = len(Zones)
	if Num == 2:
		fig, axs = plt.subplots(1, 1, figsize=(3,2))
	elif Num == 3:
		fig, axs = plt.subplots(1, 3, figsize=(9,2))
	elif Num > 3:
		fig, axs = plt.subplots(int(np.ceil(Num*(Num-1)/2/5)), 5, \
		                        figsize=(15,2*int(np.ceil(Num*(Num-1)/2/5))))
	 
	plt.subplots_adjust(left=0.125  , bottom=0.1, right=0.9 , top=0.9 , \
	                    wspace=0.3, hspace=0.3)
	
	co_m = 0
	for f_L in range(Num):
		for f_R in range(f_L+1, Num):
			ArgParameters = dict(East=East, North=North, Elevation=Elevation, \
				                 Element=Element, Category=Domains)
			
			SubMat_L = ExtractDataPerCategory(DF=DH_DB, V1=Zones[f_L], \
			                                  **ArgParameters)
			SubMat_R = ExtractDataPerCategory(DF=DH_DB, V1=Zones[f_R], \
			                                  **ArgParameters)
			tL_Mat, tR_Mat = DistancesAndValues(M1=SubMat_L, M2=SubMat_R)
			L_VecVals = MovingWindow(Vec=tL_Mat, space=5, MaxDist=MaxDistance)
			R_VecVals = MovingWindow(Vec=tR_Mat, space=5, MaxDist=MaxDistance)
			if Num == 2:
				axs.plot(L_VecVals[:,0], L_VecVals[:,1], ls='--', \
						               marker="1", lw=0.9, c="orange", label=Zones[f_L])
				axs.plot(R_VecVals[:,0], R_VecVals[:,1], ls='--', \
						               marker="2", lw=0.9, c="darkblue", label=Zones[f_R])
				axs.axvline(x=0, lw=0.5, c="grey")
				axs.set_ylabel(Element)
				axs.set_xlabel("Relative distance (m)")
				axs.set_xlim(-MaxDistance*1.1, MaxDistance*1.1)
				axs.legend()
			
			elif Num == 3:
				axs[co_m].plot(L_VecVals[:,0], L_VecVals[:,1], ls='--', \
				            marker="1", lw=0.9, c="orange", label=Zones[f_L])
				axs[co_m].plot(R_VecVals[:,0], R_VecVals[:,1], ls='--', \
				            marker="2", lw=0.9, c="darkblue", label=Zones[f_R])
				axs[co_m].axvline(x=0, lw=0.5, c="grey")
				axs[co_m].set_ylabel(Element)
				axs[co_m].set_xlabel("Relative distance (m)")
				axs[co_m].set_xlim(-MaxDistance*1.1, MaxDistance*1.1)
				axs[co_m].legend()
				
			else:
				axs[int(co_m/5), int(co_m%5)].plot(L_VecVals[:,0], L_VecVals[:,1],\
				        ls='--', marker="1", lw=0.9, c="orange", label=Zones[f_L])
				axs[int(co_m/5), int(co_m%5)].plot(R_VecVals[:,0], R_VecVals[:,1],\
				        ls='--', marker="2", lw=0.9, c="darkblue", label=Zones[f_R])	
				axs[int(co_m/5), int(co_m%5)].axvline(x=0, lw=0.5, c="grey")
				axs[int(co_m/5), int(co_m%5)].set_ylabel(Element)
				axs[int(co_m/5), int(co_m%5)].set_xlabel("Relative distance (m)")
				axs[int(co_m/5), int(co_m%5)].set_xlim(-MaxDistance*1.1, \
				                                       MaxDistance*1.1)
				axs[int(co_m/5), int(co_m%5)].legend()				
			co_m +=1
	
	if Num > 3:
		co_m = 0
		for jj in range(int(np.ceil(Num*(Num-1)/2/5))):
			for kk in range(5):
				if co_m >= int(Num*(Num-1)/2):
					fig.delaxes(axs[int(co_m/5), int(co_m%5)])
				co_m += 1
				
	
	fig.tight_layout()
	if ImName != None:
		plt.savefig(f"{ImName}",  dpi=500, bbox_inches="tight")	

	return plt.show()
