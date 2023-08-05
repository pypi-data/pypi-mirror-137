# pyc文件压缩、保护工具
import sys,marshal
from inspect import iscode
from pycodeobject.code_ import Code
try:
    from importlib._bootstrap_external import MAGIC_NUMBER
except ImportError:
    from importlib._bootstrap import MAGIC_NUMBER

def dump_to_pyc(pycfilename,code):
    # 制作pyc文件
    with open(pycfilename,'wb') as f:
        # 写入 pyc 文件头
        if sys.winver >= '3.7':
            pycheader=MAGIC_NUMBER+b'\x00'*12
        else:
            pycheader=MAGIC_NUMBER+b'\x00'*8
        f.write(pycheader)
        # 写入bytecode
        marshal.dump(code._code,f)

def process_code(co):
    co.co_lnotab = b''
    co.co_code += b'S\x00'
    co.co_filename = ''
    #co.co_name = ''
    co_consts = co.co_consts
    for i in range(len(co_consts)):
        obj = co_consts[i]
        if iscode(obj):
            data=process_code(Code(obj))
            co_consts = co_consts[:i] + (data._code,) + co_consts[i+1:]
    co.co_consts = co_consts
    return co
if len(sys.argv) == 1:
    print('Usage: %s [filename]' % sys.argv[0])

for file in sys.argv[1:]:
    data=open(file,'rb').read()
    data=data[16:] if data[16]==227 else data[12:]
    co = Code(marshal.loads(data))

    process_code(co)
    dump_to_pyc(file,co)
    print('Processed:',file)
