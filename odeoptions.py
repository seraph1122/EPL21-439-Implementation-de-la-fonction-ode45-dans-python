import numpy as np
import numbers as num
from inspect import signature



def odeoptions(options, t, y, varargin):
    
    if type(options) != type({}):
        raise Exception('{}:odeoptions:OptionsNotDictionary'.format(options))
        
    
    for (key,value) in options.items():
        
        if key == 'RelTol' or key == 'InitialStep' or key == 'MaxStep':
            if isinstance(value,num.Number):
                if value < 0:
                    raise ValueError("odeoptions: " + str(key) + ": int/float must be positive")            
            else:
                raise TypeError('odeoptions: ' + str(key) + ': must be a positive int/float')

        
        
        elif key == 'AbsTol':
            if isinstance(value,num.Number):
                if value < 0:
                    raise ValueError('odeoptions: AbsTol: int/float must be positive')
            elif isinstance(value,list) or isinstance(value,np.ndarray):
                if len(value) != len(y):
                    raise IndexError('odeoptions: AbsTol: list/ndarray must have the length as y0')
                else:
                    for i in value:
                        if isinstance(i,float) or isinstance(i,int):
                            if i < 0:
                                raise ValueError('odeoptions: AbsTol: list/ndarray must have all elements be positive')
                        else:
                            raise TypeError('odeoptions: AbsTol: list/ndarray must be have all elements be positive int/float')
            else:
                raise TypeError('odeoptions: AbsTol: must a int/float or list of int/float')
          
            
        elif key == 'NormControl' or key == 'Stats':
            if value != 'on' and value != 'off':
                raise ValueError('odeoptions: ' + str(key) + ': must either be \'on\' or \'off\'')
        
        
        elif key == 'NonNegative':
            if isinstance(value,list) or isinstance(value,np.ndarray):
                for i in value:
                    if isinstance(i,int):
                        if i >= len(y) or i < 0:
                            raise IndexError('odeoptions: NonNegative: elements must be index of y')
                    else:
                        raise TypeError('odeoptions: NonNegative: list/ndarray must only contain int')
            else:
                raise TypeError('odeoptions: NonNegative: must be a list/ndarray')
                
                
        elif key == 'Refine':
            if isinstance(value,int):
                if value < 1:
                    raise ValueError('odeoptions: Refine: must be a positive integer')
            else:
                raise TypeError('odeoptions: Refine: must be a postive integer')
                    
                
        elif key == 'Events':
            if not callable(value):
                raise TypeError('odeoptions: Events: must be a function')
            else:
                vnew,isterminal,direction = value(t,y,*varargin)
                if (isinstance(vnew,np.ndarray) or isinstance(value,list)) and (isinstance(isterminal,np.ndarray) or isinstance(isterminal,list)) and (isinstance(direction,np.ndarray) or isinstance(direction,list)):
                    raise ValueError('odeoptions: Event: must output vnew,isterminal,direction of type list or ndarray')
                else:
                    if len(vnew) != len(y) or len(isterminal) != len(y) or len(direction) != len(y):
                        raise ValueError('odeoptions: Event: must output vnew,isterminal,direction with same length as y')
                    for i in range(len(y)):
                        if not isinstance(vnew[i],float) and not isinstance(vnew[i],int):
                            raise ValueError('odeoptions: Event: vnew must be int/float')
                        if isterminal[i] != 1 and isterminal[i] != 0:
                            raise ValueError('odeoptions: Event: isterminal must be either 1 or 0')
                        if direction[i] != 1 and direction[i] != 0 and direction[i] != -1:
                            raise ValueError('odeoptions: Event: direction must be either 0, 1 or -1')
                
        
        
        elif key == 'Mass':
            if not callable(value):
                if isinstance(value,np.ndarray) or isinstance(value,list):
                    if len(value) != len(y):
                        raise ValueError('odeoptions: Mass: matrix must be a square matrix with size same as length of y')
                    for i in value:
                        if len(i) != len(y):
                            raise ValueError('odeoptions: Mass: matrix must be a square matrix with with size same as length of y')
                else:
                    raise ValueError('odeoptions: Mass: matrix or function must be a square matrix with size same as length of y of type list/ndarray')
            else:
                sig = signature(value)
                if len(sig.parameters) == 2 + len(varargin):
                    mass = value(t,y,*varargin)
                    if isinstance(mass,np.ndarray) or isinstance(mass,list):
                        if len(mass) != len(y):
                            raise ValueError('odeoptions: Mass: function must return a square matrix with size same as length of y')
                        for i in mass:
                            if len(i) != len(y):
                                raise ValueError('odeoptions: Mass: function must return a square matrix with with size same as length of y')
                    else:
                        raise ValueError('odeoptions: Mass: function must return a square matrix of type list/ndarray')
                elif len(sig.parameters) == 1 + len(varargin):
                    mass = value(t,*varargin)
                    if isinstance(mass,np.ndarray) or isinstance(mass,list):
                        if len(mass) != len(y):
                            raise ValueError('odeoptions: Mass: function must return a square matrix with size same as length of y')
                        for i in mass:
                            if len(i) != len(y):
                                raise ValueError('odeoptions: Mass: function must return a square matrix with with size same as length of y')
                    else:
                        raise ValueError('odeoptions: Mass: function must return a square matrix of type list/ndarray')

                else:
                    raise Exception('odeoptions: Mass: function must either be time dependent of state/time dependent')
                    
        
        elif key == 'MStateDependence':
            if value != 'none' and value != 'weak':
                raise ValueError('odeoptions: MStateDependence: must either be \'none\' or \'weak\'')
        
        elif key == 'OutputFcn':
            pass #TODO
        
        elif key == 'OutputSel':
            pass #TODO
                
            
        else:
            raise TypeError('odeoptions: ' + str(key) + ' is not a supported option')
        
        