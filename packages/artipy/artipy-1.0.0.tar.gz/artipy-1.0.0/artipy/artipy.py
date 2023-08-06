from setuptools import Extension
from setuptools.command.build_py import build_py as build_py_orig
from Cython.Build import cythonize
import os


def find_extensions(name):
    ex = []
    prefix = os.path.split(__file__)[0]
    dirname = os.path.join(os.path.split(__file__)[0], name)
    for root, subdirs, files in os.walk(dirname):
        if any(fname.endswith('.py') for fname in os.listdir(root)):
            path = root.replace(prefix + '/', "")
            ex.append((path.replace('/', '.') + '.*', [path + "/*.py"]))
    return [Extension(*x) for x in ex]


class build_py(build_py_orig):
    def build_packages(self):
        pass


def artipy(dirname):
    return {
        'ext_modules': cythonize(find_extensions(dirname)),
        'cmdclass': {'build_py': build_py},
    }
