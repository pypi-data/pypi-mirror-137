# coding=utf-8

"""
@Author: LiangChao
@Email: kevinleong1011@hotmail.com
@Desc: 
"""
import os
import sys

from .ospath import Path


def insert(root):
    """
    将路径插入sys.path
    :param root:
    :return:
    """
    if root in sys.path:
        sys.path.remove(root)
    sys.path.insert(0, root)
    return root


def find_project_root(path):
    """
    查找py工程根目录
    :param path:
    :return:
    """
    path = os.path.abspath(path)
    path = Path(path)
    root = path.parent if os.path.isfile(str(path)) else path
    while os.path.exists(os.path.join(root, '__init__.py')):
        root = root.parent
    return root


# def get_object(name: str, raise_error=True):
#     """
#     根据名称获取对象
#     :param name: 对象全名称，比如 demo.test.TestClass.my_method
#     :param raise_error: 是否抛出异常
#     :return: module/type/function
#     """
#     if not name:
#         return
#     if os.path.exists(name):
#         name = os.path.abspath(name)
#         return import_file(name)
#     else:
#         nodes = name.split('.')
#         o, module_name = None, ''
#         for i in range(len(nodes)):
#             module_name = '.'.join(nodes[:i + 1])
#             try:
#                 o = __import__(module_name)
#                 i += 1
#             except ModuleNotFoundError:
#                 break
#         if o:
#             for node in nodes[1:]:
#                 o = getattr(o, node, None)  # 如果py文件中直接写该函数调用，可能取不到，但不是问题
#         if not o and raise_error:
#             raise ModuleNotFoundError(module_name)
#         return o


def import_file(filename, relpath=None):
    """
    从文件导入，并返回Module对象
    :param filename: 文件路径
    :param relpath: 相对路径
    :return:
    """
    if not relpath:
        relpath = os.path.dirname(filename)
    sys.path.insert(0, relpath)
    try:
        abspath = os.path.relpath(filename, relpath)
        modulename = abspath.replace('/', '.').replace('\\', '.')[:-3]
        m = __import__(modulename)
        parts = modulename.split('.')
        for p in parts[1:]:
            m = getattr(m, p)
        return m
    except ImportError:
        sys.path.remove(relpath)
        if os.path.ismount(relpath):
            raise
        return import_file(filename, os.path.dirname(relpath))


def parse_obj(name: str, raise_error=True):
    """
    Parse obj from name. 从名称解析python对象
    :param name:
    :param raise_error:
    :return:
    """
    nodes = name.split('.')
    o, module_name = None, ''
    for i in range(len(nodes)):
        module_name = '.'.join(nodes[:i + 1])
        try:
            o = __import__(module_name)
            i += 1
        except ModuleNotFoundError:
            break
    if o:
        for node in nodes[1:]:
            o = getattr(o, node, None)  # 如果py文件中直接写该函数调用，可能取不到，但不是问题
    if not o and raise_error:
        raise ModuleNotFoundError(module_name)
    return o
