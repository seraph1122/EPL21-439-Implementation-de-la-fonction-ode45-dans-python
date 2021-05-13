from feval import feval

import numpy as np
import scipy.linalg as lg
import scipy.sparse as sp
import scipy.sparse.linalg as spl


def odemassexplicit(massType,odeFcn,odeArgs,massFcn,massM):
    
    '''Event helper function for ode45.
        
    Parameters
    ----------
    t0 : scalar
        Initial time to be evaluated.
    y0 : array_like, shape(n,)
        Initial values.
    options : dictionary
        Options, see options detail for more information.
    extras : array_like, shape(k,)
        Extra arguments in the function evaluation, if no extra arguments are used then extra is empty. 
        
    Returns
    -------
    haveeventfun : bool
        True if event function contained in options, False otherwise.
    eventFcn : callable || None
        Event function if contained in the options, None otherwise.
    eventArgs : array_like, shape(k,) || None
        extras if event function contained in options, None otherwise.
    eventValue
        Values of the event function for the initial values if event function contained in options,
        None otherwise.
    teout : ndarray, shape(0,)
        Empty numpy array to store events t values.
    yeout : ndarray, shape(0,)
        Empty numpy array to store events y values.
    ieout : ndarray, shape(0,)
        Empty numpy array to store events index values.
    '''
    
    if massType == 1:
        if type(massM)==type(sp.csr_matrix([])):
            superLU = spl.splu(massM)
            odeArgs = np.array([odeFcn, superLU, odeArgs])
            odeFcn = explicitSolverHandleMass1sparse
        else:
            PL, U = lg.lu(massM,permute_l = True)
            odeArgs = np.array([odeFcn, PL, U, odeArgs])
            odeFcn = explicitSolverHandleMass1
    elif massType==2:
        odeArgs = np.array([odeFcn, massFcn, odeArgs])
        odeFcn = explicitSolverHandleMass2
    else:
        odeArgs = np.array([odeFcn, massFcn, odeArgs])
        odeFcn = explicitSolverHandleMass3
    return odeFcn,odeArgs


def explicitSolverHandleMass1sparse(t,y,odeFcn,superLU,varargin):
    
    '''Auxiliary mass function.
        
    Parameters
    ----------
    t : scalar
        Time to be evaluated.
    y : array_like, shape(n,)
        Evaluated values.
    odeFcn : dictionary
        Options, see options detail for more information.
    superLU
    varargin : array_like, shape(k,)
        Extra arguments in the function evaluation, if no extra arguments are used then extra is empty. 
        
    Returns
    -------
    haveeventfun : bool
        True if event function contained in options, False otherwise.
    eventFcn : callable || None
        Event function if contained in the options, None otherwise.
    eventArgs : array_like, shape(k,) || None
        extras if event function contained in options, None otherwise.
    eventValue
        Values of the event function for the initial values if event function contained in options,
        None otherwise.
    teout : ndarray, shape(0,)
        Empty numpy array to store events t values.
    yeout : ndarray, shape(0,)
        Empty numpy array to store events y values.
    ieout : ndarray, shape(0,)
        Empty numpy array to store events index values.
    '''
    
    ode = feval(odeFcn,t,y,varargin)
    yp = superLU.solve(np.array(ode))
    return yp

def explicitSolverHandleMass1(t,y,odeFcn,PL,U,varargin):
    ode = feval(odeFcn,t,y,varargin)
    xp = lg.lstsq(PL,ode)[0]
    yp = lg.lstsq(U,xp)[0]
    return yp

def explicitSolverHandleMass2(t,y,odeFcn,massFcn,varargin):
    mass = feval(massFcn,t,None,varargin)
    ode = feval(odeFcn,t,y,varargin)
    yp = lg.lstsq(mass,ode)[0]
    return yp

def explicitSolverHandleMass3(t,y,odeFcn,massFcn,varargin):
    mass = feval(massFcn,t,y,varargin)
    ode = feval(odeFcn,t,y,varargin)
    yp = lg.lstsq(mass,ode)[0]
    return yp


