import scipy.integrate as i
import numpy as np
import OdeResult
import matplotlib.pyplot as plt
import ntrp45 as ntrp

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
    error=[0]
    
    yout.append(y)
    tout.append(t)
    
    tdir=1
    ynew=np.zeros(ny0)
    
    refine=4
    s=np.array(range(1,refine))/refine
    
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
            error.append(err)
            
                        
            break
        
        #Refinement
        tref=t+(tnew-t)*s
        
        nout_new=refine
        tout_new=tref.copy()
        tout_new=np.append(tout_new,tnew)
        yout_new=np.transpose(ntrp.ntrp45(tref,t,y,h,f))
        
        
        t=tnew
        y=ynew.copy()
        for i in yout_new:
            yout.append(i)
        for i in tout_new:
            tout.append(i)
        yout.append(y)
        #tout.append(t)
        f[:,0]=f[:,6]
        
        nsteps+=1
    
    return OdeResult.OdeResult(solver_name='ode45',odefun=odefun,t=tout,y=np.array(yout),err=error,nsteps=nsteps)
    

    
            
            
            
            
            
            
            
            