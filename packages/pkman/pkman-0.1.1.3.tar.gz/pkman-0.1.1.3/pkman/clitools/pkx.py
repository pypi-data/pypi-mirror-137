import os
import sys
import requests
from .utils import CmdUtil,IoUtil,StringUtil,PathUtil,FireUtil
from .config import PACKAGE_CONFIG_FILENAME
os.environ['ANSI_COLORS_DISABLED']="1"
import fire
from . import apis
from freehub import apis as fh_api
from freehub.apis import Address
from .apis import app_data_manager
from .package import Package


def fetch_web_text(url):
    return requests.get(url).text
def load_pkg_info():
    pkg_info = IoUtil.json_load(os.path.join(os.getcwd(), PACKAGE_CONFIG_FILENAME))
    return pkg_info
class TYPES:
    class WEB_TEXT:
        pass
    class GIT_FILE:
        pass
    class PACKAGE:
        pass
def complete_address(address):
    return fh_api.get_complete_address(address)
def run_package(path,args):
    p=Package(path)
    p.install_dependencies()
    p.run(args)
class Cli:
    @classmethod
    def pkx(cls,address: str, *args, **kwargs):

        if address.startswith('http://') or address.startswith('https://'):
            text = fetch_web_text(address)
            filename = StringUtil.hash_text(address)[:10] + '.py'
            file_path = app_data_manager.tempfile(filename)
            IoUtil.write_txt(text, file_path)
            CmdUtil.run_file(file_path, sys.argv[2:])
        else:
            addr = Address.from_url(Address.get_complete_address(address))
            branch_addr = Address(addr.protocol, addr.host, addr.username, addr.repo_name, addr.branch_name, '/')
            branch_dir = fh_api.fetch(branch_addr.to_url())
            dst_path = PathUtil.join_path(branch_dir, addr.rel_path)
            if os.path.isdir(dst_path):
                run_package(dst_path, sys.argv[2:])
            else:
                CmdUtil.run_file(dst_path, sys.argv[2:],extend_path=[os.path.dirname(dst_path)])

    @classmethod
    def pkfire(cls, address: str, *args, **kwargs):
        if address.startswith('http://') or address.startswith('https://'):
            text = fetch_web_text(address)
            filename = StringUtil.hash_text(address)[:10] + '.py'
            file_path = app_data_manager.tempfile(filename)
            IoUtil.write_txt(text, file_path)
            CmdUtil.run_file(file_path, sys.argv[2:],fire=True)
        else:
            addr = Address.from_url(Address.get_complete_address(address))
            branch_addr = Address(addr.protocol, addr.host, addr.username, addr.repo_name, addr.branch_name, '/')
            branch_dir = fh_api.fetch(branch_addr.to_url())
            dst_path = PathUtil.join_path(branch_dir, addr.rel_path)
            if os.path.isdir(dst_path):
                run_package(dst_path, sys.argv[2:])
            else:
                CmdUtil.run_file(dst_path, sys.argv[2:], extend_path=[os.path.dirname(dst_path)],fire=True)
def main():
    fire.Fire(Cli().pkx)
if __name__ == '__main__':
    main()