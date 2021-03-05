import numpy as np
import collections
import sys

def feval(fun,t,y,extra,verify=True):
    
    if not verify:
        mainArgs = np.array([t, y])
        extraArgs = np.array(extra)
        allArgs = np.append(mainArgs, extraArgs)
        return fun(*allArgs)
        
    if type(y)==type(None):
        mainArgs = np.array([t])
    else:
        mainArgs = np.array([t, y])
    
    
    
    
    extraArgs = np.array(extra)
    allArgs = np.append(mainArgs, extraArgs)
    
    if not (type(y)==type([]) or type(y)==type(np.array([]))):
        result = fun(*allArgs)
    else:
        try:
            
            #print(result)
            print(allArgs)
            result = fun(*allArgs)
            if not ( type(result)==type([]) or type(result)==type(np.array([]))):
                result = np.zeros(len(y))
                for i in range(len(y)):
                    allArgs[1] = y[i]
                    result[i] = fun(*allArgs)
        except TypeError:
            result = np.zeros(len(y))
            for i in range(len(y)):
                allArgs[1] = y[i]
                result[i] = fun(*allArgs)
        except:
             raise Exception("{}:feval:OtherException".format(sys.exc_info()[0]))
    
    return np.array(result)
      