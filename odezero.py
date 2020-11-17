import numpy as np
import math
from ntrp45 import ntrp45
from feval import feval

def odezero(ntrpfun,eventfun,eventargs,v,t,y,tnew,ynew,t0,h,f,idxNonNegative):
    
    
    tol = 128*max(np.finfo(float(t)).eps,np.finfo(float(tnew)).eps)
    tol = min(tol, abs(tnew - t))
    
    tout = np.array([])
    yout = np.array([])
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
            indzc=[i for i in range(len(direction)) if direction[i]*(vR[i]-vL[i])>=0 and math.copysign(1,vR[i])!=math.copysign(1,vL[i])]
            
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
                    if vL[j]==0:
                        if (tdir*ttry > tdir*tR) and (vtry[j] != vR[j]):
                            maybe = 1.0 - vR[j] * (ttry-tR) / ((vtry[j]-vR[j]) * delta)
                            if (maybe < 0) or (maybe > 1):
                                maybe = 0.5
                        else:
                            maybe = 0.5
                    elif vR[j] == 0.0:
                        if (tdir*ttry < tdir*tL) and (vtry[j] != vL[j]):
                            maybe = vL[j] * (tL-ttry) / ((vtry[j]-vL) * delta)
                            if (maybe < 0) or (maybe > 1):
                                maybe = 0.5
                        else:
                            maybe = 0.5
                    else:
                        maybe = -vL[j] / (vR[j] - vL[j])
                    if maybe < change:
                        change = maybe
                change = change * abs(delta)
            
    
                change = max(0.5*tol, min(change, abs(delta) - 0.5*tol))
            
                ttry = tL + tdir * change
                
    
            ytry, discard = ntrp45(ttry,t,y,h,f)
            ytry=ytry[:,0]
            vtry = feval(eventfun,ttry,ytry,[])[0]
            
            indzc=[index for index in range(len(direction)) if direction[index]*(vtry[index]-vL[index])>=0 and math.copysign(1,vtry[index])!=math.copysign(1,vL[index])]
            
            
            
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

        
        ntout=np.array([tR for index in range(len(indzc))])
        nyout=np.tile(np.transpose([yR]),len(indzc))
        niout=np.array([indzc[index] for index in range(len(indzc))])
        if len(tout)==0:
            tout=ntout
            yout=nyout
            iout=niout
        else:
            tout=np.append(tout,ntout)
            yout=np.append(yout,nyout)
            iout=np.append(iout,niout)
            
            
        
        if any([isterminal[index]==1 for index in indzc]):
            if tL != t0:
                stop = 1
            break
    return tout,yout,iout,vnew,stop