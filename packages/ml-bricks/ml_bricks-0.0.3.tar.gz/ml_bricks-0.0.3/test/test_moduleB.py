import ml_bricks as mlu
import unittest


class TestModuleB(unittest.TestCase): 
    
    def test_fun_b(self):
        self.assertTrue(mlu.subpackage2.moduleB.fun_b())
    
if __name__ == '__main__':
    unittest.main() 


