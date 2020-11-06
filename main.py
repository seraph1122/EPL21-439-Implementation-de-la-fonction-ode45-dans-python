import matplotlib.pyplot as plt
import numpy as np
from ode import ode45
import math
import scipy.integrate as i
import odeargument as arg


#Look at the style of code for scipy
#Look at solve_ivp and ode45 at the actual code and understand the code


#Small demo demonstrating the ODE45 function with y(t)'=-2sin(2t)cos(t)
def main():
    tspan=[0,5]
    y0=[-5,-4,-3,-2,-1,0,1,2,3,4,5]
    #y0=[0,1]

    def test(t,y):
        return -2*y + 2*np.cos(t)*np.sin(2*t)
    
    #print(arg.odearguments(True,'ode45',test,tspan,y0,[],[]))
    sol = i.solve_ivp(test, tspan, y0)
    fig = plt.gcf()
    fig.set_size_inches(8, 6)
    result_vector=ode45(test,tspan,y0)
    #print(len(result_vector.t))
#    plt.scatter(np.arange(len(result_vector.t)-1),np.diff(result_vector.t),label="ode45")
#    plt.scatter(np.arange(len(sol.t)-1),np.diff(sol.t),label="solve_ivp")
#    ax1=plt.plot(result_vector.t,result_vector.y[0],label="ode45")
#    plt.plot(sol.t,sol.y[0],label="solve_ivp")
    plt.title("Step size of ode45 with y' = -2y + 2 cos(t) sin(2t), y(0) = -5, -4, ..")
#    plt.xlabel("step")
#    plt.ylabel("h size")
    #plt.legend()
    ax1=plt.plot(result_vector.t,result_vector.y[1])
    ax1=plt.plot(result_vector.t,result_vector.y[2])
    ax1=plt.plot(result_vector.t,result_vector.y[3])
    ax1=plt.plot(result_vector.t,result_vector.y[4])
    ax1=plt.plot(result_vector.t,result_vector.y[5])
    ax1=plt.plot(result_vector.t,result_vector.y[6])
    ax1=plt.plot(result_vector.t,result_vector.y[7])
    ax1=plt.plot(result_vector.t,result_vector.y[8])
    ax1=plt.plot(result_vector.t,result_vector.y[9])
    ax1=plt.plot(result_vector.t,result_vector.y[10])
    plt.title("Solutions of y'' = -2y + 2 cos(t) sin(2t), y(0) = -5,-4,...,4,5")
#    plt.xlabel("t")
#    plt.ylabel("y")
    

main()        