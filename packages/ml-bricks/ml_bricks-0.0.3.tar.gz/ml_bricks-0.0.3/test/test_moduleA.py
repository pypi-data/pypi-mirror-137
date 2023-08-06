import ml_bricks as mlu
#import ml_bricks.subpackage1.moduleA as moduleA
#import ml_bricks.subpackage2.moduleB as moduleB
import unittest


class TestModuleA(unittest.TestCase): 
    
    def test_fun_a1(self):
        self.assertTrue(mlu.subpackage1.moduleA.fun_a1())
    
    def test_fun_a2(self):
        self.assertTrue(mlu.subpackage1.moduleA.fun_a2())
    
if __name__ == '__main__':
    unittest.main() 


