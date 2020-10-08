import matplotlib.pyplot as plt
import numpy as np
import ode45
import math

#Small demo demonstrating the ODE45 function with y(t)'=-2sin(2t)cos(t)
def main():
    rtol=0.001
    tspan=[-10,10]
    n=10
    y0=[-0.78765437911392]
    x=np.linspace(tspan[0],tspan[1],(tspan[1]-tspan[0])*n+1)

    def test(t,y):
        return -1*(2*math.sin(2*t)*math.cos(t))
    
    def expected_fun(x):
        return (4/3)*np.cos(x)*np.cos(x)*np.cos(x)

    expected_vector=expected_fun(x)
    result_vector=ode45.ode45(test,tspan,y0,n)[0]
    plt.plot(x,expected_vector)
    plt.plot(x,result_vector)
        