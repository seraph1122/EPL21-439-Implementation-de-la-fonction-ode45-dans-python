import numpy as np
import math

def odezero(ntrpfun,eventfun,eventargs,v,t,y,tnew,ynew,t0,h,f,idxNonNegative):
    
    
    tol = 128*max(np.finfo(float(t)).eps,np.finfo(float(tnew)).eps)
    tol = min(tol, abs(tnew - t))
    
    tout = np.array([])
    yout = np.array([])
    iout = np.array([])
    tdir = math.sign(tnew - t)
    stop = 0
    rmin=np.finfo(float).tiny
    
    tout,yout,iout,vnew,stop=0,0,0,0,0
    return tout,yout,iout,vnew,stop