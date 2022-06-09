# this python code has all the animation visualizations used in the course

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from IPython.display import clear_output
import matplotlib.pyplot as plt
from numpy.random import randn
from time import sleep
from matplotlib import rc
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection
from jaxlie import SO3
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

rc('text', usetex=True)
rc('font', size=9)
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
  dt = param[0]
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


def animate_ahrs(X,U,T,param,frame_num,speedup):
  class Arrow3D(FancyArrowPatch):
      def __init__(self, xs, ys, zs, *args, **kwargs):
          FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
          self._verts3d = xs, ys, zs

      def draw(self, renderer):
          xs3d, ys3d, zs3d = self._verts3d
          xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
          self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
          FancyArrowPatch.draw(self, renderer)

  dt = param[0]
  skip = np.floor(len(X)/frame_num)
  if skip < 1:
    skip=1
    frame_num = len(X)
  skip=int(skip)
  scale =2.0
  points = np.array([[-1, -1, -1],
                    [1, -1, -1 ],
                    [1, 1, -1],
                    [-1, 1, -1],
                    [-1, -1, 1],
                    [1, -1, 1 ],
                    [1, 1, 1],
                    [-1, 1, 1]])

  quat = np.array([1.,0.,0.,0.])
  Rot = SO3(quat)
  #Rot = SO3.from_rpy_radians(np.pi/10,0.,np.pi/6)


  Z = np.zeros((8,3))
  for i in range(8): Z[i,:] = Rot.apply(points[i,:])
  Z = scale*Z

  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')

  r = [-1,1]

  #X, Y = np.meshgrid(r, r)
  # plot vertices
  #ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])

  # list of sides' polygons of figure
  verts = [[Z[0],Z[1],Z[2],Z[3]],
  [Z[4],Z[5],Z[6],Z[7]], 
  [Z[0],Z[1],Z[5],Z[4]], 
  [Z[2],Z[3],Z[7],Z[6]], 
  [Z[1],Z[2],Z[6],Z[5]],
  [Z[4],Z[7],Z[3],Z[0]]]

  # plot sides
  #cube = ax.add_collection3d(Poly3DCollection(verts, 
  # facecolors='red', linewidths=0, edgecolors='r', alpha=.5))
  #cube = Poly3DCollection(verts,  facecolors='cyan', linewidths=0.2, edgecolors='c', alpha=1)
  #ax.add_collection3d(cube)
   
  Rotmat = Rot.as_matrix().T
  #print(Rotmat)
  col = ['r','g','b']
  arr_vec =[]
  i=0
  for v in Rotmat:
    #line, = ax.plot([0, 3*scale*v[0]], [0, 3*scale*v[1]],[0, 3*scale*v[2]], lw=2, color=col[i], alpha=0.8) # draw a line
    arr = Arrow3D([0, 4.5*scale*v[0]], [0, 4.5*scale*v[1]],[0, 4.5*scale*v[2]], mutation_scale=10, 
                lw=2, arrowstyle="-|>", color=col[i],alpha=0.5)
    arr_vec.append(arr)
    ax.add_artist(arr_vec[i])
    
  ax.set_xlim(-7,7)
  ax.set_ylim(-7,7)
  ax.set_zlim(-7,7)

  # Hide grid lines
  ax.grid(False)

  # Hide axes ticks
  ax.set_xticks([])
  ax.set_yticks([])
  ax.set_zticks([])
  ax.w_xaxis.line.set_visible(False)
  ax.w_yaxis.line.set_visible(False)
  ax.w_zaxis.line.set_visible(False)
  #plt.axis('off')
  arr_vec[0].set_zorder(4)
  arr_vec[1].set_zorder(4)
  arr_vec[2].set_zorder(4)

  print(arr_vec[2])

  ax.plot([-0.05,-0.05],[0,0],[0,0],'ok',alpha=0.5,zorder=5)

  plt.rcParams['figure.figsize'] = [8, 8]


  #updating (animate)
  def animate(j):
    #Rot = SO3.from_rpy_radians(np.pi/100*j,0.,np.pi/50*j)
    quat = np.array([X[skip*j][0],X[skip*j][1],X[skip*j][2],X[skip*j][3]])
    Rot = SO3(quat)

    Z = np.zeros((8,3))
    for i in range(8): 
      Z[i,:] = Rot.apply(points[i,:])
    Z = scale*Z
    # list of sides' polygons of figure
    verts = [[Z[0],Z[1],Z[2],Z[3]],
    [Z[4],Z[5],Z[6],Z[7]], 
    [Z[0],Z[1],Z[5],Z[4]], 
    [Z[2],Z[3],Z[7],Z[6]], 
    [Z[1],Z[2],Z[6],Z[5]],
    [Z[4],Z[7],Z[3],Z[0]]]

    #cube.set_verts(verts)  #ok
    handle_text.set_text('$(%.1f^{\circ},%.1f^{\circ},%.1f^{\circ})$'%(round(Rot.compute_roll_radians()/np.pi*180,1),round(Rot.compute_pitch_radians()/np.pi*180,1),round(Rot.compute_yaw_radians()/np.pi*180,1)))

    Rotmat = Rot.as_matrix().T
    i=0
    for v in Rotmat:
      arr_vec[i]._verts3d[0][1] =4*scale*v[0]
      arr_vec[i]._verts3d[1][1] =4*scale*v[1]
      arr_vec[i]._verts3d[2][1] =4*scale*v[2]
      i=i+1

  handle_text = ax.text(-7, -7, 7,'test', ha='left', va='top')
  handle_text.set_text('$(%s^{\circ},%s^{\circ},%s^{\circ})$'%(round(Rot.compute_roll_radians(),1),round(Rot.compute_pitch_radians(),1),round(Rot.compute_yaw_radians(),1)))

  ani = animation.FuncAnimation(fig, animate, frames=frame_num, repeat=True, interval=int(dt*1000*skip/speedup))
  print("Number of frames :",frame_num)
  print(arr_vec[2]._verts3d)
  print(arr_vec[1]._verts3d)
  print(arr_vec[1].get_zorder())
  plt.close()
  return ani