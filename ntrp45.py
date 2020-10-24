import numpy as np

def ntrp45(tinterp,t,y,h,f):
    
    
    BI = np.array([
    [1,       -183/64,      37/12,       -145/128,  ],
    [0,          0,           0,            0,      ],
    [0,       1500/371,    -1000/159,    1000/371,  ],
    [0,       -125/32,       125/12,     -375/64,   ],
    [0,       9477/3392,   -729/106,    25515/6784, ],
    [0,        -11/7,        11/3,        -55/28,   ],
    [0,         3/2,         -4,            5/2,    ]])

    s = (tinterp - t)/h
    yinterp=np.transpose(np.tile(y,(3,1)))+np.matmul(np.matmul(f,h*BI),np.cumprod(np.tile(s,(4,1)),axis=0))
    
    
    return yinterp