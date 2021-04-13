import unittest, os, sys
import numpy as np
import scipy.sparse as sp

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from odearguments import odearguments

class Testodearguments(unittest.TestCase):
    
    def test_odearguments_y0fail(self):
        
        def f(t,y):
            return [t]
            
        tspan = [0,10]
        extra = []
        opt = {}
        
        y = tuple((1,2))
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        y = 1
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        y = [[1,2]]
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        y = ['1','2']
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        y = []
        self.assertRaises(ValueError, odearguments, f, tspan, y, opt, extra)
    
    
    def test_odearguments_tspanfail(self):
        
        def f(t,y):
            return [t, 2*t]
        
        y = [0,10]
        extra = []
        opt = {}
        
        tspan = 1
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        tspan = tuple((1,2))
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        tspan = []
        self.assertRaises(ValueError, odearguments, f, tspan, y, opt, extra)
        tspan = [1]
        self.assertRaises(ValueError, odearguments, f, tspan, y, opt, extra)
        tspan = ['1', 2]
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        tspan = [[1,2],[3,4]]
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        tspan = [1,1]
        self.assertRaises(ValueError, odearguments, f, tspan, y, opt, extra)
        tspan = [1,3,2,4]
        self.assertRaises(ValueError, odearguments, f, tspan, y, opt, extra)
        
    
    def test_odearguments_odefail(self):
        
        tspan = [0,3]
        y = [0,10]
        extra = []
        opt = {}
        
        f = 1
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        
        def f(t):
            return t
        
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        
        def f(t,c):
            return t
        
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, [1])
        
        def f(t,y):
            return t
        
        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, [1])
        
        def f(t,y):
            return t

        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        
        def f(t,y,c):
            return t

        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, [1])
        
        def f(t,y):
            return [t]
        
        self.assertRaises(ValueError, odearguments, f, tspan, y, opt, extra)
        
        def f(t,y):
            return [t, '1']

        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        
        def f(t,y):
            return [t, y]

        self.assertRaises(TypeError, odearguments, f, tspan, y, opt, extra)
        
    
    def test_odearguments_nooptions1(self):
        opt = {}
        tspan = [0,10]
        y = [1,0]
        extra = []
        
        def f(t,y):
            return [np.cos(t),np.sin(t)]
        
        neq, tspan, ntspan, nex, t0, tfinal, tdir, y0, f0, odeArgs, odeFcn, options, threshold, rtol, normcontrol, normy, hmax, htry, htspan, dataType = odearguments(f, tspan, y, opt, extra)
        
        self.assertEqual(neq,2)
        self.assertEqual(tspan,[0,10])
        self.assertEqual(ntspan,2)
        self.assertEqual(nex,2)
        self.assertEqual(t0,0)
        self.assertEqual(tfinal,10)
        self.assertEqual(tdir,1)
        self.assertEqual(y0,[1,0])
        self.assertEqual(f0,[1,0])
        self.assertEqual(odeArgs,[])
        self.assertEqual(odeFcn,f)
        self.assertEqual(options,{})
        self.assertEqual(threshold,1e-3)
        self.assertEqual(rtol,1e-3)
        self.assertEqual(normcontrol,0)
        self.assertEqual(normy,0)
        self.assertEqual(hmax,1)
        self.assertEqual(htry,0)
        self.assertEqual(htspan,10)
        self.assertEqual(dataType,'float64')
        
        
        
if __name__ == "__main__":
    unittest.main()