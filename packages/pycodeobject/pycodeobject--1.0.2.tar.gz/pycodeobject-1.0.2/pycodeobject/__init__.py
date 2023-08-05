"""用于解析、编辑Python 字节码(bytecode)的工具。\
A tool which can parse and edit Python bytecode object.
"""

import sys
from pprint import pprint
import sys,os

__email__="3416445406@qq.com"
__author__="七分诚意 qq:3076711200 邮箱:%s"%__email__
__version__="1.0.2"

_ignore_names=["__builtins__","__doc__"]
__all__=["objectname","bases","describe","desc",
         "browse","make_list","search"]

def objectname(obj):
    """objectname(obj) - 返回一个对象的名称,形如xxmodule.xxclass。
如:objectname(int) -> 'builtins.int'"""
    if not obj.__class__==type:obj=obj.__class__
    if obj.__module__=="__main__":return obj.__name__
    return "{}.{}".format(obj.__module__,obj.__name__)

def bases(obj,level=0,tab=4):
    '''bases(obj) - 打印出该对象的基类
tab:缩进的空格数,默认为4。'''
    if not obj.__class__==type:obj=obj.__class__
    if obj.__bases__:
        if level:print(' '*(level*tab),end='')
        print(*obj.__bases__,sep=',')
        for cls in obj.__bases__:
            bases(cls,level,tab)
        

def _shortrepr(obj,maxlength=150):
    result=repr(obj)
    if len(result)>maxlength:
        return result[:maxlength]+"..."
    return result

def describe(obj,level=0,maxlevel=1,tab=4,verbose=False,file=sys.stdout):
    '''"描述"一个对象,即打印出对象的各个属性。
参数说明:
maxlevel:打印对象属性的层数。
tab:缩进的空格数,默认为4。
verbose:一个布尔值,是否打印出对象的特殊方法(如__init__)。
file:一个类似文件的对象。
'''
    if level==maxlevel:
        result=repr(obj)
        if result.startswith('[') or result.startswith('{'):pprint(result)
        else:print(result,file=file)
    elif level>maxlevel:raise ValueError(
        "Argument level is larger than maxlevel")
    else:
        print(_shortrepr(obj)+': ',file=file)
        if type(obj) is type:
            print("Base classes of the object:",file=file)
            bases(obj,level+1,tab)
            print(file=file)
        for attr in dir(obj):
            if verbose or not attr.startswith("_"):
                print(' '*tab*(level+1)+attr+': ',end='',file=file)
                try:
                    if not attr in _ignore_names:
                        describe(getattr(obj,attr),level+1,maxlevel,
                                tab,verbose,file)
                    else:print(_shortrepr(getattr(obj,attr)),file=file)
                except AttributeError:
                    print("<AttributeError!>",end='',file=file)

desc=describe #别名

try:
    from pycodeobject.code_ import *
except ImportError:
    # 直接双击运行__init__.py
    sys.path.append(os.path.split(os.getcwd())[0])
    from pycodeobject.code_ import *

if __name__=="__main__":
    import doctest
    doctest.testmod(__import__('pycodeobject.code_').code_)
    interactive()
