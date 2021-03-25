import numpy as np

class Results:
    def __init__(self):
        self.tout=np.array([])
        self.yout=np.array([])
        self.nsteps=0
        self.nfailed=0
        self.nfevals=0
        self.teout=np.array([])
        self.yeout=np.array([])
        self.ieout=np.array([])
    
    
    def __str__(self):
        return "NStesps : "+str(self.nsteps)+"\nNFailed : "+str(self.nfailed)+"\nNFevals : "+str(self.nfevals)+ \
        "\nTout : "+str(self.tout)+"\nYout : "+str(self.yout)+"\nTeout : "+str(self.teout)+ \
        "\nYeout : "+str(self.yeout)+"\nIeout : "+str(self.ieout)+"\n\n"
    
    def equal(self, tout,yout,nsteps,nfailed,nfevals,teout,yeout,ieout, tol):
        neq = len(self.yout)
        length = len(self.tout)
        
        if len(self.tout) != len(tout) or len(self.yout) != len(yout)*len(yout[0]):
            return False
        
        if len(self.teout) != len(teout) or len(self.yeout) != len(yeout)*len(yeout[0]) or len(self.ieout) != len(ieout):
            return False
            
        if self.nsteps != nsteps or self.nfailed != nfailed or self.nfevals != nfailed:
            return False
        
        for i in range(length):
            if self.tout[i]-tout[i]>tol:
                return False
            for j in range(neq):
                if self.yout[j,i]-tout[j,i]>tol:
                    return False
        
        return True
    
    
    def set_statvec(self, statsvec):
        self.nsteps=int(statsvec[0])
        self.nfailed=int(statsvec[1])
        self.nfevals=int(statsvec[2])
    
    def set_tout(self, tout):
        x = np.zeros((len(tout),))
        for i in range(len(tout)):
            x[i]=float(tout[i])
        self.tout=x
    
    def set_yout(self, yout):
        x = np.zeros((len(yout),))
        for i in range(len(yout)):
            x[i]=float(yout[i])
        self.yout=x
    
    def set_teout(self, teout):
        x = np.zeros((len(teout),))
        for i in range(len(teout)):
            x[i]=float(teout[i])
        self.teout=x
    
    def set_yeout(self, yeout):
        x = np.zeros((len(yeout),))
        for i in range(len(yeout)):
            x[i]=float(yeout[i])
        self.yeout=x

    def set_ieout(self, ieout):
        x = np.zeros((len(ieout),))
        for i in range(len(ieout)):
            x[i]=int(ieout[i])
        self.ieout=x
        
        
def read_tests(filename):
    f=open(filename,"r")
    results = []
    for line in f:
        statsvec=[0,0,0]        
        result = Results()
        #inputs = Inputs()
        sp = line.split(" ")
        for word in sp:
            key, values =word.split(":")
            if key == "Function":
                pass
            elif key == "Tspan":
                pass
            elif key == "Y0":
                pass
            elif key == "Varargin":
                pass
            elif key == "RelTol":
                pass
            elif key == "AbsTol":
                pass
            elif key == "NormControl":
                pass
            elif key == "Refine":
                pass
            elif key == "Stats":
                pass
            elif key == "NonNegative":
                pass
            elif key == "Events":
                pass
            elif key == "MaxStep":
                pass
            elif key == "InitialStep":
                pass
            elif key == "Mass":
                pass
            elif key == "MStateDependence":
                pass
            elif key == "Tout":
                val = values.split("#")
                val.pop()
                if len(val)>1:
                    result.set_tout(val)
            elif key == "Yout":
                val = values.split("#")
                val.pop()
                if len(val)>1:
                    result.set_yout(val)
            elif key == "Nsteps":
                statsvec[0]=values
            elif key == "Nfailed":
                statsvec[1]=values
            elif key == "Nfevals":
                statsvec[2]=values
            elif key == "Teout":
                val = values.split("#")
                val.pop()
                if len(val)>1:
                    result.set_teout(val)
            elif key == "Yeout":
                val = values.split("#")
                val.pop()
                if len(val)>1:
                    result.set_yeout(val)
            elif key == "Ieout":
                val = values.split("#")
                val.pop()
                if len(val)>1:
                    result.set_ieout(val)
            else:
                print(key)
                raise Exception("Invalid key")
            
        result.set_statvec(statsvec)
        results.append(result)
        print(result)
            
        
        
read_tests("test.txt")
    