import numpy as np
from feval import feval
from odeoptions import odeoptions
from odeget import odeget
import numpy as np
import itertools
from inspect import signature



def odearguments(solver, ode, tspan, y0, options, extras): 
    
    
    
    #Checking y0
    if not isinstance(y0,np.ndarray) and not isinstance(y0,list):
        raise TypeError('odearguments: y0: must be a list or ndarray')
    else:
        if len(y0)==0:
            raise ValueError('odearguments: y0: must have at least one initial value')
        neq=len(y0)
    
    #Checking tspan
    if not isinstance(tspan,np.ndarray) and not isinstance(tspan,list):
        raise TypeError('odearguments: tspan: must be a list or ndarray')
    else:
        if len(tspan) < 2:
            raise ValueError('odearguments: tspan: must have at least two initial values')    
    
    
    #Checking ode
    if not callable(ode):
        raise TypeError('odearguments: ode: ode function is not callable')
    else:
        sig = signature(ode)
        if len(sig.parameters) != 2 + len(extras):
            raise TypeError('odearguments: ode: ode function must have the correct number of arguments')
        else:
            result = ode(tspan[0],y0,*extras)
            if not isinstance(result,np.ndarray) and not isinstance(result,list):
                raise TypeError('odearguments: ode: ode function must return a list or ndarray type')
            else:
                if len(result) != len(y0):
                    raise ValueError('odearguments: ode: ode function must return a list or ndarray type of length equal to y0')
    
    odeoptions(options, tspan[0], y0, extras)
    
    htspan = abs(tspan[1]-tspan[0])
    ntspan = len(tspan)
    t0 = tspan[0]
    nex = 2
    tfinal = tspan[-1]
    args = extras
        
    
    if t0 == tfinal:
        raise ValueError('odearguments: tspan: first value and final value must be different') 
    tdir = np.sign(tfinal-t0)
    if any(tdir*np.diff(tspan)<=0):
        raise ValueError('odearguments: tspan: must be monotonic')
    
    f0=feval(ode,t0,y0,extras)
    
    classT0 = (np.array(t0)).dtype
    classY0 = (np.array(y0)).dtype
    classF0 = (np.array(f0)).dtype
    dataType=max(classT0,classY0,classF0)

    
    rtol=1e-3
    if rtol < 100 * np.finfo(dataType).eps:
        rtol = 100 * np.finfo(dataType).eps
        raise Warning('odearguments: rtol: rtol was too small')
    
    atol=odeget(options, 'AbsTol', 1e-6)
    normcontrol = (odeget(options, 'NormControl', 'off') == 'on')
    if normcontrol:
        normy=np.linalg.norm(y0)
    else:
        normy = 0
    
    #TODO Fix threshold 1d or 2d
    
    if isinstance(atol,list):
        threshold = [tol/rtol for tol in atol]
    else:
        threshold=atol/rtol
    
    hmax=max(0.1*abs(tfinal-t0), odeget(options, 'MaxStep', abs(0.1*(tfinal-t0))))
    htry=odeget(options,'InitialStep',0)
    
    odeFcn=ode
    
    
    return neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, args, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType