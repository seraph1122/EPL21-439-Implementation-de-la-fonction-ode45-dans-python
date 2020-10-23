import scipy.integrate as i
import numpy as np
import OdeResult


def ode45(odefun,tspan,y0):
    t_0=tspan[0]
    t_end=tspan[1]
    nsteps=0
    t=np.array([])
    ny0=len(y0)
    #y=np.array(np.array([]) for i in range(len(y0)))
    #y=np.array([[],[]])
    #y=np.full(len(y0),[])
    y=[]
    x=[]
    t=t_0

    #h=1/50
    tdir=t_0

    pow = 1/5
    A = np.array([1/5, 3/10, 4/5, 8/9, 1, 1])
    B = np.array([[1/5,         3/40,    44/45,   19372/6561,      9017/3168,       35/384    ],
        [0,           9/40,    -56/15,  -25360/2187,     -355/33,         0           ],
        [0,           0,       32/9,    64448/6561,      46732/5247,      500/1113    ],
        [0,           0,       0,       -212/729,        49/176,          125/192     ],
        [0,           0,       0,       0,               -5103/18656,     -2187/6784  ], 
        [0,           0,       0,       0,               0,               11/84       ],
        [0,           0,       0,       0,               0,               0           ]])
    E = np.array([71/57600, 0, -71/16695, 71/1920, -17253/339200, 22/525, -1/40])
    f=np.zeros((ny0,7))
    y_cur=y0

    hmin=16*np.finfo(float(t_0)).eps
    hmax=(t_end-t_0)/10
    absh=1 #min(hmin,hmax)
    tdir=0


    f0=np.zeros(ny0)
    
    for iy0 in range(ny0):
        f0[iy0]=odefun(t_0,y0[iy0])
        f[iy0,0]=f0[iy0]
    
    print(f0)

    done=False
    while not done:
        hmin=16*np.finfo(float(t_0)).eps
        absh = min(hmax, max(hmin, absh))
        h = 0.5#tdir * absh

        hA = h * A
        hB = h * B
        for iy0 in range(ny0):
            f[iy0,1]=odefun(tdir+hA[0],y_cur[iy0]+np.dot(f[iy0],hB[:,0]))
            f[iy0,2]=odefun(tdir+hA[1],y_cur[iy0]+np.dot(f[iy0],hB[:,1]))
            f[iy0,3]=odefun(tdir+hA[2],y_cur[iy0]+np.dot(f[iy0],hB[:,2]))
            f[iy0,4]=odefun(tdir+hA[3],y_cur[iy0]+np.dot(f[iy0],hB[:,3]))
            f[iy0,5]=odefun(tdir+hA[4],y_cur[iy0]+np.dot(f[iy0],hB[:,4]))
        ynew = y_cur + np.matmul(f,hB[:,5])
        for iy0 in range(ny0):
            f[iy0,6]=odefun(tdir+hA[5],ynew[iy0])
        
        print(hA)


        tdir+=h
        y_next=y_cur+np.matmul(E,np.transpose(f))
        y_cur=y_next
        y.append(y_next)
        done=True
    print(hmin)
    print(f)
    

    return OdeResult.OdeResult(solver_name='ode45',odefun=odefun,t=x,y=np.array(y),nsteps=nsteps)


#
# ODE45 using the standard Runge Kutta method
# Can handle multiple initial conditions
#
# def ode45(odefun,tspan,y0,n):
#     t0=tspan[0]
#     tend=tspan[1]
#     time_span=np.linspace(t0, tend, (tend-t0)*n+1)
#     result=np.zeros((len(y0),(tend-t0)*n+1))
#     for index in range(len(y0)):
#         y=np.zeros((tend-t0)*n+1)
#         y[0]=y0[index]
#         h=1/n
#         size=7
#         k=np.zeros(size)
#         t=np.zeros(size)

        
#         c=np.array([1/5,            3/10,           4/5,            8/9,            1,              1           ])

#         a=np.array([[1/5,           0,              0,              0,              0,              0           ],
#                     [3/40,          9/40,           0,              0,              0,              0           ],
#                     [44/45,         -56/15,         32/9,           0,              0,              0           ],
#                     [19372/6561,    -25360/2187,    64448/6561,     -212/729,       0,              0           ],
#                     [9017/3168,     -355/33,        46732/5247,     49/176,         -5103/18656,    0           ],
#                     [35/384,        0,              500/1113,       125/192,        -2187/6784,     11/84       ]])

#         e=np.array([5179/57600,0,7571/16695,393/640,92097/339200,187/2100,1/40]) 

#         # c=np.array([1/2,1/2,1])
#         # e=np.array([1/6,1/3,1/3,1/6])
#         # a=np.array([[1/2,0,0],
#         #             [0,1/2,0],
#         #             [0,0,1]])

#         #Main Loop
#         for i in range(1,(tend-t0)*n+1):
#             k[0]=odefun(time_span[i-1],y[i-1])
#             for j in range(1,size):
#                 newy=y[i-1]
#                 for p in range(j):
#                     newy=newy+a[j-1][p]*k[p] #could replace by matrix multiplication
#                 k[j]=odefun(time_span[i-1]+c[j-1]*h,y[i-1]+h*newy)
            
#             y[i]=y[i-1] + h*np.dot(k,e)
#         result[index,:]=y
#     return result