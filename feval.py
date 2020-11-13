import numpy as np
import sys

def feval(fun,t,y,extra):
    
    
    if extra==[]:
        try:
            result=fun(t,y)
            if len(result)==0:
                result = np.zeros(len(y))
                for i in range(len(y)):
                    result[i]=fun(t,y[i])
        except TypeError:
            result = np.zeros(len(y))
            for i in range(len(y)):
                result[i]=fun(t,y[i])
        except:
            print("Unexpected error:", sys.exc_info()[0])
    else:
        try:
            result=fun(t,y,extra)
            if len(result)==0:
                result = np.zeros(len(y))
                for i in range(len(y)):
                    result[i]=fun(t,y[i],extra)
        except TypeError:
            result = np.zeros(len(y))
            for i in range(len(y)):
                result[i]=fun(t,y[i],extra)
        except:
            print("Unexpected error:", sys.exc_info()[0])
    
    return np.array(result)
    