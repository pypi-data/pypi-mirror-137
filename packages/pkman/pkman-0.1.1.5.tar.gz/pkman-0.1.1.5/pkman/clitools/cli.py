import os
import shutil
import sys
from .utils import CmdUtil,IoUtil,SetupUtil
from .config import PACKAGE_CONFIG_FILENAME
from .package import Package
os.environ['ANSI_COLORS_DISABLED']="1"
import fire
from . import apis

def load_pkg_info():
    pkg_info = IoUtil.json_load(os.path.join(os.getcwd(), PACKAGE_CONFIG_FILENAME))
    return pkg_info

class CLI:
    def hi(cls):
        print('Hi, welcome to use pkman !'.center(50, '*'))
    @classmethod
    def upgradeself(cls):
        CmdUtil.run_command([sys.executable,'-m','pip','install','-U','-i','https://pypi.org/simple','pkman'])
    @classmethod
    def us(cls):
        return cls.upgradeself()
    @classmethod
    def cmd(cls, *args, **kwargs):
        CmdUtil.run_command(sys.argv[2:])
    @classmethod
    def build(cls):
        '''build a python package in current directory'''
        info=load_pkg_info()
        assert info
        for d in ["dist","build","%s.egg-info"%(info['name'])]:
            if os.path.exists(d):
                shutil.rmtree(d)
        SetupUtil.setup_package(**info,cmd=['sdist','bdist_wheel'])
    @classmethod
    def config(cls):
        pass
    @classmethod
    def docs(cls):
        pass
    @classmethod
    def init(cls):
        apis.init()
    @classmethod
    def gitsetup(cls,branch):
        Package(os.getcwd()).gitsetup(branch)
    @classmethod
    def install(cls):
        Package(os.getcwd()).install_packages_in_dist()
    @classmethod
    def instd(cls):
        Package(os.getcwd()).install_dependencies()
    @classmethod
    def list(cls):
        pass
    @classmethod
    def ls(cls):
        pass
    @classmethod
    def login(cls):
        pass
    @classmethod
    def logout(cls):
        pass
    @classmethod
    def publish(cls):
        cls.build()
        CmdUtil.run_command([sys.executable,'-m','twine',"upload","dist/*"])
        apis.up_version(os.getcwd())

    @classmethod
    def run(cls,cmd):
        pkg_info=load_pkg_info()
        scripts=pkg_info['scripts']
        if cmd in scripts:
            CmdUtil.run_command([scripts[cmd]])
        else:
            raise Exception('Command not found: %s'%(cmd))
    @classmethod
    def search(cls):
        pass
    @classmethod
    def uninstall(cls):
        pass
    @classmethod
    def unpublish(cls):
        pass
    @classmethod
    def update(cls):
        pass
    @classmethod
    def upgit(cls,msg="update somthing"):
        CmdUtil.run_multiple_commands(["git add .",'git commit -m "%s"'%(msg),"git push"])
    @classmethod
    def version(cls):
        pkg_info=load_pkg_info()
        print(pkg_info['version'])
    @classmethod
    def test(cls):
        return cls.run('test')


    @classmethod
    def testsysargv(cls, *args, **kwargs):
        import sys
        print("sys.argv:", sys.argv)
        print("executable:", sys.executable)

def main():
    fire.Fire(CLI())

if __name__ == '__main__':
    main()