utils.py

# python file having all utility functions used by GNCmun course
import numpy as np
import math 

print("The following functions are loaded :  rotnp('axis',angle)")

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
