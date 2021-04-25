import os, sys, unittest, math
import numpy as np
from testScript import read_tests

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from ode import ode45
import matplotlib.pyplot as plt

class Testode45(unittest.TestCase):
    
    def test_ode45(self):
        
        results,inputs=read_tests("ode45.txt",True)
        
        for i in range(len(inputs)):
            inp = inputs[i]
            res = results[i]
            
            if inp.fun == 'polyNN':
                self.polyNN(res)
                pass
            elif inp.fun == 'ball':
                self.ball(res)
                pass
            elif inp.fun == 'trigbasic':
                self.trigevents(res)
                pass
            elif inp.fun == 'trigbasic2':
                self.trigtol(res)
                pass
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
        
    
    def ball(self,result):
        y0 = [0,20]
        tspan = [0,30]
        
        def f(t,y):
            return [y[1], -9.8]
        
        def events(t,y):
            return [y[0]],[1],[-1]
        
        opt = {'Events':events}
        sol = ode45(f,tspan,y0,opt)
        teout,yeout,ieout=sol.get_events()
        self.compare_ty(result,sol.tout,sol.yout)
        self.compare_stats(result,sol.get_stats())
        self.compare_events(result,teout,yeout,ieout)
            
    
    def trigevents(self,result):
        y0 = [0,-1]
        tspan = [0,30]
        
        def f(t,y):
            return [np.cos(t),np.sin(t)]
        
        def events(t,y):
            return [y[0],y[1],y[0]],[0,0,0],[-1,0,1]
        
        opt = {'Events':events}
        sol = ode45(f,tspan,y0,opt)
        teout,yeout,ieout=sol.get_events()
        self.compare_ty(result,sol.tout,sol.yout)
        self.compare_stats(result,sol.get_stats())
        self.compare_events(result,teout,yeout,ieout)
        
    def trigtol(self,result):
        def f(t,y):
            return [y[0]*np.cos(t),y[1]*np.sin(t)]    

        opt={'RelTol' : 0.0009,'AbsTol' : 3.e-8,'NormControl' : 'on','Refine' : 3,'NonNegative' : [0, 1]}
        
        Tspan = [19, 53]
        Y0 = [6, 38]
        sol=ode45(f,Tspan,Y0,opt)
        self.compare_ty(result,sol.tout,sol.yout)
        self.compare_stats(result,sol.get_stats())
        
    
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
       
        
    def compare_events(self,res,teout,yeout,ieout):
        te=res.teout
        ye=res.yeout
        ie=res.ieout
        
        self.assertEqual(len(te),len(teout))
        self.assertEqual(len(ye),len(yeout)*len(yeout[0]))
        self.assertEqual(len(ie),len(ieout))
        
        for i in range(len(te)):
            for j in range(len(yeout)):
                self.assertAlmostEqual(ye[j*len(te)+i],yeout[j][i])
            self.assertAlmostEqual(teout[i],te[i])
            self.assertEqual(ieout[i],ie[i]-1)
        


if __name__ == "__main__":
    unittest.main()
    