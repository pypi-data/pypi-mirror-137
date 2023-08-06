import subprocess
import sys
import os
from .AppDataManager import AppDataManager
from . import StringUtil,IoUtil,PathUtil,FireUtil
app_data_manager=AppDataManager('.pkman/tmp_code')

def run_command(args,check=False,cwd='.'):
    cmd=" ".join(args) if isinstance(args,(list,tuple)) else args
    if check:
        return subprocess.check_call(cmd, shell=True,cwd=cwd)
    else:
        return subprocess.call(cmd, shell=True,cwd=cwd)
def run_multiple_commands(args_list,check=False,cwd='.'):
    if os.name=='nt':
        return run_command(" & ".join([" ".join(args) if isinstance(args ,list) else args for args in args_list]),check=check,cwd=cwd)
    else:
        return run_command(" && ".join([" ".join(args) if isinstance(args ,list) else args for args in args_list]),check=check,cwd=cwd)
def run_batch_code(code):
    filename=StringUtil.hash_text(code)[:10]+'.bat'
    file_path=app_data_manager.tempfile(filename)
    IoUtil.write_txt(code,file_path)
    res=os.system(file_path)
    os.remove(file_path)
    return res
def run_python_script(path, args, extend_path=None):
    if extend_path is None:
        extend_path = []
    cmd=[sys.executable,path,*args]
    if extend_path:
        if os.name == 'nt':
            code = 'set PYTHONPATH=%s' % (';'.join(extend_path)) + ' & ' + ' '.join(cmd)
            return run_command([code])
        else:
            code='export PYTHONPATH=%s'%(':'.join(extend_path))+' && '+ ' '.join(cmd)
            return run_command([code])
    else:
        return run_command(cmd)
def gen_fire_argv(*args, **kwargs):
    argv = []
    for arg in args:
        argv.append(str(arg))
    for k, v in kwargs.items():
        argv.append('--%s=%s' % (k, v))
    return argv


def run_file(path, args, fire=False, extend_path=None):
    if extend_path is None:
        extend_path = []
    def run_py(path):
        if os.path.exists(path):
            if fire:
                FireUtil.inject_fire(path)
                try:
                    run_python_script(path, args, extend_path=extend_path)
                except Exception as e:
                    print('Error :',e)
                FireUtil.remove_fire(path)
            else:
                run_python_script(path, args, extend_path=extend_path)
        else:
            raise FileNotFoundError(path)
    if path.endswith('.py'):
        run_py(path)
    else:
        run_py(path+'.py')