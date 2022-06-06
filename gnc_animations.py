# this python code has all the animation visualizations used in the course

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import clear_output
import matplotlib.pyplot as plt
from numpy.random import randn
from time import sleep
from matplotlib import rc
import matplotlib as mpl

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


def animate_2Dbot(X,U,T,param,robot_scale,frame_num,speedup):
  robot_scale =0.5;
  fig = plt.figure()
  ax = fig.add_subplot(aspect='equal')
  ax.set_xlim(-2.2, 2.2)
  ax.set_ylim(-2.2, 2.2)
  triangle = ax.add_patch(plt.Polygon(np.array([[-0.4,0.3],[-0.4,-0.3],[0.4,-0.01],[1.2,0],[0.4,0.01]])*robot_scale, True))
  line, = ax.plot([0, 0,3], [0, -1,5], lw=1, c='c', alpha=0.5) # draw a line 
  line.set_data([0],[0])
  transform = mpl.transforms.Affine2D().rotate_deg(-45) + mpl.transforms.Affine2D().translate(-5,-5) 
  triangle.set_transform(transform+ax.transData)

  # determine skip amount from number of frames
  #frame_num =300
  #speedup =2
  tail = 15
  skip = np.floor(len(X)/frame_num)
  if skip < 1:
    skip=1
    frame_num = len(X)
  skip=int(skip)

  def animate(i):
    #print(i)
    transform = mpl.transforms.Affine2D().rotate(X[skip*i][2]) + mpl.transforms.Affine2D().translate(X[skip*i][0],X[skip*i][1]) 
    triangle.set_transform(transform+ax.transData)
    if i>1:
      if i>tail:
        Xtemp= np.array(X[i-tail:i])
        line.set_data(Xtemp[:,0],Xtemp[:,1])
      else:
        Xtemp= np.array(X[0:i])
        line.set_data(Xtemp[:,0],Xtemp[:,1])

  ani = animation.FuncAnimation(fig, animate, frames=frame_num, repeat=True, interval=int(dt*1000*skip/speedup)) # interval determines speed in ms
  print("Number of frames :",frame_num)
  plt.close()
  return ani