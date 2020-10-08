import unittest
import ode45 as o
import numpy as np
import utils as u
import math

#Series to the test the basic functionalities of the ODE45 function

class TestBasic(unittest.TestCase):    

    def setUp(self):
        self.rtol=0.01
        self.tspan=[-10,10]
        self.n=10
        self.x_span=np.linspace(self.tspan[0],self.tspan[1],(self.tspan[1]-self.tspan[0])*self.n+1)

    #Test the function y(t)'=1
    def test_constant(self):
        y0=[-10]

        def test(t,y):
            return 1
        
        def expected_fun(x):
            return x
        
        expected_vector=expected_fun(self.x_span)
        result_vector=o.ode45(test,self.tspan,y0,self.n)[0]
        self.assertTrue(u.assertVectorEqual(expected_vector,result_vector,self.rtol))

    #Test the function y(t)'=2t+1
    def test_linear(self):
        y0=[90]

        def test(t,y):
            return 2*t+1
        
        def expected_fun(x):
            return x*x+x
        
        expected_vector=expected_fun(self.x_span)
        result_vector=o.ode45(test,self.tspan,y0,self.n)[0]
        self.assertTrue(u.assertVectorEqual(expected_vector,result_vector,self.rtol))

    #Test the function y(t)'=3t^2+t+2
    def test_square(self):
        y0=[-970]

        def test(t,y):
            return 3*t*t+t+2
        
        def expected_fun(x):
            return x*x*x+0.5*x*x+2*x
        
        expected_vector=expected_fun(self.x_span)
        result_vector=o.ode45(test,self.tspan,y0,self.n)[0]
        self.assertTrue(u.assertVectorEqual(expected_vector,result_vector,self.rtol))
    
    #Test the function y(t)'=sin(t)
    def test_sin(self):
        y0=[0.8390715290764524]

        def test(t,y):
            return np.sin(t)
        
        def expected_fun(x):
            return -1*np.cos(x)
        
        expected_vector=expected_fun(self.x_span)
        result_vector=o.ode45(test,self.tspan,y0,self.n)[0]
        self.assertTrue(u.assertVectorEqual(expected_vector,result_vector,self.rtol))
    
    #Test the function y(t)'=-2sin(2t)cos(t)
    def test_trig(self):
        y0=[-0.7876543791139244]

        def test(t,y):
            return -1*(2*math.sin(2*t)*math.cos(t))
    
        def expected_fun(x):
            return (4/3)*np.cos(x)*np.cos(x)*np.cos(x)

        expected_vector=expected_fun(self.x_span)
        result_vector=o.ode45(test,self.tspan,y0,self.n)[0]
        self.assertTrue(u.assertVectorEqual(expected_vector,result_vector,self.rtol))

if __name__ == "__main__":
    unittest.main()
