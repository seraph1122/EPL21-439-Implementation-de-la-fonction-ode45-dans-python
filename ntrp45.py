import numpy as np

def ntrp45(tinterp,t,y,h,f,idxNonNegative):
    
    
    BI = np.array([
    [1,       -183/64,      37/12,       -145/128,  ],
    [0,          0,           0,            0,      ],
    [0,       1500/371,    -1000/159,    1000/371,  ],
    [0,       -125/32,       125/12,     -375/64,   ],
    [0,       9477/3392,   -729/106,    25515/6784, ],
    [0,        -11/7,        11/3,        -55/28,   ],
    [0,         3/2,         -4,            5/2,    ]])

    if type(tinterp)!=type(np.array([])):
        tinterp=np.array([tinterp])
    s = (tinterp - t)/h

    diff=np.matmul(np.matmul(f,h*BI),np.cumprod(np.tile(s,(4,1)),axis=0))
    yinterp=np.transpose(np.tile(y,(len(tinterp),1)))+diff
    
    ncumprod=np.array([np.ones(len(s)),2*s,1.5*s,3*s])
    ypinterp=np.matmul(np.matmul(f,BI),ncumprod)
    if len(idxNonNegative)!=0:
        idx=[(i,j) for i in idxNonNegative for j in range(len(yinterp[0])) if yinterp[i][j]<0]
        if len(idx) != 0:
            for i,j in idx:
                ypinterp[i][j]=0
                yinterp[i][j]=0

    return yinterp, ypinterp