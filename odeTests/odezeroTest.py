import unittest, os, sys
import numpy as np
import math

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from odezero import odezero
from ntrp45 import ntrp45

class Testodenonnegative(unittest.TestCase):
    
    def setUp(self):
        self.ntrpfun = ntrp45
        
        
        def events(t,y):
            dDSQdt=2*((y[0]-1.2)*(y[2])+(y[1])*(y[3]))
            value = [dDSQdt[0], dDSQdt[0]]
            isterminal = [1,  0]
            direction  = [1, -1]
            return value, isterminal, direction
        
        self.eventfun = events
        self.eventArgs = []
        
    
    def test_odezero_orbit_1(self):
        v = [0,0]
        t = 0
        t0 = 0
        y = np.array([[1.200000000000000],[0],[0],[-1.049357509830320]])
        tnew=0.0001091763007209654
        ynew = np.array([[1.199999989030461],[-0.0001145649700707966],[-0.0002009509097853963],[-1.049357482729883]])
        h = 0.0001091763007209654
        f =np.array([[0,-4.01901829041533e-05,-6.02852742315053e-05,-0.000160760729140163,-0.000178623031642439,-0.000200950909635729,0.000200950909785396],
                      [-1.04935750983032,-1.04935750983032,-1.04935750739128,-1.04935749248604,-1.04935748841763,-1.04935748272988,-1.04935748272988],
                      [-1.84060930067928,-1.84060929560188,-1.84060928896840,-1.84060921740195,-1.84060919786776,-1.84060917055846,-1.84060917055846],
                      [0,9.92905522476813e-05,0.000148935827810288,0.000397162184722919,0.000441291308683021,0.000496452711953234,0.000496452713303303]])
        tout,yout,iout,vnew,stop = odezero(self.ntrpfun,self.eventfun,self.eventArgs,v,t,y,tnew,ynew,t0,h,f,[])
        self.assertAlmostEqual(tout[0],8.673617379884035e-19)
        self.assertAlmostEqual(yout[0,0],1.200000000000000)
        self.assertAlmostEqual(yout[1,0],-9.101725534976095e-19)
        self.assertAlmostEqual(yout[2,0],-1.596474081994797e-18)
        self.assertAlmostEqual(yout[3,0],-1.049357509830320)
        self.assertEqual(iout[0],0)
        self.assertAlmostEqual(vnew[0],2.404392216137085e-04)
        self.assertAlmostEqual(vnew[1],2.404392216137085e-04)
        self.assertEqual(stop,0)
    
    
    def test_odezero_orbit_2(self):
        v = [0.0709660070663352,0.0709660070663352]
        t = 3.073702537116772
        t0 = 0
        y = np.array([[-1.25303745104691],[-0.0278803446539743],[-0.0262613776788988],[1.03790465248548]])
        tnew=3.736828735995603
        ynew = np.array([[-0.970915957541717],[0.552906097367589],[0.805672467818631],[0.545137918406686]])
        h = 0.663126198878830
        f =np.array([[-0.0262613776788988,0.168198588890896,0.264890094027170,0.638153751971133,0.601391638316492,0.666247222075260,0.805672467818631],
                     [1.03790465248548,1.04308703131542,0.997717835448477,0.711268613130676,0.603173441010397,0.491800407103479,0.545137918406686],
                     [1.46623649388740,1.46262747313064,1.41434048184318,1.08418439265122,1.07204869147643,0.956856963247705,0.820779999605265],
                     [0.0390753587982691,-0.282367630907199,-0.445767034868927,-1.14677504219520,-1.15936253595522,-1.32533533895986,-1.46209882892580]])
        tout,yout,iout,vnew,stop = odezero(self.ntrpfun,self.eventfun,self.eventArgs,v,t,y,tnew,ynew,t0,h,f,[])
        self.assertAlmostEqual(tout[0],3.087783972989064)
        self.assertAlmostEqual(yout[0,0],-1.253259311735786)
        self.assertAlmostEqual(yout[1,0],-0.013261032612228)
        self.assertAlmostEqual(yout[2,0],-0.005612072916572)
        self.assertAlmostEqual(yout[3,0],1.038220065006574)
        self.assertEqual(iout[0],1)
        self.assertAlmostEqual(vnew[0],2.404392216137085e-04)
        self.assertAlmostEqual(vnew[1],2.404392216137085e-04)
        self.assertEqual(stop,0)       
        
    
if __name__ == "__main__":
    unittest.main()