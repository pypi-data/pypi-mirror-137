# -*- coding: utf-8 -*-
"""
Class dedicated to Drill-Holes database

"""

# Author: Sebastian Avalos <sebastian.avalos@apmodtech.com>
#         Advanced Predictive Modeling Technology
#         www.apmodtech.com/pyAPMT/
#         Jan-2022
#
# License: MIT License


# All submodules and packages
import pandas as pd
import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt

# pyAPMT functions
from . import Contact_Analysis
from .Contact_Analysis import PlotContacs

__all__ = ['DrillHoles', 'PlotContacs']

class DrillHoles:
	
	def __init__(self, DH_DB, East, North, Elevation, \
	             HoleID=None, From = None, To = None, Length = None):
		self.DH = pd.read_csv(DH_DB)
		self.East = East
		self.North = North
		self.Elevation = Elevation
		self.HoleID = HoleID		
		self.From = From
		self.To = To
		self.Length = Length
		self.Header = list(self.DH.columns.values)
		
	def Describe(self):
		return self.DH.describe()
	
	def ElemInDom(self, Dom):
		'''Categorical elements as list on a selected column'''
		Cat = []
		for ii in self.DH[Dom]:
			if ii not in Cat:
				Cat.append(ii)
		return Cat	
		
	def SampleLength(self):
		if 'Length' not in self.Header:
			self.DH['Length'] = self.DH['From'] - self.DH['To'] 
		return None
	
	def ContactAnalysis(self, Dom, Var, MaxDis, \
	                    SubDom =  None, OutputImage=None): 
		return PlotContacs(DH_DB=self.DH, Domains=Dom, Element=Var, MaxDistance=MaxDis, \
		                   East=self.East , North=self.North , \
		                   Elevation=self.Elevation, Zones = SubDom, ImName = OutputImage)
	
	def Plot_3D(self, Var, Title = None, VMax = None, OutputName=None):
		mlab.options.offscreen = False
		figure = mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1), size=(750, 750))
		if VMax != None:
			pts_2 = mlab.points3d(self.DH[self.East], self.DH[self.North], self.DH[self.Elevation],\
					                  self.DH[Var], mask_points=1, scale_factor=10, colormap = 'rainbow',\
					    scale_mode='none', mode='cube', vmin=0, vmax=VMax)
		else:
			pts_2 = mlab.points3d(self.DH[self.East], self.DH[self.North], self.DH[self.Elevation],\
				    self.DH[Var], mask_points=1, scale_factor=10, colormap = 'rainbow',\
				    scale_mode='none', mode='cube', vmin=0)
	
		mesh = mlab.pipeline.delaunay2d(pts_2) 
		mlab.outline(mesh)  
		mlab.colorbar(orientation='vertical', nb_labels=(2), label_fmt='%.1f')
		
		if Title != None:
			mlab.title(Title, size=0.5)
		if OutputName != None:
			mlab.savefig(OutputName)
		
		return mlab.show()
	
	
	