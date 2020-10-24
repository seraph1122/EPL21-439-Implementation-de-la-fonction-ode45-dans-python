import numpy as np

class OdeResult:
    """
    Parameters
    ----------
    solver_name : string
        Name of the solver used.
    odefun : callable
        Function which was integrated.
    t : array like
        Points at which the function was evaluated.
    y : array like
        Evaluation of the function at point t.
    err : array like
        Error at certain intervals
    nsteps : int
        Number of steps
    """
    def __init__(self,solver_name='ode45',odefun=None,t=np.array([]),y=np.array([]),err=np.array([]),nsteps=0):
        self.solver_name=solver_name
        self.odefun=odefun
        self.t=t
        self.y=y
        self.err=err
        self.nsteps=nsteps
    
    def __str__(self):
        string=" Method : "+self.solver_name+"\n Function : "+str(self.odefun)+"\n t : "+str(self.t)+"\n y : "+str(self.y)+"\n err : "+str(self.err)+"\n nsteps : "+str(self.nsteps)
        return string