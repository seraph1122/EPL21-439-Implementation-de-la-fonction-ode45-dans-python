import matplotlib.pyplot as plt
import numpy as np
import ode as ode45
import math
import scipy.integrate as i


#Look at the style of code for scipy
#Look at solve_ivp and ode45 at the actual code and understand the code


#Small demo demonstrating the ODE45 function with y(t)'=-2sin(2t)cos(t)
def main():
    tspan=[0,5]
    #n=10
    #y0=[-0.78765437911392,1]
    y0=[0]
    #x=np.linspace(tspan[0],tspan[1],(tspan[1]-tspan[0])*n+1)

    # def test(t,y):
    #     return -1*(2*np.sin(2*t)*np.cos(t))
    
    # def expected_fun(x):
    #     return (4/3)*np.cos(x)*np.cos(x)*np.cos(x)
    # y0=[0.8390715290764524]

    # def test(t,y):
    #     return np.sin(t)
    
    def test(t,y):
        return np.cos(x)

    def expected_fun(x):
        return -1*np.cos(x)

    #print(i.solve_ivp(test,[0,10],[0]))

    #expected_vector=expected_fun(x)

    result_vector=ode45.ode45(test,tspan,y0)
    #print(result_vector)
    #ax1=plt.plot(result_vector.y[:,0])

    #ax2=plt.plot(result_vector.y[:,1])
    # test_vector=test(x,0)
    # plt.title("y(t)'=sin(t)")
    # ax1=plt.plot(x,expected_vector,label='y(t)\'')
    # ax2=plt.plot(x,result_vector,label='y(t)')
    # plt.legend()
    # plt.show()
    #plt.legend()

main()        