import matplotlib.pyplot as plt
import numpy as np
from ode import ode45
import math
import scipy.integrate as i
import odeargument as arg
from feval import feval



def main():
#    fig = plt.gcf()
#    fig.set_size_inches(8, 6)
#    
#    
#    mu = 1.0 / 82.45
#    mustar = 1 - mu
#    y0 = [1.2, 0, 0, -1.04935750983031990726]
#    tspan = [0,7]
#    
#    def events(t,y):
#      dDSQdt = (y[0]-y0[0])*(y[0]-y0[0])+(y[1]-y0[1])*(y[1]-y0[1])
#      value = [dDSQdt, dDSQdt]
#      isterminal = [1,  0]
#      direction  = [1, -1]
#      
#      return value,isterminal,direction
#  
#    def f(t,y):
#      mu = 1.0 / 82.45
#      mustar = 1 - mu
#      r13 = math.pow(((y[0] + mu)*(y[0] + mu) + y[1]*y[1]), 1.5)
#      r23 = math.pow(((y[0] - mustar)*(y[0] - mustar) +  y[1]*y[1]), 1.5)
#      x1=y[2]
#      x2=y[3]
#      x3=2*y[3] + y[0] - mustar*((y[0]+mu)/r13) - mu*((y[0]-mustar)/r23)
#      x4=-2*y[2] + y[1] - mustar*(y[1]/r13) - mu*(y[1]/r23)
#      dydt = [ x1, x2, x3, x4]
#      return dydt
#    
#    options={'Events':events}
#    
#    r=ode45(f,tspan,y0,options)
#    
#    plt.plot(r.y[0],r.y[1])
    
    
    
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    
    
    def dydt(t,y):
        return np.cos(t)
    
    
    
    options={'NonNegative':[0,1]}
    tspan=[0,10]
    y0=[0,0.1]
    r=ode45(dydt,tspan,y0,options)
    print(r.y[0])
    plt.plot(r.t,r.y[0])
    plt.plot(r.t,r.y[1])
#    
    
    
    
#    def events(t,y):
#        value = [y[0]]
#        isterminal = [1]
#        direction = [-1]
#        return [value,isterminal,direction]
#    
#    options={'Events':events}
#
#    tspan=[0,30]
#    tstart=0
#    y0 = [0, 20]
#    
#    def dydt(t,y):
#        return [y[1],-9.8]
#    
#    t=np.array([])
#    y=np.array([])
#    for i in range(10):
#        tspan=[tstart,30]
#        r=ode45(dydt,tspan,y0,options)
#        n=len(r.t)
#        y0[1]=0.9*y0[1]
#        t=np.append(t,r.t)
#        y=np.append(y,r.y[0])
#        tstart=r.t[n-1]
#        
#        
#    print(len(t))
#    plt.plot(t,y)
    #plt.scatter(np.arange(len(t)-1),np.diff(t))
    #plt.yscale('log')
    #plt.ylim(10e-7,1)
    #plt.xlabel('step')
    #plt.ylabel('h size')
    #plt.title('Step size python')

    
    
    #Orbit
#    mu = 1 / 82.45
#    mustar = 1 - mu
#    y0 = [1.2, 0, 0, -1.04935750983031990726]
#    tspan = [0, 7]
#    
#    def f(t,y):
#        mu = 1.0 / 82.45
#        mustar = 1 - mu
#        r13 = math.pow(((y[0] + mu)*(y[0] + mu) + y[1]*y[1]), 1.5)
#        r23 = math.pow(((y[0] - mustar)*(y[0] - mustar) +  y[1]*y[1]), 1.5)
#        x1=y[2]
#        x2=y[3]
#        x3=2*y[3] + y[0] - mustar*((y[0]+mu)/r13) - mu*((y[0]-mustar)/r23)
#        x4=-2*y[2] + y[1] - mustar*(y[1]/r13) - mu*(y[1]/r23)
#        dydt = [ x1, x2, x3, x4]
#        #print(dydt)
#        return dydt
#
#    def events(t,y):
#        #print(t,y)
#        dDSQdt=2*((y[0]-1.2)*(y[2])+(y[1])*(y[3]))
#        value = [dDSQdt, dDSQdt]
#        isterminal = [1,  0]
#        direction  = [1, -1]
#        
#        return value, isterminal, direction
#    
#    options = {'Events':events}
#    
#    
#    res=ode45(f,tspan,y0,options)
#
#    plt.plot(res.y[0],res.y[1])
    
    
    
    
    
    
#    
#    tspan=[0,5]
#    y0=[-5,-4,-3,-2,-1,0,1,2,3,4,5]
#    #y0=[0,1]
#
#    def test(t,y):
#        return -2*y + 2*np.cos(t)*np.sin(2*t)
#    
#    #print(arg.odearguments(True,'ode45',test,tspan,y0,[],[]))
#    sol = i.solve_ivp(test, tspan, y0)
#    fig = plt.gcf()
#    fig.set_size_inches(8, 6)
#    result_vector=ode45(test,tspan,y0)
#    #print(len(result_vector.t))
##    plt.scatter(np.arange(len(result_vector.t)-1),np.diff(result_vector.t),label="ode45")
##    plt.scatter(np.arange(len(sol.t)-1),np.diff(sol.t),label="solve_ivp")
##    ax1=plt.plot(result_vector.t,result_vector.y[0],label="ode45")
##    plt.plot(sol.t,sol.y[0],label="solve_ivp")
#    plt.title("Step size of ode45 with y' = -2y + 2 cos(t) sin(2t), y(0) = -5, -4, ..")
##    plt.xlabel("step")
##    plt.ylabel("h size")
#    #plt.legend()
#    ax1=plt.plot(result_vector.t,result_vector.y[1])
#    ax1=plt.plot(result_vector.t,result_vector.y[2])
#    ax1=plt.plot(result_vector.t,result_vector.y[3])
#    ax1=plt.plot(result_vector.t,result_vector.y[4])
#    ax1=plt.plot(result_vector.t,result_vector.y[5])
#    ax1=plt.plot(result_vector.t,result_vector.y[6])
#    ax1=plt.plot(result_vector.t,result_vector.y[7])
#    ax1=plt.plot(result_vector.t,result_vector.y[8])
#    ax1=plt.plot(result_vector.t,result_vector.y[9])
#    ax1=plt.plot(result_vector.t,result_vector.y[10])
#    plt.title("Solutions of y'' = -2y + 2 cos(t) sin(2t), y(0) = -5,-4,...,4,5")
##    plt.xlabel("t")
##    plt.ylabel("y")
    

main()