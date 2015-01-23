import numpy as np
import matplotlib.pyplot as pl
import matplotlib.animation as animation
import types
import copy

def relaxate(V):
  tempV = np.vstack( (np.zeros(nx).astype(float), V, np.zeros(nx).astype(float)) )
  tempV = np.hstack( (np.zeros((ny+2,1)).astype(float), tempV, np.zeros((ny+2,1)).astype(float)) )
  tempV = (0.25)*(np.roll(tempV, 1, 0) + np.roll(tempV, -1, 0) + np.roll(tempV, 1, 1) + np.roll(tempV, -1, 1))
  # copy over V
  newV = copy.copy(V)
  # reassign the interior
  newV[1:-1,1:-1] = tempV[2:-2, 2:-2]
  diff = np.max(np.abs(newV - V))
  return newV, diff

# http://matplotlib.org/examples/pylab_examples/contourf_demo.html
def plotate(V):
  global nx, ny
  fig, ax = pl.subplots()
  X,Y = np.meshgrid( np.linspace(0.0, 5.0, nx), np.linspace(-1.0, 1.0, ny) )
  contour_set = ax.contourf(X, Y, V, 6, cmap=pl.cm.cool, origin='lower')
  cbar = fig.colorbar(contour_set)
  cbar.ax.set_ylabel('potential')
  pl.show()
  pl.close(fig)

'''
  global nx, ny
  fig, ax = pl.subplots()
  X,Y = np.meshgrid( np.linspace(0.0, 5.0, nx), np.linspace(-1.0, 1.0, ny) )
  im = ax.contourf(X, Y, V, 6, cmap=pl.cm.hot_r, origin='lower')

  # monkey hack
  # http://matplotlib.1069221.n5.nabble.com/Matplotlib-1-1-0-animation-vs-contour-plots-td18703.html
  def setvisible(self,vis): 
     for c in self.collections: c.set_visible(vis) 
  im.set_visible = types.MethodType(setvisible,im,None) 
  im.axes = ax
  pl.close(fig)
  return im
'''

def generate_contour(V, ax):
  return [ax.imshow(V, cmap=pl.cm.cool)]
  

# set up dimensions of problem
nx = 50
ny = 50

# define the minimum difference for "stabilization"
epsilon = 1e-4

# initialize the potential grid to zero
V = np.zeros((ny, nx)).astype(float)

# set up an example boundary conditions (first row = 1)
V[0, :] = 1
V[-1,:] = 1

ims = []

fig, ax = pl.subplots(figsize=(6,6))
V, diff = relaxate(V)
print diff
ims.append(generate_contour(V, ax))
while diff > epsilon:
  print diff
  V, diff = relaxate(V)
  ims.append(generate_contour(V, ax))

im_ani = animation.ArtistAnimation(fig, ims, interval=10, repeat_delay=3000, blit=True)
im_ani.save('im.mp4', dpi=300, metadata={'artist':'Giordon'})

pl.close(fig)
