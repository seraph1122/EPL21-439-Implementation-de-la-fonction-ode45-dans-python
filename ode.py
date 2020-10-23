import scipy.integrate as i
import numpy as np
import OdeResult
import matplotlib.pyplot as plt

def ode45(odefun,tspan,y0):
    t_0=tspan[0]
    t_end=tspan[1]
    nsteps=0
    ny0=len(y0)
    t=t_0
    y=y0
    threshold=np.full(ny0,1^-3)
    
    yout=[]
    tout=[]
    
    yout.append(y)
    tout.append(t)
    
    tdir=1
    ynew=np.zeros(ny0)
    
    
    hmin=16*np.finfo(float(t)).eps
    hmax=(t_end-t_0)/10
    absh=hmax
    
    pow = 1/5
    A = np.array([1/5, 3/10, 4/5, 8/9, 1, 1])
    B = np.array([[1/5,         3/40,    44/45,   19372/6561,      9017/3168,       35/384    ],
        [0,           9/40,    -56/15,  -25360/2187,     -355/33,         0           ],
        [0,           0,       32/9,    64448/6561,      46732/5247,      500/1113    ],
        [0,           0,       0,       -212/729,        49/176,          125/192     ],
        [0,           0,       0,       0,               -5103/18656,     -2187/6784  ], 
        [0,           0,       0,       0,               0,               11/84       ],
        [0,           0,       0,       0,               0,               0           ]])
    E = np.array([[71/57600], [0], [-71/16695], [71/1920], [-17253/339200], [22/525], [-1/40]])
    f=np.zeros((ny0,7))
    
    f0=np.zeros(ny0)
    for iy0 in range(ny0):
        f0[iy0]=odefun(t_0,y0[iy0])
        f[iy0,0]=f0[iy0]
    
    #print(f)
    #f[:,0]=f0
    
    done=False
    while not done:
        hmin = 16*np.finfo(float(t)).eps
        absh = min(hmax, max(hmin, absh))
        h = tdir * absh
        
        if 1.1*absh >= abs(t_end - t):
            h = t_end - t
            absh = abs(h)
            done = True
        
        nofailed=False
        while True:
            hA = h * A
            hB = h * B
    
            for iy0 in range(ny0):
                f[iy0,1]=odefun(t+hA[0],y[iy0]+np.dot(f[iy0],hB[:,0]))
                f[iy0,2]=odefun(t+hA[1],y[iy0]+np.dot(f[iy0],hB[:,1]))
                f[iy0,3]=odefun(t+hA[2],y[iy0]+np.dot(f[iy0],hB[:,2]))
                f[iy0,4]=odefun(t+hA[3],y[iy0]+np.dot(f[iy0],hB[:,3]))
                f[iy0,5]=odefun(t+hA[4],y[iy0]+np.dot(f[iy0],hB[:,4]))
            
            
        
            tnew = t + hA[5]
            if done:
              tnew = t_end
            h = tnew - t 
            
            for iy0 in range(ny0):
                ynew[iy0] = y[iy0] + np.dot(f[iy0],hB[:,5])
            for iy0 in range(ny0):
                f[iy0,6]=odefun(tnew,ynew[iy0])
            

            denom=np.linalg.norm(np.maximum(np.maximum(np.abs(y),np.abs(ynew)),threshold),np.inf)
            err=absh*np.linalg.norm(np.matmul(f,E))/denom
            
            print(err)
            #err = absh * norm((f * E) ./ max(max(abs(y),abs(ynew)),threshold),inf);
            
            break
         
#        if nofailed:
#            temp = 1.25*(err/rtol)^pow
#            if temp > 0.2:
#              absh = absh / temp
#            else:
#              absh = 5.0*absh
        
        t=tnew
        y=ynew.copy()
        yout.append(y)
        tout.append(t)
        f[:,0]=f[:,6]
        
        nsteps+=1
        
    
    
    return OdeResult.OdeResult(solver_name='ode45',odefun=odefun,t=tout,y=np.array(yout),nsteps=nsteps)
    


tspan=[0,5]
y0=[0]        
def test(t,y):
    return 2*t#-2*y + 2*np.cos(t)*np.sin(2*t)

result_vector=ode45(test,tspan,y0)
print(result_vector)
ax1=plt.plot(result_vector.y[:,0])

    
            
            
            
            
            
            
            
            
            
            