import numpy as np

from feval import feval


def odenonnegative(ode,y0,threshold,idxNonNegative):
    
    if any([True for i in idxNonNegative if i<0 or i>=len(y0)]):
        raise Exception('{}:odenonnegative:NonNegativeIndicesInvalid'.format(idxNonNegative))
    
    if any([True for i in idxNonNegative if y0[i]<0]):
        raise Exception('{}:odenonnegative:NonNegativeInitialValue'.format(idxNonNegative))
    
    if type(threshold)==type([]) or type(threshold)==type(np.array([])):
        thresholdNonNegative = np.array([threshold[i] for i in idxNonNegative])
    else:
        thresholdNonNegative = np.repeat(threshold, len(idxNonNegative))
    
    
    def local_odeFcn_nonnegative(t,y,varargin=[]):
        yp = feval(ode,t,y,varargin)
        ndx = [i for i in idxNonNegative if y[i]<=0]
        print(ndx,y,yp)
        for i in ndx:
            yp[i] = max(yp[i],0)
        print(yp)
        return yp

    odeFcn = local_odeFcn_nonnegative
        
    return odeFcn,thresholdNonNegative

