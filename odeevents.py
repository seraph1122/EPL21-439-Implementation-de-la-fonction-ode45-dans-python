import numpy as np
from odeget import odeget
from feval import feval

def odeevents(ode,t0,y0,options,extras):
    
    haveeventfun = False
    eventArgs = None
    eventValue = None
    teout = np.array([])
    yeout = np.array([])
    ieout = np.array([])
    
    eventFcn=odeget(options,'Events',None)
    
    if eventFcn==None:
        return haveeventfun,eventFcn,eventArgs,eventValue,teout,yeout,ieout
    
    haveeventfun = True
    eventArgs = extras
#    mainArgs = np.array([t0, y0])
#    extraArgs = np.array(eventArgs)
#    allArgs = np.append(mainArgs, extraArgs)
    eventValue,isterminal,direction = feval(eventFcn,t0,y0,eventArgs)
    
    return haveeventfun,eventFcn,eventArgs,eventValue,teout,yeout,ieout