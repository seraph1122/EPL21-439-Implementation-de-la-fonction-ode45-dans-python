
#options is a dictionary
def odeget(options,name,default):
    
    opt = default
    
    if name in options:
        opt=options.get(name)
        
    return opt
