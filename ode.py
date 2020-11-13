import numpy as np
from OdeResult import OdeResult
from ntrp45 import ntrp45
from odeargument import odearguments
from odeget import odeget
from odeevents import odeevents
from feval import feval
from odezero import odezero
import itertools
import math

def ode45(odefun,tspan,y0,options=None,varargin=[]):
    
    solver_name='ode45'
    
    ''' 79 - 91
    TODO : Check inputs
    '''
    
    if options==None:
        options={}
    
    if type(options)!=type({}):
        raise Exception('{}:ode45:OptionsNotDictionary'.format(solver_name))
    
    
    
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
    
    neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, odeArgs, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType = odearguments(True, solver_name, odefun, tspan, y0, options, varargin)
    nfevals = nfevals + 1
    
    ''' 118 - 144
    TODO : Handle Outputs
    '''
    
    refine=max(1,odeget(options,'Refine',4))
    s=np.array(range(1,refine))/refine #Temp
    
    haveEventFcn,eventFcn,eventArgs,valt,teout,yeout,ieout=odeevents(FcnHandlesUsed,odeFcn,t0,y0,options,varargin)
    
    ''' 146 - 148
    TODO : Handle Event Function
    '''
    
    ''' 150 - 163
    TODO : Handle Mass Function
    '''
    
    nonNegative=0 #Temp
    output_ty=1 #Temp
    idxNonNegative=False #temp
    
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
        if normcontrol: #TODO
            if len(normy)==0:
                rh=(np.linalg.norm(f0)/ threshold)/ (0.8 * math.pow(rtol,power))
            else:
                rh=(np.linalg.norm(f0)/ max(threshold,max(normy)))/ (0.8 * math.pow(rtol,power))
        else:
            rh=np.linalg.norm(f0 / np.maximum(np.abs(y),np.repeat(threshold,len(y))),np.inf) / (0.8 * math.pow(rtol,power))
            
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
            f[:,1]=feval(odefun,t+hA[0],y+np.matmul(f,hB[:,0]),varargin)
            f[:,2]=feval(odefun,t+hA[1],y+np.matmul(f,hB[:,1]),varargin)
            f[:,3]=feval(odefun,t+hA[2],y+np.matmul(f,hB[:,2]),varargin)
            f[:,4]=feval(odefun,t+hA[3],y+np.matmul(f,hB[:,3]),varargin)
            f[:,5]=feval(odefun,t+hA[4],y+np.matmul(f,hB[:,4]),varargin)

            
            
            tnew = t + hA[5]
            if done:
              tnew = tfinal
            h = tnew - t 
            
            
            ynew=y+np.matmul(f,hB[:,5])
            f[:,6]=feval(odefun,tnew,ynew,varargin)
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
        
        if haveEventFcn:
            te,ye,ie,valt,stop=odezero(ntrp45,eventFcn,eventArgs,valt,t,y,tnew,ynew,t0,h,f,idxNonNegative)
            
        
#        if haveEventFcn
#            [te,ye,ie,valt,stop] = ...
#                odezero(@ntrp45,eventFcn,eventArgs,valt,t,y,tnew,ynew,t0,h,f,idxNonNegative);
#            if ~isempty(te)
#              if output_sol || (nargout > 2)
#                teout = [teout, te];
#                yeout = [yeout, ye];
#                ieout = [ieout, ie];
#              end
#              if stop               % Stop on a terminal event.               
#                % Adjust the interpolation data to [t te(end)].   
#                
#                % Update the derivatives using the interpolating polynomial.
#                taux = t + (te(end) - t)*A;        
#                [~,f(:,2:7)] = ntrp45(taux,t,y,[],[],h,f,idxNonNegative);        
#                
#                tnew = te(end);
#                ynew = ye(:,end);
#                h = tnew - t;
#                done = true;
#              end
#            end
#          end
        
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
            yout_new=np.transpose(ntrp45(tref,t,y,h,f))
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
    return OdeResult(solver_name='ode45',odefun=odefun,t=tout[0,0:nout],y=yout[:,0:nout],nsteps=nsteps)
    

    
            
            
            
            
            
            
            
            