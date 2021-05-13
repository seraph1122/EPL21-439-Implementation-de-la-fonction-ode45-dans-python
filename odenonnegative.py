from feval import feval


def odenonnegative(ode,y0,threshold,idxNonNegative):
    
    if any([True for i in idxNonNegative if i<0 or i>=len(y0)]):
        raise IndexError('odenonnegative: idxNonNegative: index outside of scope')
    
    if any([True for i in idxNonNegative if y0[i]<0]):
        raise ValueError('odenonnegative: y0: initial values were negative')
    
    if isinstance(threshold,list):
        thresholdNonNegative = [threshold[i] for i in idxNonNegative]
    else:
        thresholdNonNegative = [threshold] * len(idxNonNegative)
    
    
    def local_odeFcn_nonnegative(t,y,*varargin):
        yp = feval(ode,t,y,varargin)
        ndx = [i for i in idxNonNegative if y[i]<=0]
        for i in ndx:
            yp[i] = max(yp[i],0)
        return yp

    odeFcn = local_odeFcn_nonnegative
        
    return odeFcn,thresholdNonNegative

