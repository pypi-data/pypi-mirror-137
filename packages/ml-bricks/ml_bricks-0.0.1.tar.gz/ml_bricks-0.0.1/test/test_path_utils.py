import unittest
import os
import ml_bricks as mlu
from ml_bricks.path_utils.path_utils import makedir, get_file_name, delete_file, deletedir, get_files

class TestPathUtils(unittest.TestCase):
    def test_makedir(self):
        direc = './test_dir'
        if os.path.exists(direc):
            deletedir(direc)
        self.assertTrue(makedir(direc))
        self.assertTrue(os.path.exists(direc))
        self.assertFalse(makedir(direc))
        deletedir(direc)
        
    def test_get_file_name(self):
        filepath = './test_dir/test_file.txt'
        self.assertEqual(get_file_name(filepath), 'test_file')
        
    def test_delete_file(self):
        filepath = './test_dir/test_file.txt'
        makedir('./test_dir')
        with open(filepath, 'w') as f:
            f.write('test')
        self.assertTrue(delete_file(filepath))
        self.assertFalse(os.path.exists(filepath))
        self.assertFalse(delete_file(filepath))
        os.rmdir('./test_dir')
        
    def test_deletedir(self):
        direc = './test_dir'
        makedir(direc)
        self.assertTrue(deletedir(direc))
        self.assertFalse(os.path.exists(direc))
        self.assertFalse(deletedir(direc))
    
    def test_get_files(self):
        direc = './test_dir'
        makedir(direc)
        files = [os.path.join(direc, f) for f in os.listdir(direc) if os.path.isfile(os.path.join(direc, f))]
        self.assertEqual(len(files), 0)
        for i in range(10):
            with open(os.path.join(direc, 'test_file_{}.txt'.format(i)), 'w') as f:
                f.write('test')
        files = [os.path.join(direc, f) for f in os.listdir(direc) if os.path.isfile(os.path.join(direc, f))]
        self.assertEqual(len(files), 10)
        files = [os.path.join(direc, f) for f in os.listdir(direc) if os.path.isfile(os.path.join(direc, f)) and os.path.splitext(f)[1] == '.txt']
        self.assertEqual(len(files), 10)
        files = mlu.path_utils.path_utils.get_files(direc, extns=['txt'])
        self.assertEqual(len(files), 10)
        files = mlu.path_utils.path_utils.get_files(direc)
        self.assertEqual(len(files), 10)
        files = mlu.path_utils.path_utils.get_files(direc, extns=['png'])
        self.assertNotEqual(len(files), 10)

        deletedir(direc)



if __name__ == '__main__':
    unittest.main()