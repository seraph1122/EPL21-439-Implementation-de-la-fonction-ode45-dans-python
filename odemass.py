from odeget import odeget
from feval import feval

import numpy as np
import scipy.sparse as sp


def odemass(ode,t0,y0,options,extras):
    massType = 0
    massFcn = None
    massM = sp.eye(len(y0),format="csr")
    massArgs = None
    
    Moption = odeget(options,'Mass',None)
    if isinstance(Moption,type(None)):
        return massType, massM, massFcn
    elif not callable(Moption):
        massType = 1
        massM = Moption
        return massType, massM, massFcn
    else:
        massFcn = Moption
        massArgs = extras
        Mstdep = odeget(options,'MStateDependence','weak')
        if Mstdep == 'none':
            massType = 2
        elif Mstdep == 'weak':
            massType = 3
        else:
            raise Exception('{}:odemass:MStateDependenceMassType'.format(Mstdep))
            
        if massType > 2:
            massM = feval(massFcn,t0,y0,massArgs);
        else:
            massM = feval(massFcn,t0,None,massArgs);
    
    return massType, massM, massFcn
