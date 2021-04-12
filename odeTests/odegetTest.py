import unittest, os, sys

#Code taken from https://codeolives.com/2020/01/10/python-reference-module-in-parent-directory/
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from odeget import odeget

class Testodeget(unittest.TestCase):
    
    def test_odeget_basic(self):
        options={}
        opt=odeget(options,'Mass',[[1,2],[4,5]])
        self.assertEqual(opt,[[1,2],[4,5]])
        
        
        options={'Refine':4,'AbsTol':1e-3}
        opt=odeget(options,'Mass',[[1,2],[4,5]])
        self.assertEqual(opt,[[1,2],[4,5]])
        
        opt=odeget(options,'Refine',10)
        self.assertEqual(opt,4)

if __name__ == "__main__":
    unittest.main()