
def odeevents(FcnHandlesUsed,ode,t0,y0,options,extras):
    
    haveeventfun = 0
    eventArgs = None
    eventValue = None
    teout = None
    yeout = None
    ieout = None
    
    eventFcn=None
    
    return haveeventfun,eventFcn,eventArgs,eventValue,teout,yeout,ieout