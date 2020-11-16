import numpy as np
import math
from ntrp45 import ntrp45
from feval import feval

def odezero(ntrpfun,eventfun,eventargs,v,t,y,tnew,ynew,t0,h,f,idxNonNegative):
    
    
    tol = 128*max(np.finfo(float(t)).eps,np.finfo(float(tnew)).eps)
    tol = min(tol, abs(tnew - t))
    
    tout = np.array([])
    yout = np.zeros((len(y),0))
    iout = np.array([])
    tdir = math.copysign(1,tnew - t)
    stop = 0
    rmin=np.finfo(float).tiny
    
    
    tL = t
    yL = y
    vL = v
    [vnew,isterminal,direction] = feval(eventfun,tnew,ynew,eventargs)
    if len(direction)==0:
      direction = np.zeros(len(vnew))
    tR = tnew
    yR = ynew
    vR = vnew
    
    ttry = tR
    
    
    while True:
        lastmoved = 0
        while True:
            indzc=[i for i in range(len(direction)) if direction[i]*(vR-vL)>=0 and math.copysign(1,vR)!=math.copysign(1,vL)]
            if len(indzc)==0:
                if lastmoved != 0:
                    raise Exception('ode45:odezero:LostEvent')
                else:
                    return tout,yout,iout,vnew,stop
            
            delta = tR - tL
            if abs(delta) <= tol:
                break
            
            if (tL == t) and any([vL[index]==0 and vR[index]!=0 for index in indzc]):
                ttry = tL + tdir*0.5*tol
            else:
                change = 1
                for j in indzc:
                    if vL==0:
                        if (tdir*ttry > tdir*tR) and (vtry[j] != vR):
                            maybe = 1.0 - vR * (ttry-tR) / ((vtry[j]-vR) * delta)
                            if (maybe < 0) or (maybe > 1):
                                maybe = 0.5
                        else:
                            maybe = 0.5
                    elif vR == 0.0:
                        if (tdir*ttry < tdir*tL) and (vtry[j] != vL):
                            maybe = vL * (tL-ttry) / ((vtry[j]-vL) * delta)
                            if (maybe < 0) or (maybe > 1):
                                maybe = 0.5
                        else:
                            maybe = 0.5
                    else:
                        maybe = -vL / (vR - vL)
                    if maybe < change:
                        change = maybe
                change = change * abs(delta)
            
    
                change = max(0.5*tol, min(change, abs(delta) - 0.5*tol))
            
                ttry = tL + tdir * change
                
    
            ytry = ntrp45(ttry,t,y,h,f)[:,0]
            vtry = feval(eventfun,ttry,ytry,[])[0,0]
    
            indzc=[i for i in range(len(direction)) if direction[i]*(vtry-vL)>=0 and math.copysign(1,vtry)!=math.copysign(1,vL)]
            
            if len(indzc)!=0:
                tswap = tR
                tR = ttry
                ttry = tswap
                yswap = yR
                yR = ytry
                ytry = yswap
                vswap = vR
                vR = vtry
                vtry = vswap
                if lastmoved == 2:
                    pass #TODO
                    
                lastmoved = 2
            else:
                tswap = tL
                tL = ttry
                ttry = tswap
                yswap = yL
                yL = ytry
                ytry = yswap
                vswap = vL
                vL = vtry
                vtry = vswap
                
                if lastmoved == 1:
                    pass #TODO
                    
                lastmoved = 1
            
        
        #To Complete
        j = np.ones((1,len(indzc)))
        tout = tR
        yout = yR
        iout = indzc
        
        if isterminal[0]==1:
            if tL != t0:
                stop = 1
        

        break
    return tout,yout,iout,vnew,stop