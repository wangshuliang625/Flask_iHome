# coding=utf-8
import functools


def func_decorator(func):
    @functools.wraps(func)
    def wrapper(a, b):
        """装饰器闭包函数"""
        func(a, b)

    return wrapper


@func_decorator
def add(a, b):
    """求a和b的和"""
    return a + b


@func_decorator
def add2(a, b):
    """求a和b的和"""
    return a + b

# add = func_decorator(add)


if __name__ == '__main__':
    print add.__name__
    print add.__doc__

    print add2.__name__
    print add2.__doc__
