import os
import site
import sys
import pkg_resources
from setuptools import setup, Extension
from Cython.Distutils import build_ext
from autowrap.Main import run as autowrap_run

# This line enable user based installations when in editable mode
site.ENABLE_USER_SITE = "--user" in sys.argv[1:]

data_dir = pkg_resources.resource_filename("autowrap", "data_files")
include_dir = os.path.join(data_dir, "autowrap")

autowrap_run(
    [os.path.abspath('./src/chenhancc.pxd')],
    [], [], os.path.abspath('./src/geodesic_chenhan.pyx'))

ext = Extension(
    "geodesic_chenhan",
    sources=['src/geodesic_chenhan.cpp'],
    language="c++",
    extra_compile_args=["-std=c++14"],
    extra_link_args=["-std=c++14"],
    include_dirs=[include_dir, data_dir],
)

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[ext],
)
