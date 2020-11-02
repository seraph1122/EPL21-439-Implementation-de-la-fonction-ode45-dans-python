import numpy as np
import OdeResult
import ntrp45 as ntrp
import odeargument as odearg
import itertools
import math

def ode45(odefun,tspan,y0,options=[],varagin=[]):
    
    solver_name='ode45'
    
    ''' 79 - 91
    TODO : Check inputs
    '''
    
    #Stats
    nsteps=0
    nfailed = 0
    nfevals = 0
  
    #Outputs
    FcnHandlesUsed=callable(odefun)
    ''' 100 - 110
    TODO : Outputs
    '''
    
    neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, odeArgs, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType = odearg.odearguments(True, solver_name, odefun, tspan, y0, options, varagin)
    nfevals = nfevals + 1
    
    ''' 118 - 144
    TODO : Handle Outputs
    '''
    
    haveEventFcn,eventFcn,eventArgs,valt,teout,yeout,ieout=0,None,None,None,None,None,None #Temp
    
    ''' 146 - 148
    TODO : Handle Event Function
    '''
    
    ''' 150 - 163
    TODO : Handle Mass Function
    '''
    
    nonNegative=0 #Temp
    
    ''' 167 - 172
    TODO : Non-negative solution
    '''
    
    
    
    t=t0
    y=y0
    
    yout=[]
    tout=[]
    error=[0]
    output_ty=1
    
    yout.append(y)
    tout.append(t)
    
    ynew=np.zeros(neq)
    
    refine=4
    s=np.array(range(1,refine))/refine
    
    hmin=16*np.finfo(float(t)).eps
    absh=hmax
    
    nout=1
    
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
    f=np.zeros((neq,7))
    
    for iy0 in range(neq):
        f[iy0,0]=f0[iy0]
    
    
    done=False
    while not done:
        hmin = 16*np.finfo(float(t)).eps
        absh = min(hmax, max(hmin, absh))
        h = tdir * absh
        
        if 1.1*absh >= abs(tfinal - t):
            h = tfinal - t
            absh = abs(h)
            done = True
        
        nofailed=False
        while True:
            hA = h * A
            hB = h * B
            
            
            for iy0 in range(neq):
                f[iy0,1]=odefun(t+hA[0],y[iy0]+np.dot(f[iy0],hB[:,0]))
                f[iy0,2]=odefun(t+hA[1],y[iy0]+np.dot(f[iy0],hB[:,1]))
                f[iy0,3]=odefun(t+hA[2],y[iy0]+np.dot(f[iy0],hB[:,2]))
                f[iy0,4]=odefun(t+hA[3],y[iy0]+np.dot(f[iy0],hB[:,3]))
                f[iy0,5]=odefun(t+hA[4],y[iy0]+np.dot(f[iy0],hB[:,4]))
            
            
        
            tnew = t + hA[5]
            if done:
              tnew = tfinal
            h = tnew - t 
            
            for iy0 in range(neq):
                ynew[iy0] = y[iy0] + np.dot(f[iy0],hB[:,5])
            for iy0 in range(neq):
                f[iy0,6]=odefun(tnew,ynew[iy0])
            

            denom=np.linalg.norm(np.maximum(np.maximum(np.abs(y),np.abs(ynew)),threshold),np.inf)
            err=absh*np.linalg.norm(np.matmul(f,E))/denom
            error.append(err)
            
            h = tdir * absh
            break
        
        #Refinement
        tref=t+(tnew-t)*s
        
        nout_new=refine
        tout_new=tref.copy()
        tout_new=np.append(tout_new,tnew)
        yout_new=np.transpose(ntrp.ntrp45(tref,t,y,h,f))
        
        
        while nex <= ntspan:
            if tdir * (tnew - tspan[nex-1]) < 0:
                break
            nout_new = nout_new + 1
            
            np.append(tout_new,tspan[nex-1])
            #not done
            nex = nex + 1
        
        
#        if nout_new > 0:
#            if output_ty:
#                oldnout = nout
#                nout = nout + nout_new
#                for i in range(oldnout,nout):
#                    tout[i] = tout_new[i-oldnout]
#                    yout[:,i] = yout_new[i-oldnout]
        
        
        if True:
            temp = math.pow(1.25*(err/rtol),pow)
            if temp > 0.2:
                absh=absh/temp
            else:
                absh=0.5*absh
            
        
#        if nofailed
#            % Note that absh may shrink by 0.8, and that err may be 0.
#            temp = 1.25*(err/rtol)^pow;
#            if temp > 0.2
#              absh = absh / temp;
#            else
#              absh = 5.0*absh;
#            end
#          end
                
        
        if done:
            break
            
        t=tnew
        y=ynew.copy()
        for i in yout_new:
            yout.append(i)
        for i in tout_new:
            tout.append(i)
        yout.append(y)
        f[:,0]=f[:,6]
        
        nsteps+=1
    
    return OdeResult.OdeResult(solver_name='ode45',odefun=odefun,t=tout,y=np.array(yout),err=error,nsteps=nsteps)
    

    
            
            
            
            
            
            
            
            