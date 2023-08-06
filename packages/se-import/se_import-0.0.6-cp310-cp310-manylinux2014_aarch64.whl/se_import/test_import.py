# -*- coding: utf-8 -*-
# @Time    : 2021/11/9 16:42

import sys
import se_import
print(dir(se_import))

#从内存加载模块
def test_load_mem():
    s = "a = 100\nb=1000"
    #自定义模块名
    name = 'test_load_mem_test'
    ret = se_import.load_module(name,s,name + '.py')
    print(ret)
    print(dir(ret))
    print(ret.a)
    print(ret.b)

#从内存加载模块，支持模块解密回调
def test_load_custom():
    #从内存加载模块
    s = "a = 100\nb=1000"
    # 自定义模块名
    name = 'load_module_custom_test'
    ret= se_import.load_module_custom(name,s,name + '.py',lambda x:x + '\nadasdadada=1000')
    print(ret)
    print(dir(ret))
    print(ret.a)
    print(ret.b)

#从本地 des加密文件加载模块
def test_save_load_desfile():

    #模块des 加密，保存到文件
    infile = "./des.py"
    outfile = './des.pys'
    key = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    iv = bytes([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    #第一个参数类型是字符串 是文件名， bytes 则为二进制文件内容
    ret = se_import.dump_module_to_desfile(infile, key, iv)
    with open(outfile,mode='wb') as f:
        f.write(ret)

    #从文件加载加密模块
    # 自定义模块名
    infile = './des.pys'
    name = 'test_save_load_desfile_test'
    ret2 = se_import.load_module_from_desfile(name,infile,name + '.py')
    print(ret2)
    print(dir(ret2))

if __name__ == '__main__':
    test_save_load_desfile()