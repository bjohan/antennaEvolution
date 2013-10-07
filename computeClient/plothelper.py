from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
class PlotHelper:
	def __init__(self):
		pass

	def plot3d(self,azimuth, elevation, z):
		X, Y = np.meshgrid(azimuth, elevation)
		fig = plt.figure()
		ax = fig.gca(projection = '3d')
		surf = ax.plot_surface(X,Y, z, rstride = 1, cstride = 1, linewidth = 0, antialiased = False, cmap = 'cool')
		ma = max(max(z))
		mi = min(min(z))
		ax.set_zlim(mi, ma)
		fig.colorbar(surf, shrink = 0.5, aspect = 5)
		plt.xlabel('azimuth')
		plt.ylabel('elevation')
		#plt.zlabel('value')
		plt.show()
		
	def plotColorMap(self, azimuth, elevation, z):
		X, Y = np.meshgrid(azimuth, elevation)
		p = pcolor(X,Y,array(z), cmap = 'cool')
		#xaxis(aximuth)
		axis('tight')
		xlabel('azimuth')
		ylabel('elevation')
		colorbar()
		show()
		#print dir(p)

