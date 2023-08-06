from setuptools import Extension
from setuptools.command.build_py import build_py as build_py_orig
import shutil

from Cython.Build import cythonize
import os


def find_extensions(name, setup_py):
    ex = []
    prefix = os.path.split(setup_py)[0]
    dirname = os.path.join(prefix, name)
    for root, subdirs, files in os.walk(dirname):
        if any(fname.endswith('.py') for fname in os.listdir(root)):
            path = root.replace(prefix + '/', "")
            ex.append((path.replace('/', '.') + '.*', [path + "/*.py"]))
    return [Extension(*x) for x in ex]


class build_py(build_py_orig):

    def build_packages(self):
        pass


def artipy(dirname, setup_py, **kwargs):
    if os.environ.get('DISABLE_ARTIPY') == "1":
        return {}
    else:
        return {
            'ext_modules': cythonize(find_extensions(dirname, setup_py), **kwargs),
            'cmdclass': {'build_py': build_py},
        }


def clean(setup_py):
    if os.environ.get('NO_CLEAR_ARTIPY') == "1":
        return
    else:
        dirname = os.path.split(setup_py)[0]
        print(dirname)
        shutil.rmtree(os.path.join(dirname, "build"))
        for root, subdirs, files in os.walk(dirname):
            for fname in os.listdir(root):
                fname.endswith('.c')
                os.remove(fname)
