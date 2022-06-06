# python file having all utility functions used by GNCmun course
import numpy as np
import math 

print("The following functions are loaded :  rotnp('axis',angle)  skew(v)  wrapToPi(angle)")

def rotnp(a,b):   
      c=math.cos(b)
      s=math.sin(b)
      if a=="z":
        R = np.array([[c,-s,0],
        [s,c,0],
        [0,0,1]])
      if a=="x":
        R = np.array([[1,0,0],
        [0,c,-s],
        [0,s,c]])
      if a=="y":
        R = np.array([[c,0,s],
        [0,1,0],
        [-s,0,c]])
      return(R)

def skew(v):
    if len(v.shape) is not 1:
      raise ValueError("v should be 1 dimentional")
    elif v.shape[0] is not 3:
      raise ValueError("v should be 1 dimentional and have 3 elemnets")
    else:
      V = np.array( [[ 0, -v[2], v[1]],
                    [v[2],  0,  -v[0]],
                    [-v[1],  v[0],   0]])
    return V


def wrapToPi(x):
    xwrap = np.remainder(x, 2 * np.pi)
    mask = np.abs(xwrap) > np.pi
    if len(x.shape) is not 1 :
      if mask :
        xwrap -= 2 * np.pi * np.sign(xwrap)
      else :
        xwrap = x
    else :
      xwrap[mask] -= 2 * np.pi * np.sign(xwrap[mask])
    #mask1 = x < 0
    #mask2 = np.remainder(x, np.pi) == 0
    #mask3 = np.remainder(x, 2 * np.pi) != 0
    #xwrap[mask1 & mask2 & mask3] -= 2 * np.pi
    return xwrap