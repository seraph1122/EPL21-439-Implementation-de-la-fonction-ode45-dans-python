import numpy as np
from OdeResult import OdeResult
from ntrp45 import ntrp45
from odeargument import odearguments
from odeget import odeget
from odeevents import odeevents
from feval import feval
from odezero import odezero
from odemass import odemass
from odemassexplicit import odemassexplicit
from odenonnegative import odenonnegative
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
    dataType='float64'
    
    ''' 118 - 144
    TODO : Handle Outputs
    '''
    haveOutputFcn =1#Temp
    
    refine=max(1,odeget(options,'Refine',4))
    s=np.array(range(1,refine))/refine #Temp
    
    haveEventFcn,eventFcn,eventArgs,valt,teout,yeout,ieout=odeevents(FcnHandlesUsed,odeFcn,t0,y0,options,varargin)
    
    ''' 146 - 148
    TODO : Handle Event Function
    '''
    
    
    
    Mtype, M, Mfun =  odemass(odeFcn,t0,y0,options,varargin)
    print(Mtype,M,Mfun)
    if Mtype > 0:
        odeFcn,odeArgs = odemassexplicit(Mtype,odeFcn,odeArgs,Mfun,M)
        print(odeArgs)
        f0 = feval(odeFcn,t0,y0,odeArgs)
        nfevals = nfevals + 1;
    
    nonNegative=0 #Temp
    output_ty=1 #Temp
    
    idxNonNegative = odeget(options,'NonNegative',[])
    if len(idxNonNegative) != 0:
        odeFcn,thresholdNonNegative = odenonnegative(odeFcn,y0,threshold,idxNonNegative);
        f0 = feval(odeFcn,t0,y0,odeArgs)
        nfevals = nfevals + 1
    
    
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
    A = np.array([1./5., 3./10., 4./5., 8./9., 1., 1.],dtype='float64')
    B = np.array([[1./5.,         3./40.,    44./45.,   19372./6561.,      9017./3168.,       35./384.    ],
                [0.,           9./40.,    -56./15.,  -25360./2187.,     -355./33.,         0.           ],
                [0.,           0.,       32./9.,    64448./6561.,      46732./5247.,      500./1113.    ],
                [0.,           0.,       0.,       -212./729.,        49./176.,          125./192.     ],
                [0.,           0.,       0.,       0.,               -5103./18656.,     -2187./6784.  ], 
                [0.,           0.,       0.,       0.,               0.,               11./84.       ],
                [0.,           0.,       0.,       0.,               0.,               0.           ]],dtype='float64')
    
    
    E = np.array([[71./57600.], [0.], [-71./16695.], [71./1920.], [-17253./339200.], [22./525.], [-1./40.]],dtype='float64')
    f=np.zeros((neq,7),dtype='float64')#,dtype=dataType)
    hmin=16*np.finfo(float(t)).eps
    np.set_printoptions(precision=16)    
    
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
    
    #print(absh)
    
    ''' 232 - 236
    TODO : Init ouput function
    '''
    
    ynew=np.zeros(neq,dtype='float64')
        
    
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
            #print(varargin)
            f[:,1]=feval(odeFcn,t+hA[0],y+np.matmul(f,hB[:,0]),odeArgs)
            f[:,2]=feval(odeFcn,t+hA[1],y+np.matmul(f,hB[:,1]),odeArgs)
            f[:,3]=feval(odeFcn,t+hA[2],y+np.matmul(f,hB[:,2]),odeArgs)
            f[:,4]=feval(odeFcn,t+hA[3],y+np.matmul(f,hB[:,3]),odeArgs)
            f[:,5]=feval(odeFcn,t+hA[4],y+np.matmul(f,hB[:,4]),odeArgs)

            #print(odeFcn)
            #print(f)
            
            tnew = t + hA[5]
            if done:
              tnew = tfinal
            h = tnew - t 
            
            
            ynew=y+np.matmul(f,hB[:,5])
            f[:,6]=feval(odeFcn,tnew,ynew,odeArgs)
            nfevals=nfevals+6
            
#            print(h)
            #print(f)
            
            NNrejectStep = False
            if normcontrol:
                ''' 280 - 289
                TODO : Estimate Error
                '''
                err=0
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
            
            te,ye,ie,valt,stop=odezero([],eventFcn,eventArgs,valt,t,np.transpose(np.array([y])),tnew,ynew,t0,h,f,idxNonNegative)
            
            if len(te)!=0:
                if True: #Temp
                    teout=np.append(teout,te)
                    if len(yeout)==0:
                        yeout=ye
                    else:
                        yeout=np.append(yeout,ye,axis=0)
                    ieout=np.append(ieout,ie) #ieout is 2d
                if stop:
                    taux = t + (te[-1] - t)*A
                    discard,f[:,1:7]=ntrp45(taux,t,np.transpose(np.array([y])),h,f,idxNonNegative)
                    tnew = te[-1]
                    ynew = ye[:,-1]
                    h = tnew - t
                    done = True
                    
        
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
            #print(y)
            #y=np.transpose(np.array([y]))
            #print(y)
            yout_new,discard=ntrp45(tref,t,np.transpose(np.array([y])),h,f,idxNonNegative) #Fix y orientation
            yout_new=np.transpose(yout_new)
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
                absh=5.0*absh
                
        
        
            
        t=tnew
        y=ynew.copy()
        f[:,0]=f[:,6]
        
        nsteps+=1
    return OdeResult(solver_name='ode45',odefun=odeFcn,t=tout[0,0:nout],y=yout[:,0:nout],nsteps=nsteps)
    

    
            
            
            
            
            
            
            
            