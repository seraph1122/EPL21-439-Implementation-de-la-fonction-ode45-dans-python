import unittest, os, sys
import numpy as np
import math

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from odenonnegative import odenonnegative



class Testodenonnegative(unittest.TestCase):
    
    def setUp(self):
        
        def f_int(t,y,c):
            return -1*t + y + c
        
        def f_vec(t,y,c):
            return [-1*t+c+y[0],-2*t+c]
        
        def f_sin(t,y):
            return math.sin(t)
            
        
        self.f_int = f_int
        self.f_vec = f_vec
        self.f_sin = f_sin
        
        
    def test_odenonnegative_int_basic1(self):
         y = [1,2]
         c = 1 
         t = np.linspace(0,4,num=9)
         threshold = 0.001
         expectedThresh = [0.001,0.001]
         expected = np.array([[2,3],[1.5,2.5],[1,2],[0.5,1.5],[0,1],[0,0.5],[0,0],[0,0],[0,0]])
         idxNonNegative = [0,1]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_int,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),2)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[c])
             self.assertEqual(yp[0],expected[i,0])
             self.assertEqual(yp[1],expected[i,1])
         
            
    def test_odenonnegative_int_basic2(self):
         y = [1,2]
         c = 1 
         t = np.linspace(0,4,num=9)
         threshold = [0.001,0.002]
         expectedThresh = [0.001,0.002]
         expected = np.array([[2,3],[1.5,2.5],[1,2],[0.5,1.5],[0,1],[0,0.5],[0,0],[0,0],[0,0]])
         idxNonNegative = [0,1]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_int,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),2)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[c])
             self.assertEqual(yp[0],expected[i,0])
             self.assertEqual(yp[1],expected[i,1])
    
    
    def test_odenonnegative_int_basic3(self):
         y = [1,2]
         c = 1 
         t = np.linspace(0,4,num=9)
         threshold = 0.001
         expectedThresh = [0.001]
         expected = np.array([[2,3],[1.5,2.5],[1,2],[0.5,1.5],[0,1],[-0.5,0.5],[-1,0],[-1.5,0],[-2,0]])
         idxNonNegative = [1]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_int,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),1)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[c])
             self.assertEqual(yp[0],expected[i,0])
             self.assertEqual(yp[1],expected[i,1])
         
            
    def test_odenonnegative_vec_basic1(self):
         y = [1,2]
         c = 1 
         t = np.linspace(0,4,num=9)
         threshold = 0.001
         expectedThresh = [0.001,0.001]
         expected = np.array([[2,1],[1.5,0],[1,0],[0.5,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
         idxNonNegative = [0,1]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_vec,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),2)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[c])
             self.assertEqual(yp[0],expected[i,0])
             self.assertEqual(yp[1],expected[i,1])
    
    
    def test_odenonnegative_vec_basic2(self):
         y = [1,2]
         c = 1 
         t = np.linspace(0,4,num=9)
         threshold = 0.001
         expectedThresh = [0.001]
         expected = np.array([[2,1],[1.5,0],[1,-1],[0.5,-2],[0,-3],[0,-4],[0,-5],[0,-6],[0,-7]])
         idxNonNegative = [0]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_vec,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),1)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[c])
             self.assertEqual(yp[0],expected[i,0])
             self.assertEqual(yp[1],expected[i,1])
          
            
    def test_odenonnegative_sin_basic1(self):
         y = [0]
         t = np.linspace(0,10,num=500)
         threshold = 0.002
         expectedThresh = [0.002]
         idxNonNegative = [0]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_sin,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),1)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[])
             self.assertGreaterEqual(yp[0],0.0)
         
            
    def test_odenonnegative_sin_basic2(self):
         y = [0,0]
         t = np.linspace(0,10,num=500)
         threshold = 0.002
         expectedThresh = [0.002,0.002]
         idxNonNegative = [0]
         odeFcn,thresholdNonNegative = odenonnegative(self.f_sin,y,threshold,idxNonNegative)
         self.assertEqual(len(thresholdNonNegative),1)
         for i in range(len(idxNonNegative)):
             self.assertEqual(thresholdNonNegative[i],expectedThresh[i])

         for i in range(len(t)):
             yp = odeFcn(t[i],y,[])
             self.assertGreaterEqual(yp[0],0.0)
             self.assertGreaterEqual(yp[1],math.sin(t[i]))
         
        
    
if __name__ == "__main__":
    unittest.main()