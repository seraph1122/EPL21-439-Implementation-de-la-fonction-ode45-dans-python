import numpy as np
from ntrp45 import ntrp45
from odearguments import odearguments
from odeget import odeget
from odeevents import odeevents
from feval import feval
from odezero import odezero
from odemass import odemass
from odemassexplicit import odemassexplicit
from odenonnegative import odenonnegative
import math
from odefinalize import odefinalize

def ode45(odefun,tspan,y0,options={},varargin=[]):
    
    solver_name='ode45'

    nsteps=0
    nfailed = 0
    nfevals = 0
  
    
    neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, odeArgs, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType = odearguments(odefun, tspan, y0, options, varargin)
    nfevals = nfevals + 1
    #dataType='float64'
    
    
    refine=max(1,odeget(options,'Refine',4))
    if len(tspan) > 2:
        outputAt = 'RequestedPoints'
    elif refine == 1:
        outputAt = 'SolverSteps'
    else:
        outputAt = 'RefinedSteps'
        s=np.array(range(1,refine))/refine
    
    
    printstats = (odeget(options,'Stats','off') == 'on')
    
    
    haveEventFcn,eventFcn,eventArgs,valt,teout,yeout,ieout=odeevents(odeFcn,t0,y0,options,varargin)
    
    
    Mtype, M, Mfun =  odemass(odeFcn,t0,y0,options,varargin)
    if Mtype > 0:
        odeFcn,odeArgs = odemassexplicit(Mtype,odeFcn,odeArgs,Mfun,M)
        f0 = feval(odeFcn,t0,y0,odeArgs)
        nfevals = nfevals + 1;
    
     
        
    idxNonNegative = odeget(options,'NonNegative',[])
    nonNegative = False
    if len(idxNonNegative) != 0:
        odeFcn,thresholdNonNegative = odenonnegative(odeFcn,y0,threshold,idxNonNegative);
        f0 = feval(odeFcn,t0,y0,odeArgs)
        nfevals = nfevals + 1
        nonNegative = True
    
    
    t=t0
    y=y0
    
    #Memory Allocation
    nout=1
    yout=np.array([],dtype=dataType)
    tout=np.array([],dtype=dataType)
    if ntspan > 2:
          tout = np.zeros((1,ntspan),dtype=dataType)
          yout = np.zeros((neq,ntspan),dtype=dataType)
    else:
        chunk = min(max(100,50*refine), refine+math.floor(math.pow(2,11)/neq))
        tout = np.zeros((1,chunk),dtype=dataType)
        yout = np.zeros((neq,chunk),dtype=dataType)
        
    nout = 1
    tout[nout-1] = t
    yout[:,nout-1] = y.copy()
    
    
    #Initialize method parameters
    stop=0
    power = 1/5
    A = np.array([1./5., 3./10., 4./5., 8./9., 1., 1.],dtype='float64')
    B = np.array([[1./5.,         3./40.,    44./45.,   19372./6561.,      9017./3168.,       35./384.    ],
                [0.,           9./40.,    -56./15.,  -25360./2187.,     -355./33.,         0.           ],
                [0.,           0.,       32./9.,    64448./6561.,      46732./5247.,      500./1113.    ],
                [0.,           0.,       0.,       -212./729.,        49./176.,          125./192.     ],
                [0.,           0.,       0.,       0.,               -5103./18656.,     -2187./6784.  ], 
                [0.,           0.,       0.,       0.,               0.,               11./84.       ],
                [0.,           0.,       0.,       0.,               0.,               0.           ]],dtype='float64')
    
    
    E = np.array([[71./57600.], [0.], [-71./16695.], [71./1920.], [-17253./339200.], [22./525.], [-1./40.]],dtype='float64')
    f=np.zeros((neq,7),dtype='float64')
    hmin=16*np.spacing(float(t))
    np.set_printoptions(precision=16)    
    
    if htry==0:
        absh = min(hmax, htspan)
        if normcontrol:
            rh=(np.linalg.norm(f0)/ max(normy, threshold))/ (0.8 * math.pow(rtol,power))
        else:
            if isinstance(threshold,list):
                rh=np.linalg.norm(f0 / np.maximum(np.abs(y),threshold),np.inf) / (0.8 * math.pow(rtol,power))
            else:
                rh=np.linalg.norm(f0 / np.maximum(np.abs(y),np.repeat(threshold,len(y))),np.inf) / (0.8 * math.pow(rtol,power))
        if (absh * rh) > 1:
            absh =1/rh
        absh = max(absh,hmin)
    else:
        absh=min(hmax,max(hmin,htry))
    
    f[:,0]=f0
    
    ynew=np.zeros(neq,dtype='float64')
    
    done=False
    while not done:
        hmin = 16*np.spacing(float(t))
        absh = min(hmax, max(hmin, absh))
        h = tdir * absh
                

        if 1.1*absh >= abs(tfinal - t):
            h = tfinal - t
            absh = abs(h)
            done = True
        
        nofailed=True
        while True:
            hA = h * A
            hB = h * B
            f[:,1]=feval(odeFcn,t+hA[0],y+np.matmul(f,hB[:,0]),odeArgs)
            f[:,2]=feval(odeFcn,t+hA[1],y+np.matmul(f,hB[:,1]),odeArgs)
            f[:,3]=feval(odeFcn,t+hA[2],y+np.matmul(f,hB[:,2]),odeArgs)
            f[:,4]=feval(odeFcn,t+hA[3],y+np.matmul(f,hB[:,3]),odeArgs)
            f[:,5]=feval(odeFcn,t+hA[4],y+np.matmul(f,hB[:,4]),odeArgs)

            
            tnew = t + hA[5]
            if done:
              tnew = tfinal
            h = tnew - t 
            
            
            ynew=y+np.matmul(f,hB[:,5])
            f[:,6]=feval(odeFcn,tnew,ynew,odeArgs)
            nfevals=nfevals+6

            
            NNrejectStep = False
            if normcontrol:
                normynew = np.linalg.norm(ynew)
                errwt = max(max(normy,normynew),threshold)
                err = absh * np.linalg.norm(np.matmul(f,E)[:,0])/errwt
                if nonNegative and err <= rtol and any([True for i in idxNonNegative if ynew[i] < 0]):
                    errNN = np.linalg.norm([max(0, -1*ynew[i]) for i in idxNonNegative]) / errwt
                    if errNN > rtol:
                        err = errNN
                        NNrejectStep = True
            else:
                denom=np.maximum(np.maximum(np.abs(y),np.abs(ynew)),threshold)
                err=absh*np.linalg.norm(np.divide(np.matmul(f,E)[:,0],denom),np.inf)
                if nonNegative and err <= rtol and any([True for i in idxNonNegative if ynew[i] < 0]):
                    errNN = np.linalg.norm(np.divide([max(0, -1*ynew[i]) for i in idxNonNegative],thresholdNonNegative), np.inf)
                    if errNN > rtol:
                        err = errNN
                        NNrejectStep =True



            if err > rtol:
                nfailed = nfailed + 1
                if absh <= hmin:
                    raise Warning("ode45: ode45: IntegrationTolNotMet "+str(t)+" "+str(hmin))
                    return odefinalize(solver_name,printstats,[nsteps,nfailed,nfevals],nout,tout,yout,haveEventFcn,teout,yeout,ieout)

                    
                if nofailed:
                    nofailed = False
                    if NNrejectStep:
                        absh = max(hmin, 0.5*absh)
                    else:
                        absh = max(hmin, absh * max(0.1, 0.8 * math.pow(rtol/err,power)))
                else:
                    absh = max(hmin, 0.5*absh)
                h= tdir * absh
                done = False
            else:
                NNreset_f7 = False
                if nonNegative and any([True for i in idxNonNegative if ynew[i]<0]):
                    for j in idxNonNegative:
                        ynew[j] = max(ynew[j],0)
                        
                    if normcontrol:
                        normynew = np.linalg.norm(ynew)
                    NNreset_f7=True
                
                break
            
            
            
        nsteps+=1
        
        if haveEventFcn:
            te,ye,ie,valt,stop=odezero([],eventFcn,eventArgs,valt,t,np.transpose(np.array([y])),tnew,np.transpose(np.array([ynew])),t0,h,f,idxNonNegative)
            if len(te)!=0:
                if len(teout)==0:
                    teout=np.copy(te)
                else:
                    teout=np.append(teout,te)
                    
                if len(yeout)==0:
                    yeout=np.copy(ye)
                else:
                    yeout=np.append(yeout,ye,axis=1)
                
                if len(ieout)==0:
                    ieout=np.copy(ie)
                else:
                    ieout=np.append(ieout,ie)
                    
                if stop:
                    taux = t + (te[-1] - t)*A
                    discard,f[:,1:7]=ntrp45(taux,t,np.transpose(np.array([y])),h,f,idxNonNegative)
                    tnew = te[-1]
                    ynew = ye[:,-1]
                    h = tnew - t
                    done = True
                    
        
        
        if outputAt == "SolverSteps":
            nout_new=1
            tout_new=tnew
            yout_new=ynew
        elif outputAt == "RefinedSteps":    
            tref=t+(tnew-t)*s
            nout_new=refine
            tout_new=tref.copy()
            tout_new=np.append(tout_new,tnew)
            yout_new,discard=ntrp45(tref,t,np.transpose(np.array([y])),h,f,idxNonNegative)
            yout_new=np.append(yout_new,np.transpose(np.array([ynew])),axis=1)
        elif outputAt == "RequestedPoints":
            nout_new=0
            tout_new=np.array([])
            yout_new=np.array([])
            while nex <= ntspan:
                if tdir * (tnew - tspan[nex-1]) < 0:
                    if haveEventFcn and stop:
                        nout_new=nout_new+1
                        tout_new=np.appaned(tout_new,tnew)
                        if len(yout_new)==0:
                            yout_new=np.transpose(np.array([ynew]))
                        else:
                            yout_new=np.append(yout_new,np.transpose(np.array([ynew])),axis=1)
                    break
                
                nout_new = nout_new + 1
                tout_new = np.append(tout_new, tspan[nex-1])
                
                if tspan[nex-1] == tnew:
                    yout_temp = np.transpose(np.array([ynew]))    
                else:
                    yout_temp,discard = ntrp45(tspan[nex-1],t,y,h,f,idxNonNegative)
                
                if len(yout_new)==0:
                    yout_new=yout_temp
                else:
                    yout_new=np.append(yout_new,yout_temp,axis=1)
                nex = nex + 1
        
        
        if nout_new > 0:
            oldnout=nout
            nout=nout+nout_new
            if nout>len(tout[0]):
                talloc=np.zeros((1,chunk),dtype=dataType)
                tout=np.array([np.append(tout,talloc)])
                yalloc=np.zeros((neq,chunk),dtype=dataType)
                yout=np.append(yout,yalloc,axis=1)
            for i in range(oldnout,nout):
                tout[0,i] = tout_new[i-oldnout]
                yout[:,i] = yout_new[:,i-oldnout]
            
        
        if done:
            break
        
        
        if nofailed:
            temp = 1.25*math.pow((err/rtol),power)
            if temp > 0.2:
                absh=absh/temp
            else:
                absh=5.0*absh
                
            
        t=tnew
        y=ynew.copy()
        if normcontrol:
            normy=normynew
        
        if NNreset_f7:
            f[:,6]=feval(odeFcn,tnew,ynew,odeArgs)
            nfevals = nfevals+1
        f[:,0]=f[:,6]
        
    
    return odefinalize(solver_name,printstats,[nsteps,nfailed,nfevals],nout,tout,yout,haveEventFcn,teout,yeout,ieout)
    

    
            
            
            
            
            
            
            
            