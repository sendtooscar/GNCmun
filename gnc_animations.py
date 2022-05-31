# this python code has all the animation visualizations used in the course

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import clear_output
import matplotlib.pyplot as plt
from numpy.random import randn
from time import sleep
from matplotlib import rc

rc('animation', html='jshtml')

def animate_isl_pendulum(X,U,T,param,fps,duration):
  fps = 30
  duration = 1
  fig = plt.figure()
  ax = fig.add_subplot(aspect='equal')
  line, = ax.plot([0, 0], [0, -1], lw=3, c='k') # draw a line
  bob_radius = 0.08
  circle = ax.add_patch(plt.Circle([0,-1], bob_radius, fc='r', zorder=3)) # draw a circle
  ax.set_xlim(-1.2, 1.2)
  ax.set_ylim(-1.2, 1.2)
  def animate(i):
    px = np.sin(X[20*i][0])
    py = -np.cos(X[20*i][0])
    line.set_data([0, px], [0, py])
    circle.set_center((px, py))

  print("Number of frames :", int(np.size(T)/20))
  ani = animation.FuncAnimation(fig, animate, frames=int(np.size(T)/20), repeat=True,
                              interval=20)

  plt.close()
  return ani