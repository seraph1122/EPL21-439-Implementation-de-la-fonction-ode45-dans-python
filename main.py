import matplotlib.pyplot as plt
import numpy as np
import ode as ode
import math
import scipy.integrate as i
import odeargument as arg


#Look at the style of code for scipy
#Look at solve_ivp and ode45 at the actual code and understand the code


#Small demo demonstrating the ODE45 function with y(t)'=-2sin(2t)cos(t)
def main():
    tspan=[0,5]
    #y0=[-5,-4,-3,-2,-1,0,1,2,3,4,5]
    y0=[0,1]

    def test(t,y):
        return -2*y + 2*np.cos(t)*np.sin(2*t)
    
    #print(arg.odearguments(True,'ode45',test,tspan,y0,[],[]))
    
    fig = plt.gcf()
    fig.set_size_inches(10, 6)
    result_vector=ode.ode45(test,tspan,y0)
    ax1=plt.plot(result_vector.t,result_vector.y[:,0])
    ax1=plt.plot(result_vector.t,result_vector.y[:,1])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,2])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,3])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,4])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,5])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,6])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,7])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,8])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,9])
#    ax1=plt.plot(result_vector.t,result_vector.y[:,10])
    plt.title("Solutions of y'' = -2y + 2 cos(t) sin(2t), y(0) = -5,-4,...,4,5")
    plt.xlabel("t")
    plt.ylabel("y")
    
    print(len(result_vector.t))


main()        