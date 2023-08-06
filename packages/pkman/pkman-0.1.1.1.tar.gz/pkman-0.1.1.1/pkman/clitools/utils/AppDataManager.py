import os
USER_HOME=os.path.expanduser('~')
class AppDataManager:
    def __init__(self,cache_dirname):
        self.root = os.path.join(USER_HOME, cache_dirname)
        self.tmp_dir=os.path.join(self.root,'tmp')
        self.data_dir=os.path.join(self.root,'data')
        self.init()
    def make_dirs(self,dirs):
        for d in dirs:
            if not os.path.exists(d):
                os.makedirs(d)
    def init(self):
        self.make_dirs([self.root,self.tmp_dir,self.data_dir])
    def tempfile(self,filename):
        return os.path.join(self.tmp_dir,filename)
app_data_manager=AppDataManager('.pkman')

