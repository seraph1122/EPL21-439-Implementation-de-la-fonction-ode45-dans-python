import numpy as np

def feval(fun,t,y,extra):
    
    if isinstance(y,type(None)):
        try:
            result = fun(t,*extra)
        except:
            raise Exception("ode45: feval: FunctionError")
        return result
    else:
        try:
            if isinstance(y,np.ndarray):
                if y.ndim != 1:
                    y = np.squeeze(y)
            result = fun(t,y,*extra)
        except:
            raise Exception("ode45: feval: FunctionError")
        return result