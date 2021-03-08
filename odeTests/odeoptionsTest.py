import unittest, os, sys
import numpy as np
import scipy.sparse as sp

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from odeoptions import odeoptions

class Testodeoptions(unittest.TestCase):
    
    def test_odeoptions_nooptions(self):
        options = {}
        y = [1, 2]
        t = 1
        try:
            odeoptions(options, t, y, [])
        except:
            self.fail("No option correct test failed")
    
    def test_odeoptions_reltol(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'RelTol':1e-2}
            odeoptions(options, t, y, extra)
            options = {'RelTol':100}
            odeoptions(options, t, y, extra)
            options = {'RelTol':0}
            odeoptions(options, t, y, extra)
        except:
            self.fail("RelTol option correct test failed")
        
        options = {'RelTol':-1e-2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'RelTol':'1'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'RelTol':[1, 1.2]}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)

    
    def test_odeoptions_abstol(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'AbsTol':1e-2}
            odeoptions(options, t, y, extra)
            options = {'AbsTol':100}
            odeoptions(options, t, y, extra)
            options = {'AbsTol':0}
            odeoptions(options, t, y, extra)
            options = {'AbsTol':[0, 1]}
            odeoptions(options, t, y, extra)
            options = {'AbsTol':[0, 1.0]}
            odeoptions(options, t, y, extra)
        except:
            self.fail("AbsTol option correct test failed")
        
        options = {'AbsTol':-1e-2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'AbsTol':'1'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'AbsTol':[1, 1.2, 3]}
        self.assertRaises(IndexError, odeoptions, options, t, y, extra)
        options = {'AbsTol':[-1, 1.2]}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'AbsTol':['1', 1.2]}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
    
    
    def test_odeoptions_normcontrol(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'NormControl':'on'}
            odeoptions(options, t, y, extra)
            options = {'NormControl':'off'}
            odeoptions(options, t, y, extra)
        except:
            self.fail("NormControl option correct test failed")
        
        options = {'NormControl':2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'NormControl':'none'}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
  

    def test_odeoptions_stats(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'Stats':'on'}
            odeoptions(options, t, y, extra)
            options = {'Stats':'off'}
            odeoptions(options, t, y, extra)
        except:
            self.fail("Stats option correct test failed")
        
        options = {'Stats':2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'Stats':'none'}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)      

    
    def test_odeoptions_nonnegative(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'NonNegative':[]}
            odeoptions(options, t, y, extra)
            options = {'NonNegative':[1]}
            odeoptions(options, t, y, extra)
            options = {'NonNegative':[0, 1]}
            odeoptions(options, t, y, extra)
        except:
            self.fail("NonNegative option correct test failed")
        
        options = {'NonNegative':[2]}
        self.assertRaises(IndexError, odeoptions, options, t, y, extra)
        options = {'NonNegative':[0, '2']}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'NonNegative':[1.0]}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'NonNegative':'one'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
       
        
    def test_odeoptions_refine(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'Refine':1}
            odeoptions(options, t, y, extra)
            options = {'Refine':5}
            odeoptions(options, t, y, extra)
        except:
            self.fail("Refine option correct test failed")
        
        options = {'Refine':1e-2}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'Refine':-2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'Refine':0}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)


    def test_odeoptions_initialstep(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'InitialStep':1}
            odeoptions(options, t, y, extra)
            options = {'InitialStep':5e-2}
            odeoptions(options, t, y, extra)
        except:
            self.fail("InitialStep option correct test failed")
        
        options = {'InitialStep':-1e-2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'InitialStep':-1}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'InitialStep':[1.0]}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'InitialStep':'on'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        
        
    def test_odeoptions_maxstep(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'MaxStep':1}
            odeoptions(options, t, y, extra)
            options = {'MaxStep':5e-2}
            odeoptions(options, t, y, extra)
        except:
            self.fail("MaxStep option correct test failed")
        
        options = {'MaxStep':-1e-2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'MaxStep':-1}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'MaxStep':[1.0]}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'MaxStep':'on'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
    
    def test_odeoptions_events(self):
        y = [1, 2]
        t = 0
        
        try:
            extra = []
            def events(t, y):
                return [[3.2, 2.1],[1, 0],[-1, 1]] 
            options = {'Events':events}
            odeoptions(options, t, y, extra)
            
            extra = [1, [3, 2]]
            def events(t, y, c, b):
                return [[3.2, 2.1],[1, 0],[-1, 1]]
            options = {'Events':events}
            odeoptions(options, t, y, extra)
            
            y = np.array([1, 2])
            extra = np.array([[3, 2]])
            def events(t, y, c):
                print(c[0])
                print(type(c[0]))
                return [[3.2, c[0]],[1, 0],[-1, 1]]
            options = {'Events':events}
            odeoptions(options, t, y, extra)

        except:
            self.fail("Events option correct test failed")
        
        extra = []
        options = {'Events':[[3.2, 2.1],[1, 0],[-1, 1]] }
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'Events':'on'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, 2.1, 3],[1, 0],[-1, 1]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, 2.1],[1, 0, 1],[-1, 1]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, 2.1],[1, 0],[-1, 1, 0]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, '2.1'],[1, 0],[-1, 1]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, '2.1'],[1, 0],[-1, 1]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, 2.1],[-1, 0],[0, 1]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        
        def events(t, y):
             return [[3.2, 2.1],[1, 0],[0, 2]]
        options = {'Events':events}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
    
    
    def test_odeoptions_maxstep(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'MaxStep':1}
            odeoptions(options, t, y, extra)
            options = {'MaxStep':5e-2}
            odeoptions(options, t, y, extra)
        except:
            self.fail("MaxStep option correct test failed")
        
        options = {'MaxStep':-1e-2}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'MaxStep':-1}
        self.assertRaises(ValueError, odeoptions, options, t, y, extra)
        options = {'MaxStep':[1.0]}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        options = {'MaxStep':'on'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
    
    
    def test_odeoptions_mass(self):
        y = [1, 2]
        t = 0
        extra = []
        try:
            options = {'Mass':[[1,1],[0,2]]}
            odeoptions(options, t, y, extra)
            
            def mass(t):
                return [[t, 0],[0, t+1]]
            options = {'Mass':mass}
            odeoptions(options, t, y, extra)
            
            def mass(t,c):
                return np.array([[t, 0],[c, t+1]])
            options = {'Mass':mass}
            odeoptions(options, t, y, [0])
            
            def mass(t,y):
                return np.array([[t, y[0]],[0, t+1]])
            options = {'Mass':mass}
            odeoptions(options, t, y, extra)
            
            def mass(t,y,c):
                return [[t, y[0]],[c, t+1]]
            options = {'Mass':mass}
            odeoptions(options, t, y, [1])
            
            
        except:
            self.fail("Mass option correct test failed")
        
        options = {'Mass':'on'}
        self.assertRaises(TypeError, odeoptions, options, t, y, extra)
        
    
    def test_odeoptions_alloptions(self):
        def events(t,y):
            return [[1,1],[1,1],[1,1]]
        
        options = {'RelTol':1e-2,
            'AbsTol':1e-3,
            'Events':events}
        #Stats
        #OutputFcn
        #OutputSel
#            'NormControl':'on',
#            'Refine',
#            'MaxStep',
#            'InitialStep',
#            'NonNegative',      
#            'Events',  
#            'Mass':[],
#            'MStateDependence'}
        
        y = [1, 2]
        t = 0
        odeoptions(options, t, y, [])
        
if __name__ == "__main__":
    unittest.main()