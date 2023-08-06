import json
import os.path

from .utils import IoUtil,OsUtil
from .config import PACKAGE_CONFIG_FILENAME
from .utils.AppDataManager import AppDataManager
from .utils import CmdUtil,IoUtil,StringUtil,PathUtil,FireUtil
from .utils.AppDataManager import app_data_manager

def init_config_file(root_path):

    # if not OsUtil.is_empty_dir(root_path):
    #     raise Exception('Not an empty directory:',root_path)
    def input_field(description, default, keep_empty):
        res = input('%s: (%s)' % (description, default)).strip() if default is not None else input(
            '%s: ' % (description)).strip()
        if res:
            return res
        elif default is not None:
            return default
        elif keep_empty:
            return ""
        else:
            return default

    def field(description, default=None, keep_empty=False):
        return dict(description=description, default=default, keep_empty=keep_empty)

    form = dict(
        name=field(description="package name", default=os.path.basename(os.path.abspath(os.getcwd()))),
        package_dir=field(description="package directory name", default=os.path.basename(os.path.abspath(os.getcwd())).replace("-","_")),
        version=field(description="version", default="0.0.0.1"),
        description=field(description="description", keep_empty=True),
        # entry_point=field(description="entry point", default="main.py"),
        test_command=field(description="test command"),
        git_repository=field(description="git repository"),
        keywords=field(description="keywords (separated with ',')"),
        author=field(description="author", keep_empty=True),
        license=field(description="license", default='MIT'),
        python_requires=field(description="required python version", default='>=3.0'),
    )

    def fill_form(form):
        result = {}
        for k, f in form.items():
            v = input_field(f['description'], f['default'], f["keep_empty"])
            if v is not None:
                result[k] = v
        return result

    info = fill_form(form)
    if "test_command" in info.keys():
        test_command = info.pop("test_command")
    else:
        test_command = 'echo "Error: no test specified"'
    info["scripts"] = {"test": test_command}

    if "git_repository" in info.keys():
        repository = {
            "type": "git",
            "url": info.pop("git_repository")
        }
        info["repository"]=repository
    if "keywords" in info and info["keywords"]:
        info["keywords"]=[x.strip() for x in info["keywords"].split(',')]
    pkg_name=info['name']
    package_dir=info['package_dir']
    extra_fields = dict(
        author_email="",
        url="",
        dependencies=[],
        package_dir=package_dir,
        entry_points={
            'console_scripts': [
                '%s = %s.clitools.cli:main'%(pkg_name,package_dir)
            ]
        },
        include_package_data=True,
        package_data={
            package_dir: [
                'data/*', 'data/*/*', 'data/*/*/*', 'data/*/*/*/*', 'data/*/*/*/*/*', 'data/*/*/*/*/*/*',
                'data/*/*/*/*/*/*/*',
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
    )
    info.update(extra_fields)
    pkg_config_path=os.path.join(root_path,PACKAGE_CONFIG_FILENAME)
    IoUtil.json_dump(info,pkg_config_path,indent=2)
    print(IoUtil.read_txt(pkg_config_path))
    return info
def init_readme(pkg_name,description,root_path):
    readme_path=os.path.join(root_path,"README.md")
    readme_content='''# %s\n---\n%s'''%(pkg_name,description)
    IoUtil.write_txt(readme_content,readme_path)
def init(root_path=None):
    if not root_path:
        root_path=os.getcwd()
    info=init_config_file(root_path)
    init_readme(info['name'],info['description'],root_path)

def up_version(root_path=None):
    if not root_path:
        root_path=os.getcwd()
    config_file_path=os.path.join(root_path,PACKAGE_CONFIG_FILENAME)
    cfg=IoUtil.json_load(config_file_path)
    def version_grow(version, index=-1, limit=None):
        if limit is None:
            limit = [9, 9, 9, 9, 9, 9, 9]
        def to_array(v):
            return [int(x) for x in v.split('.')]
        def to_string(v):
            return '.'.join([str(x) for x in v])
        version=to_array(version)
        if index == -1: index = len(version) - 1
        version[index] += 1
        if version[index] > limit[len(version) - index - 1]:
            version[index] = 0
            if index == 0:
                raise Exception('Max version number reached. %s' % (version))
            return version_grow(to_string(version), index - 1,limit)
        else:
            return to_string(version)
    cfg['version']=version_grow(cfg['version'])
    IoUtil.json_dump(cfg,config_file_path,indent=2)



