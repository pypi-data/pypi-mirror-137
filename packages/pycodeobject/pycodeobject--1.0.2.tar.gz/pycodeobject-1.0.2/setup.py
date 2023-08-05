import pycodeobject,os
from setuptools import setup

try:os.chdir(os.path.split(__file__)[0])
except:pass

try:
    long_desc=open("README.rst").read()
except OSError:
    long_desc=pycodeobject.__doc__

setup(
  name='pycodeobject',
  version=pycodeobject.__version__,
  description="""用于解析、编辑Python 字节码(bytecode)的工具。\
A tool which can parse and edit Python bytecode object.""",
  long_description=long_desc,
  author=pycodeobject.__author__,#作者
  author_email=pycodeobject.__email__,
  packages=['pycodeobject'], #这里是所有代码所在的文件夹名称
  keywords=["python","bytecode","字节码","assemble","pyc","uncompile"],
  classifiers=["Topic :: Software Development :: Libraries :: Python Modules",
               "Programming Language :: Python :: 3",
               "Natural Language :: Chinese (Simplified)",
               "Topic :: Software Development :: Assemblers",
               "Topic :: Software Development :: Build Tools",
               "Topic :: Software Development :: Disassemblers",
               "Topic :: Software Development :: Bug Tracking",
               "Topic :: Education"]
)
