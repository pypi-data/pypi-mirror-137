import os
def is_empty_dir(path):
    if os.listdir(path):
        return False
    return True