
def odeget(options, name, default):
    
    '''Helper function to retreive the value of an option.
        
    Parameters
    ----------
    options : dictionary
        Dictionary containing the options of the ode45 execution in the form {'name':value,...}.
    name : string
        Name of the option to retreive.
    default : variable
        If name is not in the dictionary, this is the value which will be returned.
        
    Returns
    -------
    opt : variable
        If name is in options then opt is the value in the dictionary, otherwise opt is default.
    '''
    
    opt = default
    
    if name in options:
        opt=options.get(name)
        
    return opt
