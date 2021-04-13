import numpy as np
import os
import sys

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from ode import ode45
import matplotlib.pyplot as plt

def solve_ode(inputs,result):
    #print(inputs.get_options())
    sol=ode45(inputs.fun,inputs.tspan,inputs.y0,inputs.get_options(),inputs.varargin)
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    plt.plot(sol.tout,sol.yout[0])
    plt.plot(sol.tout,sol.yout[1])
    print(result)
    



def get_fun(val):
    if val == 'cosbasic':
        def f(t,y):
            return [np.cos(t),2*np.cos(t)]
    if val == 'trigbasic':
        def f(t,y):
            return [y[0]*np.cos(t),y[1]*np.sin(t)]
    return f

def get_event_fun(val):
    return val

def get_mass_fun(val):
    return val

class Inputs:
    def __init__(self):
        self.fun=None
        self.tspan=None
        self.y0=None
        self.varargin=[]
        self.reltol=None
        self.norm=None
        self.abstol=None
        self.refine=None
        self.stats=None
        self.nonnegative=None
        self.events=None
        self.maxstep=None
        self.initialstep=None
        self.mass=None
        self.massstate=None

    def __str__(self):
        return "Fun : "+str(self.fun)+"\nTspan : "+str(self.tspan)+"\nY0 : "+str(self.y0)+ \
        "\nVarargin : "+str(self.varargin)+"\nRelTol : "+str(self.reltol)+"\nAbsTol : "+str(self.abstol)+ \
        "\nNormControl : "+str(self.norm)+"\nRefine : "+str(self.refine)+"\nStats : "+str(self.stats)+ \
        "\nNonNegative : "+str(self.nonnegative)+"\nEvents : "+str(self.events)+"\nMaxStep : "+str(self.maxstep)+ \
        "\nInitialStep : "+str(self.initialstep)+"\nMass : "+str(self.mass)+"\nMStateDependence : "+str(self.massstate)+ "\n\n"

    def set_fun(self, val):
        self.fun=get_fun(val)
        
    def set_tspan(self, val):
        x = [0] * len(val)
        for i in range(len(val)):
            x[i]=float(val[i])
        self.tspan=x
    
    def set_y0(self, val):
        x = [0] * len(val)
        for i in range(len(val)):
            x[i]=float(val[i])
        self.y0=x
    
    def set_varargin(self, val):
        x = [0] * len(val)
        for i in range(len(val)):
            x[i]=float(val[i])
        self.varargin=x
    
    def set_reltol(self, val):
        self.reltol=float(val)
        
    def set_abstol(self, val):
        if len(val)==1:
            self.abstol=float(val[0])
        else:
            x = [0] * len(val)
            for i in range(len(val)):
                x[i]=float(val[i])
            self.abstol=x
        
    def set_norm(self, val):
        self.norm=val
        
    def set_refine(self, val):
        self.refine=int(val)
        
    def set_stats(self, val):
        self.stats=val
        
    def set_nonnegative(self, val):
        x = [0] * len(val)
        for i in range(len(val)):
            x[i]=int(val[i])-1
        self.nonnegative=x
        
    def set_events(self, val):
        self.events=get_event_fun(val)
        
    def set_maxstep(self, val):
        self.maxstep=float(val)
        
    def set_initialstep(self, val):
        self.initialstep=float(val)
    
    def set_mass_fun(self, val):
        self.mass=get_mass_fun(val)
    
    def set_mass_mat(self, val):
        l = int(np.sqrt(len(val)))
        x = np.zeros((l,l))
        for i in range(l):
            for j in range(l):
                x[i,j]=float(val[i*l + j])
        self.mass=x
    
    def set_massstate(self, val):
        self.massstate=val
    
    
    def get_options(self):
        opt ={}
        
        if self.reltol != None:
            opt["RelTol"] = self.reltol
        if self.abstol != None:
            opt["AbsTol"] = self.abstol
        if self.norm != None:
            opt["NormControl"] = self.norm
        if self.refine != None:
            opt["Refine"] = self.refine
        if self.stats != None:
            opt["Stats"] = self.stats
        if self.nonnegative != None:
            opt["NonNegative"] = self.nonnegative
        if self.events != None:
            opt["Events"] = self.events
        if self.maxstep != None:
            opt["MaxStep"] = self.maxstep
        if self.initialstep != None:
            opt["InitialStep"] = self.initialstep
        if not isinstance(self.mass,type(None)):
            opt["Mass"] = self.mass
        if self.massstate != None:
            opt["MStateDependence"] = self.massstate
        
        return opt

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
    
    def compare(self,tout,yout):
        errt = 0
        erry = 0
        
        t = self.tout
        y = self.yout
        
        print(len(tout))
        print(len(t))
        print("Equal size : " + str(len(t)==len(tout)))
        
        for i in range(t):
            if abs(tout[i]-t[i])>errt:
                errt = abs(tout[i]-t[i])
        
        print("Error t : " + str(errt))
    
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
                if self.yout[j,i]-yout[j,i]>tol:
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
    inputs = []
    for line in f:
        statsvec=[0,0,0]
        result = Results()
        inp = Inputs()
        sp = line.split(" ")
        for word in sp:
            key, values =word.split(":")
            if key == "Function":
                inp.set_fun(values)
            elif key == "Tspan":
                val = values.split("#")
                val.pop()
                inp.set_tspan(val)         
            elif key == "Y0":
                val = values.split("#")
                val.pop()
                inp.set_y0(val) 
            elif key == "Varargin":
                val = values.split("#")
                val.pop()
                if len(val)>1:
                    inp.set_varargin(val)
            elif key == "RelTol":
                if values != '': 
                    inp.set_reltol(values)
            elif key == "AbsTol":
                val = values.split("#")
                val.pop()
                if val[0] != '': 
                    inp.set_abstol(val)
            elif key == "NormControl":
                if values != '': 
                    inp.set_norm(values)
            elif key == "Refine":
                if values != '': 
                    inp.set_refine(values)
            elif key == "Stats":
                if values != '': 
                    inp.set_stats(values)
            elif key == "NonNegative":
                val = values.split("#")
                val.pop()
                if val[0] != '':
                    inp.set_nonnegative(val)
            elif key == "Events":
                if values != '': 
                    inp.set_events(values)
            elif key == "MaxStep":
                if values != '': 
                    inp.set_maxstep(values)
            elif key == "InitialStep":
                if values != '': 
                    inp.set_initialstep(values)
            elif key == "Mass":
                val = values.split("#")
                if len(val) == 1:
                    inp.set_mass_fun(values)
                else:
                    val.pop()
                    if len(val)>1:
                        inp.set_mass_mat(val)
            elif key == "MStateDependence":
                if values != '': 
                    inp.set_massstate(values)
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
        inputs.append(inp)
    return results,inputs
            
        
results,inputs=read_tests("test.txt")
for i in range(len(inputs)):
    solve_ode(inputs[i],results[i])

    