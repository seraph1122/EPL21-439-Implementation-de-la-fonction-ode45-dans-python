import numpy as np
from feval import feval
import itertools

def odearguments(FcnHandlesUsed, solver, ode, tspan, y0, options, extras): 
    
    neq=len(y0)
    
    if None in tspan:
        raise Exception('{}:odearguments:TspanNoneTypeValues'.format(solver))
    
    if FcnHandlesUsed:
        if len(tspan)==0 or len(y0)==0:
            raise Exception('{}:odearguments:TspanOrY0NotSupplied'.format(solver))
        if len(tspan)<2:
            raise Exception('{}:odearguments:SizeTspan'.format(solver))
        htspan = abs(tspan[1]-tspan[0])
        ntspan = len(tspan)
        t0 = tspan[0]
        nex = 2
        tfinal = tspan[1]
        args = extras
        
    neq = len(y0)
    
    if t0 == tfinal:
        raise Exception('{}:odearguments:TspanEndpointsNotDistinct'.format(solver))
    tdir = np.sign(tfinal-t0)
    if any(tdir*np.diff(tspan)<=0):
        raise Exception('{}:odearguments:TspanNotMonotonic'.format(solver))
    
    
    f0=feval(ode,t0,y0,extras)

    shape=f0.shape
    if len(shape)==1:
        m=shape[0]
        n=1
    else:
        m=shape[0]
        n=shape[1]
    
    if n>1:
        raise Exception('{}:odearguments:FoMustReturnCol'.format(solver))
    elif m!=neq:
        raise Exception('{}:odearguments:SizeIC'.format(solver))
        
    
    classT0 = (np.array(t0)).dtype
    classY0 = (np.array(y0)).dtype
    classF0 = f0.dtype
    dataType=max(classT0,classY0,classF0)
    
    rtol=1e-3
    if rtol < 100 * np.finfo(dataType).eps:
        rtol = 100 * np.finfo(dataType).eps
        raise Warning('{}:odearguments:RelTolIncrease'.format(solver))
    
    atol=1e-6
    normcontrol=0
    normy=[]
    threshold=atol/rtol
    hmax=0.1*abs(tfinal-t0)
    htry=[]
    
    odeFcn=ode
    
    
    
    return neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, args, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType