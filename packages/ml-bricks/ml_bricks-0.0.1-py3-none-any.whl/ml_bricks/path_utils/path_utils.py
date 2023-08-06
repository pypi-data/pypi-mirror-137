import os
import shutil
print('path-utils loaded')

def makedir(direc):
    if not os.path.exists(direc):
        os.makedirs(direc)
        return True
    else:
        return False

def get_file_name(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def get_files(direc, extns=None):
    ''' Returns a list of files in a directory.
    If extns is not None, only files with those extensions will be returned.
    '''
    files = os.listdir(direc)
    if extns is not None:
        files = [f for f in files if f.split('.')[-1] in extns]
    return files
    
def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    else:
        return False    

def deletedir(direc):
    if os.path.exists(direc):
        shutil.rmtree(direc)
        return True
    else:
        return False


if __name__=='__main__': # pragma: no cover
    # Driver code:
    direc = './test_dir'
    makedir(direc)
    print(os.path.exists(direc))

    