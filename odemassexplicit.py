from odeget import odeget
from feval import feval

import numpy as np
import scipy.linalg as lg
import scipy.sparse as sp
import scipy.sparse.linalg as spl


def odemassexplicit(massType,odeFcn,odeArgs,massFcn,massM):
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


