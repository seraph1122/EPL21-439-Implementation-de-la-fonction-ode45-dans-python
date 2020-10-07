import unittest
import ode45 as o
import numpy as np
import utils as u
import math


class TestBasic(unittest.TestCase):    

    def setUp(self):
        self.rtol=0.01
        self.tspan=[-10,10]
        self.n=10
        self.x_span=np.linspace(self.tspan[0],self.tspan[1],(self.tspan[1]-self.tspan[0])*self.n+1)

    def test_constant(self):
        y0=[-10,-5,0,5,10]
        c=[0,5,10,15,20]

        def test(t,y):
            return 1
        
        def expected_fun(x,c):
            return x+c
        
        
        result_vector=o.ode45(test,self.tspan,y0,self.n)
        for i in range(len(c)):
            expected_vector=expected_fun(self.x_span,c[i])
            self.assertTrue(u.assertVectorEqual(expected_vector,result_vector[i],self.rtol))

    
    def test_sin(self):
        y0=[0.8390715290764524-1,0.8390715290764524,1.8390715290764524]
        c=[-1,0,1]

        def test(t,y):
            return np.sin(t)
        
        def expected_fun(x,c):
            return -1*np.cos(x)+c
        
        result_vector=o.ode45(test,self.tspan,y0,self.n)
        for i in range(len(c)):
            expected_vector=expected_fun(self.x_span,c[i])
            self.assertTrue(u.assertVectorEqual(expected_vector,result_vector[i],self.rtol))
    
    def test_trig(self):
        y0=[-1.7876543791139244,-0.7876543791139244,1-0.7876543791139244]
        c=[-1,0,1]

        def test(t,y):
            return -1*(2*math.sin(2*t)*math.cos(t))
    
        def expected_fun(x,c):
            return (4/3)*np.cos(x)*np.cos(x)*np.cos(x)+c

        result_vector=o.ode45(test,self.tspan,y0,self.n)
        for i in range(len(c)):
            expected_vector=expected_fun(self.x_span,c[i])
            self.assertTrue(u.assertVectorEqual(expected_vector,result_vector[i],self.rtol))

if __name__ == "__main__":
    unittest.main()
