import PackageSnippet1 as cv2x
import unittest

class TestCV2X(unittest.TestCase): 
    
    def test_module1_hello(self):
        self.assertTrue(cv2x.subpackage1.moduleA.fun_a())
    
    def test_module2_hello(self):
        self.assertTrue(cv2x.subpackage2.moduleB.fun_b())
    
if __name__ == '__main__':
    unittest.main() 


