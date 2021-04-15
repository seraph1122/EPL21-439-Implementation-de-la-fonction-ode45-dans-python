import os, sys, unittest, math
import numpy as np
from testScript import read_tests

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from ode import ode45

class Testode45(unittest.TestCase):
    
    def test_ode45(self):
        
        results,inputs=read_tests("ode45.txt",True)
        
        for i in range(len(inputs)):
            inp = inputs[i]
            res = results[i]
            
            if inp.fun == 'polyNN':
                self.polyNN(res)
            else:
                print("Function not recognized : "+str(inp.fun))
            
        

    def polyNN(self,result):
        tspan = [-6,5]
        y0=[25,50,25,50]
        opt={'NonNegative':[0,1]}
        
        def f(t,y):
            x=0.02*(3*pow(t,5)-62*pow(t,3)+42*pow(t,2)+45*t+18)
            return [x,x,x,x]
        
        sol = ode45(f,tspan,y0,opt)
        self.compare_ty(result,sol.tout,sol.yout)
        self.compare_stats(result,sol.get_stats())
        plt.plot(sol.tout,sol.yout[0])
        plt.plot(sol.tout,sol.yout[1])
        plt.plot(sol.tout,sol.yout[2])
        plt.plot(sol.tout,sol.yout[3])
        
    
    def compare_ty(self,res,tout,yout):
        
        t = res.tout
        y = res.yout
        
        self.assertEqual(len(t),len(tout))
        self.assertEqual(len(y),len(yout)*len(yout[0]))
        
        for i in range(len(t)):
            for j in range(len(yout)):
                self.assertAlmostEqual(y[j*len(t)+i],yout[j][i])   
            self.assertAlmostEqual(tout[i],t[i])
    
    def compare_stats(self,res,statsvec):
        self.assertEqual(res.nsteps,statsvec[0])
        self.assertEqual(res.nfailed,statsvec[1])
        self.assertEqual(res.nfevals,statsvec[2])
        
if __name__ == "__main__":
    unittest.main()
    