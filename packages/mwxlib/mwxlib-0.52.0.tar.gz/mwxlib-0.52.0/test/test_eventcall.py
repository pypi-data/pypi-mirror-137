#! python
# -*- coding: utf-8 -*-
import wx
import mwx
import unittest
import platform
from misc import echo
from utilus import inspect_args

## mwx.apropos(platform, '', pred=callable)

print("--------------------------------")
@echo
@inspect_args
def func(self, a, b, c=0, *args, **kwargs):
    """Test func"""
    print("(a,b,c) =", (a,b,c))
    pass


print("--------------------------------")
@inspect_args
def func2(self, a, b, c=0, *args, key:int, value:int=0, **kwargs) -> int:
    """This function uses new syntax"""
    print("(a,b,c) =", (a,b,c))
    pass

print("--------------------------------")
@inspect_args
class A(object):
    """class doc:str"""
    @inspect_args
    def func(self, a, b, c=1, *args, **kwargs):
        """method doc:str"""
        pass


if __name__ == "__main__":
    a = A()
    a.func(1,2,3)
    inspect_args(a)
    func(1,2,3,4,5,end=6)

## f = mwx.funcall(func)
## print(inspect_args(f))
## 
## ## f(None, -1) # TypeError: func() missing 1 required positional argument: 'b'
## f(None, -1, -2) # ok
## f(None, -1, -2, -3) # ok
## f(None, -1, -2, -3, -4) # ok
