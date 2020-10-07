import scipy.integrate as i
import numpy as np


def ode45(odefun,tspan,y0,n):
    t0=tspan[0]
    tend=tspan[1]
    time_span=np.linspace(t0, tend, (tend-t0)*n+1)
    result=np.zeros((len(y0),(tend-t0)*n+1))
    for index in range(len(y0)):
        y=np.zeros((tend-t0)*n+1)
        y[0]=y0[index]
        h=1/n
        size=4
        k=np.zeros(size)
        t=np.zeros(size)

        
        # c=np.array([1/5,            3/10,           4/5,            8/9,            1,              1           ])

        # a=np.array([[1/5,           0,              0,              0,              0,              0           ],
        #             [3/40,          9/40,           0,              0,              0,              0           ],
        #             [44/45,         -56/15,         32/9,           0,              0,              0           ],
        #             [19372/6561,    -25360/2187,    64448/6561,     -212/729,       0,              0           ],
        #             [9017/3168,     -355/33,        46732/5247,     49/176,         -5103/18656,    0           ],
        #             [35/384,        0,              500/1113,       125/192,        -2187/6784,     11/84       ]])

        # e=np.array([5179/57600,0,7571/16695,393/640,92097/339200,187/2100,1/40]) 

        c=np.array([1/2,1/2,1])
        e=np.array([1/6,1/3,1/3,1/6])
        a=np.array([[1/2,0,0],
                    [0,1/2,0],
                    [0,0,1]])

        for i in range(1,(tend-t0)*n+1):
            k[0]=odefun(time_span[i-1],y[i-1])
            for j in range(1,size):
                newy=y[i-1]
                for p in range(j):
                    newy=newy+a[j-1][p]*k[p] #could replace by matrix multiplication
                k[j]=odefun(time_span[i-1]+c[j-1]*h,y[i-1]+h*newy)
            
            y[i]=y[i-1] + h*np.dot(k,e)
        result[index,:]=y
    return result