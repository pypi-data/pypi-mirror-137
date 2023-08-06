# -*- coding: utf-8 -*-
"""
Simple_file_user package includes functions and a class for more flexible and easy working with files.

This is list of functions included this package:
    read(path: str, encoding: str = "utf-8", binary_mode: bool = False) -> str ---- Read file and return it's content. If binary mode is True open file in binary mode.
    rewrite(path: str, content: str, encoding: str = "utf-8") -> int ---- Clear file and write content into it. Return amount of written symbols.
    add(path: str, content: str, encoding = "utf-8") -> int ---- Add content into file. Return amount of written symbols.
    remove(path: str) -> None ---- Remove file (path).
    rename(path: str, new_name: str) -> None ---- Change name of file (path) to new_name.
    getSize(path: str) -> int ---- Return size of file (path) in bytes.
    writeToFile(path: str, encoding: str = "utf-8") ---- It is decorator. Return function that write to file (path) returning of decorated callable object.
    addToFile(path: str, encoding: str = "utf-8") ---- It is decorator. Return function that add to file (path) returning of decorated callable object.

Copyright (c) 2022 Vennetskiy Andrew Dmitrievich <internetstalcker@yandex.ru>
"""
import os
from .File import *

__version__ = "0.1"
__all__ = ['File']




def read(path: str, encoding: str = "utf-8", binary_mode: bool = False) -> str:
    r"""
    read(path: str, encoding: str = "utf-8", binary_mode: bool = False) -> str ---- Read file and return it's content. 
    If binary mode is True, open file in binary mode. If binary_mode is True, you don't need to pass encoding, but it 
    won't raise exception like read method of builtin file object if you've done it. If file doesn't exist raise 
    exception FileNotFoundError.
    """
    if binary_mode:
        with open(path, "br") as file:
            content = file.read()
    else:
        with open(path, "tr", encoding = encoding) as file:
            content = file.read()
    return content


def rewrite(path: str, content: str, encoding: str = "utf-8") -> int:
    """
    rewrite(path: str, content: str, encoding: str = "utf-8") -> int ---- Clears file and write content into it. 
    Return amount of written symbols. If file doesn't exist, create it.
    """
    with open(path, "w", encoding = encoding) as file:
        size = file.write(content)
    return size


def add(path: str, content: str, encoding: str = "utf-8") -> int:
    """
    add(path: str, content: str, encoding = "utf-8") -> int ---- Add content into file. Return amount of written symbols.
    If file doesn't exist, create it.
    """
    with open(path, "a", encoding = encoding) as file:
        size = file.write(content)
    return size


def remove(path: str) -> None:
    """
    remove(path: str) -> None ---- Remove file (path).
    """
    os.remove(path)


def rename(path: str, new_name: str) -> None:
    """
    rename(path: str, new_name: str) -> None ---- Change name of file (path) to new_name. If file doesn't exist, raise
    FileNotFoundError.
    """
    os.rename(path, new_name)


def getSize(path: str) -> int:
    """
    getSize(path: str) -> int ---- Returns size of file (path) in bytes. If file doesn't exist, raise FileNotFoundError.
    """
    return os.path.getsize(path)


def writeToFile(path: str, encoding: str = "utf-8"):
    """
    writeToFile(path: str, encoding: str = "utf-8") ---- It is decorator. Return function that write to file (path) returning of decorated callable object.
    """
    def wrapper(function):
        def ar(*args, **kwargs):
            file = File(path = path, encoding = encoding, new = True)
            file.write(function(*args, **kwargs), "w")
        return ar
    return wrapper

def addToFile(path: str, encoding: str = "utf-8"):
    """
    addToFile(path: str, encoding: str = "utf-8") ---- It is decorator. Return function that add to file (path) returning of decorated callable object.
    """
    def wrapper(function):
        def ar(*args, **kwargs):
            file = File(path = path, encoding = encoding, new = False)
            file.write(function(*args, **kwargs), "a")
        return ar
    return wrapper