from distutils.core import setup
from distutils.core import Extension
from distutils.command.install import install
from distutils.command.build import build
from distutils.command.build_ext import build_ext
from distutils.sysconfig import get_config_vars

import subprocess
import shutil
import glob
import os
import sys

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        self.compiler.define_macro("PYTHON_MAJOR_VERSION", sys.version_info[0])
        print("Testing for std::tr1::shared_ptr...")
        try:
            self.compiler.compile(['test_std_tr1_shared_ptr.cpp'])
            self.compiler.define_macro("HAVE_STD_TR1_SHARED_PTR")
            print("...found")
        except:
            print(" ...not found")

        print("Testing for std::shared_ptr...")
        try:
            self.compiler.compile(['test_std_shared_ptr.cpp'], extra_preargs=['-std=c++0x']),
            self.compiler.define_macro("HAVE_STD_SHARED_PTR")
            print("...found")
        except:
            print("...not found")

        print("Testing for std::unique_ptr...")
        try:
            self.compiler.compile(['test_std_unique_ptr.cpp'], extra_preargs=['-std=c++0x']),
            self.compiler.define_macro("HAVE_STD_UNIQUE_PTR")
            print("...found")
        except:
            print("...not found")
    
        build_ext.build_extensions(self)

# Remove the "-Wstrict-prototypes" compiler option, which isn't valid for C++.
import distutils.sysconfig
cfg_vars = distutils.sysconfig.get_config_vars()
for key, value in cfg_vars.items():
    if type(value) == str:
        cfg_vars[key] = value.replace("-Wstrict-prototypes", "")
        
setup(name='quickfix-ssl-2',
      version='1.15.1-4',
      py_modules=[
        'src/python/quickfix',
        'src/python/quickfixt11', 
        'src/python/quickfix40', 
        'src/python/quickfix41', 
        'src/python/quickfix42', 
        'src/python/quickfix43', 
        'src/python/quickfix44', 
        'src/python/quickfix50', 
        'src/python/quickfix50sp1', 
        'src/python/quickfix50sp2'
      ],
      data_files=[('share/quickfix', glob.glob('spec/FIX*.xml'))],
      author='Oren Miller',
      author_email='oren@quickfixengine.org',
      maintainer='Giovanni Opromolla',
      maintainer_email='giopromolla@gmail.com',
      description="FIX (Financial Information eXchange) protocol implementation (SSL enabled)",
      url='http://www.quickfixengine.org',
      download_url='http://www.quickfixengine.org',
      license='MIT',
      include_dirs=['src/C++',],
      cmdclass = {'build_ext': build_ext_subclass },
      ext_modules=[Extension('_quickfix', glob.glob('src/C++/*.cpp'), extra_compile_args=['-std=c++0x', '-Wno-deprecated', '-Wno-unused-variable', '-Wno-deprecated-declarations', '-Wno-maybe-uninitialized'])],
)
