
#options is a dictionary
def odeget(options,name,default):
    
    o=None
    
    Names = ['AbsTol',
            'Events',
            'InitialStep',
            'JConstant',
            'Mass',
            'MaxStep',
            'NonNegative', 
            'NormControl',
            'OutputFcn',
            'OutputSel',
            'Refine',
            'RelTol',
            'Stats',
            'MStateDependence']
    
    if name not in Names:
        raise Exception('{}:odeoptions:OptionNameInvalid'.format(name))
    
    if name in options:
        if type(options.get(name))!=type(default) and default!=None:
            raise Exception('{}:odeoptions:OptionValueInvalidType'.format(name))
        else:
            o=options.get(name)
    else:
        o=default
        
    
    return o
