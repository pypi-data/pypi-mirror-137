import json
import os
import subprocess
import sys

import setuptools
from . import IoUtil,StringUtil
from .AppDataManager import app_data_manager


def setup_package(name, version, author, author_email, description, url, dependencies, entry_points, package_data, python_requires, classifiers, package_dir=None,
                  cmd=None, **kwargs):
    if cmd is None:
        cmd = ["sdist", "bdist_wheel"]
    if not package_dir:
        package_dir={name:name}
    elif isinstance(package_dir,str):
        package_dir={package_dir:package_dir}

    packages = setuptools.find_packages(exclude=['local', 'local.*'])
    files=os.listdir('.')
    long_description="No long_description",
    long_description_content_type="text/plain"
    for f in files:
        if f.lower()=='readme.md':
            with open(f,'r',encoding='utf-8') as fp:
                long_description=fp.read()
                long_description_content_type="text/markdown"
        elif f.lower()=='readme.txt':
            with open(f,'r',encoding='utf-8') as fp:
                long_description=fp.read()
                long_description_content_type="text/plain"
    cfg = dict(
        # executable=True,
        name=name,  # Replace with your own username
        version=version,
        author=author,
        author_email=author_email,
        description=description,
        long_description=long_description,
        long_description_content_type=long_description_content_type,
        url=url,
        packages=packages,
        package_dir=package_dir,
        install_requires=dependencies,
        include_package_data=True,
        entry_points=entry_points,
        package_data=package_data,
        classifiers=classifiers,
        python_requires=python_requires,
    )
    # cfg.update(**kwargs)
    jsonfile=app_data_manager.tempfile("setup_config_"+StringUtil.hash_text(json.dumps(cfg))[:10]+".json")
    setupfile=app_data_manager.tempfile("setup_"+StringUtil.hash_text(json.dumps(cfg))[:10]+".py")
    IoUtil.json_dump(cfg,jsonfile)
    setuppy_content='''import setuptools
import json
with open(r"%s","r",encoding="utf-8") as f:
    cfg=json.load(f)
setuptools.setup(**cfg)'''%(jsonfile)
    IoUtil.write_txt(setuppy_content,setupfile)
    try:
        subprocess.check_call([sys.executable, setupfile, *cmd], shell=True)
    except Exception as e:
        print(e)
    os.remove(jsonfile)
    os.remove(setupfile)




