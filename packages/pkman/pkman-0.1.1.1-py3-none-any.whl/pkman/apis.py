from .clitools.package import Package

def load_pkg_info(path):
    return Package(path).load_pkg_info()