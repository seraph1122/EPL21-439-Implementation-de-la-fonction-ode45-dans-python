import numpy as np
import collections
import sys

def feval(fun,t,y,extra):
    
    mainArgs = np.array([t,y])
    extraArgs = np.array(extra)
    allArgs = np.append(mainArgs, extraArgs)
    
    if not isinstance(y,collections.Sequence):
        result = fun(*allArgs)
    else:
        try:
            result = fun(*allArgs)
            print(result)
            if not ( isinstance(result,collections.Sequence) or type(result)==type(np.array([]))):
                raise Exception('{}:feval:FunctionResultType'.format(fun))
        except TypeError:
            result = np.zeros(len(y))
            for i in range(len(y)):
                allArgs[1] = y[i]
                result[i] = fun(*allArgs)
        except:
             raise Exception("{}:feval:OtherException".format(sys.exc_info()[0]))
    
    return np.array(result)
    
    
#    if extra==[]:
#        try:
#            result=fun(t,y)
#            if len(result)==0:
#                result = np.zeros(len(y))
#                for i in range(len(y)):
#                    result[i]=fun(t,y[i])
#        except TypeError:
#            result = np.zeros(len(y))
#            for i in range(len(y)):
#                result[i]=fun(t,y[i])
#        except:
#            print("Unexpected error:", sys.exc_info()[0])
#    else:
#        try:
#            result=fun(t,y,extra)
#            if len(result)==0:
#                result = np.zeros(len(y))
#                for i in range(len(y)):
#                    result[i]=fun(t,y[i],extra)
#        except TypeError:
#            result = np.zeros(len(y))
#            for i in range(len(y)):
#                result[i]=fun(t,y[i],extra)
#        except:
#            print("Unexpected error:", sys.exc_info()[0])
#    
#    return np.array(result)
#    