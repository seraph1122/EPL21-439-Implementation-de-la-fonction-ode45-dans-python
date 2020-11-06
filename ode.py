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
    output_sol=0 #Temp
    ''' 100 - 110
    TODO : Outputs
    '''
    
    neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, odeArgs, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType = odearg.odearguments(True, solver_name, odefun, tspan, y0, options, varagin)
    nfevals = nfevals + 1
    
    ''' 118 - 144
    TODO : Handle Outputs
    '''
    refine=4 #Temp
    s=np.array(range(1,refine))/refine #Temp
    
    haveEventFcn,eventFcn,eventArgs,valt,teout,yeout,ieout=0,None,None,None,None,None,None #Temp
    
    ''' 146 - 148
    TODO : Handle Event Function
    '''
    
    ''' 150 - 163
    TODO : Handle Mass Function
    '''
    
    nonNegative=0 #Temp
    output_ty=1 #Temp
    
    ''' 167 - 172
    TODO : Non-negative solution
    '''
    
    t=t0
    y=y0
    
    #Memory Allocation
    nout=1
    yout=np.array([],dtype=dataType)
    tout=np.array([],dtype=dataType)
    nargout=2 #TODO
    if nargout > 0:
        if output_sol:
            chunk = min(max(100,50*refine), refine+math.floor(math.pow(2,11)/neq))
            tout = np.zeros((1,chunk),dtype=dataType)
            yout = np.zeros((neq,chunk),dtype=dataType)
            #TODO f3d
        else:
            if ntspan > 2:
              tout = np.zeros((1,ntspan),dtype=dataType)
              yout = np.zeros((neq,ntspan),dtype=dataType)
            else:
              chunk = min(max(100,50*refine), refine+math.floor(math.pow(2,13)/neq))
              tout = np.zeros((1,chunk),dtype=dataType)
              yout = np.zeros((neq,chunk),dtype=dataType)
        nout = 1
        tout[nout-1] = t
        yout[:,nout-1] = y.copy()
    
    
    #Initialize method parameters
    power = 1/5
    A = np.array([1/5, 3/10, 4/5, 8/9, 1, 1])
    B = np.array([[1/5,         3/40,    44/45,   19372/6561,      9017/3168,       35/384    ],
        [0,           9/40,    -56/15,  -25360/2187,     -355/33,         0           ],
        [0,           0,       32/9,    64448/6561,      46732/5247,      500/1113    ],
        [0,           0,       0,       -212/729,        49/176,          125/192     ],
        [0,           0,       0,       0,               -5103/18656,     -2187/6784  ], 
        [0,           0,       0,       0,               0,               11/84       ],
        [0,           0,       0,       0,               0,               0           ]])
    E = np.array([[71/57600], [0], [-71/16695], [71/1920], [-17253/339200], [22/525], [-1/40]])
    f=np.zeros((neq,7),dtype=dataType)
    hmin=16*np.finfo(float(t)).eps
    
    
    if len(htry)==0:
        absh = min(hmax, htspan)
        if normcontrol:
            if len(normy)==0:
                rh=(np.linalg.norm(f0)/ threshold)/ (0.8 * math.pow(rtol,power))
            else:
                rh=(np.linalg.norm(f0)/ max(threshold,max(normy)))/ (0.8 * math.pow(rtol,power))
        else:
            rh=(np.linalg.norm(f0 / max(max(np.abs(y)),threshold),np.inf))/ (0.8 * math.pow(rtol,power))
            
        if (absh * rh) > 1:
            absh =1/rh
        absh = max(absh,hmin)
    else:
        if len(htry)==0:
            absh=min(absh,hmin)
        else:
            absh=min(absh,max(hmin,max(htry)))
    
    f[:,0]=f0
    
    ''' 232 - 236
    TODO : Init ouput function
    '''
    
    ynew=np.zeros(neq)
        
    
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
            nfevals=nfevals+6
            
            
            NNrejectStep = False
            if normcontrol:
                ''' 280 - 289
                TODO : Estimate Error
                '''
            else:
                denom=np.maximum(np.maximum(np.abs(y),np.abs(ynew)),threshold)
                err=absh*np.linalg.norm(np.divide(np.matmul(f,E)[:,0],denom),np.inf)
                ''' 292 - 298
                TODO : Non-negative
                '''

            ''' 305 - 348
            TODO : Failed step
            '''
            NNreset_f7 = False #Temp
                
            break
        nsteps+=1
        
        ''' 351 - 371
        TODO : Event Function
        '''
        
        ''' 375 - 385
        TODO : Failed step
        '''
        
        if output_ty or haveOutputFcn:
            ''' 389 - 392
            TODO : Solver Steps
            '''
            
            #Refinement
            tref=t+(tnew-t)*s
            nout_new=refine
            tout_new=tref.copy()
            tout_new=np.append(tout_new,tnew)
            yout_new=np.transpose(ntrp.ntrp45(tref,t,y,h,f))
            yout_new=np.append(yout_new,np.array([ynew]),axis=0)
            yout_new=np.transpose(yout_new)
            
            ''' 398 - 420
            TODO : Requested Points
            '''
            
            if nout_new > 0:
                if output_ty:
                    oldnout=nout
                    nout=nout+nout_new
                    if nout>len(tout[0]):
                        talloc=np.zeros((1,chunk),dtype=dataType)
                        tout=np.append(tout,talloc)
                        yalloc=np.zeros((neq,chunk),dtype=dataType)
                        yout=np.append(yout,yalloc,axis=0)
                    for i in range(oldnout,nout):
                        tout[0,i] = tout_new[i-oldnout]
                        yout[:,i] = yout_new[:,i-oldnout]
                    
                    ''' 434 - 439
                    TODO : haveOutputFcn
                    '''
        
        if done:
            break
        
        if True:
            temp = 1.25*math.pow((err/rtol),power)
            if temp > 0.2:
                absh=absh/temp
            else:
                absh=0.5*absh
        
                
        
        
            
        t=tnew
        y=ynew.copy()
        f[:,0]=f[:,6]
        
        nsteps+=1
    return OdeResult.OdeResult(solver_name='ode45',odefun=odefun,t=tout[0,0:nout],y=yout[:,0:nout],nsteps=nsteps)
    

    
            
            
            
            
            
            
            
            