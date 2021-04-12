

def feval(fun,t,y,extra):
    
    if isinstance(y,type(None)):
        try:
            result = fun(t,*extra)
        except:
            raise Exception("ode45: feval: FunctionError")
        return result
    else:
        try:
            result = fun(t,y,*extra)
        except:
            raise Exception("ode45: feval: FunctionError")
        return result