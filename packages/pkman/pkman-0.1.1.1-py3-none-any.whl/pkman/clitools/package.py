import os
import sys
import pkg_resources
from pkg_resources import DistributionNotFound, VersionConflict

from .utils import CmdUtil,IoUtil,StringUtil,PathUtil,FireUtil
from .config import PACKAGE_CONFIG_FILENAME,PACKAGE_CONFIG_FILENAME_YML

class Package:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.plugins=[]
        self.add_plugins([
            ShellCommandRunner(),
            PkxCommandRunner(),
            QuickCommandRunner(),
            EntryFileRunner(),
            FireFileRunner(),
            PkmanCommandRunner(),
        ])
    def add_plugins(self,plugins):
        self.plugins.extend(plugins)
    def join_path(self, path):
        return os.path.join(self.path,path)
    def load_pkg_info(self):
        config_path = self.join_path(PACKAGE_CONFIG_FILENAME)
        config_path_yml = self.join_path(PACKAGE_CONFIG_FILENAME_YML)
        if os.path.exists(config_path):
            return IoUtil.json_load(config_path)
        elif os.path.exists(config_path_yml):
            return IoUtil.yaml_load(config_path_yml)
        else:
            return None
    def cmd_in_path(self,command):
        return CmdUtil.run_multiple_commands([command],cwd=self.path)
    def install_dependencies(self):
        cfg = self.load_pkg_info()
        if cfg:
            dependencies = cfg['dependencies']
            try:
                pkg_resources.require(dependencies)
            except DistributionNotFound:
                for pkg in dependencies:
                    self.cmd_in_path([sys.executable,'-m','pip','install',pkg])
            except VersionConflict:
                raise VersionConflict
    def run(self, args):
        for plugin in self.plugins:
            res=plugin.use(self,args)
            if plugin.should_stop:
                return res
    def error(self,msg):
        raise Exception('Error: %s'%(msg))
    def no_config_file_error(self):
        self.error('No config file found.')
    def gitsetup(self,branch):
        cfg=self.load_pkg_info()
        if cfg is None:
            self.no_config_file_error()
        else:
            IoUtil.write_txt("\n".join([
                ".idea",'.vscode',".code",".node_modules","local","build","dist",cfg['name']+".egg-info"
            ]),self.join_path('.gitignore'))
            self.cmd_in_path('pkx gitops init %s %s' % (cfg['repository']['url'], branch))
class Plugin:
    def __init__(self):
        self.should_stop=False
    def use(self,pkg:Package,args):
        pass
class EntryFileRunner(Plugin):
    def use(self,pkg:Package,args):
        path = pkg.path
        entry_filepath = os.path.join(path, 'entry.py')
        if os.path.exists(entry_filepath):
            self.should_stop=True
            return CmdUtil.run_file(entry_filepath, args)
        self.should_stop=False
class FireFileRunner(Plugin):
    def use(self,pkg:Package,args):
        path = pkg.path
        fire_filepath = os.path.join(path, 'firex.py')
        if os.path.exists(fire_filepath):
            self.should_stop=True
            return CmdUtil.run_file(fire_filepath, args,fire=True)
        self.should_stop=False
class QuickCommandRunner(Plugin):
    def use(self,pkg:Package,args):
        if len(args)==1 and (args[0] in ['ls','dir']):
            self.should_stop = True
            if os.name=='nt':
                return pkg.cmd_in_path('dir')
            else:
                return pkg.cmd_in_path('ls')
        else:
            self.should_stop=False
class PkmanCommandRunner(Plugin):
    def use(self,pkg:Package,args):
        path = pkg.path
        self.should_stop = True
        return CmdUtil.run_command(['pkman', *args],cwd=path)

class PkxCommandRunner(Plugin):
    def use(self,pkg:Package,args):
        path = pkg.path
        if len(args)>=1 and args[0]=='-x':
            self.should_stop = True
            return CmdUtil.run_command(['pkx', *args[1:]],cwd=path)
        else:
            self.should_stop=False

class ShellCommandRunner(Plugin):
    def use(self,pkg:Package,args):
        path = pkg.path
        if len(args)>=1 and args[0]=='-cmd':
            self.should_stop = True
            return CmdUtil.run_command([*args[1:]],cwd=path)
        else:
            self.should_stop=False

