# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 13:42:12
# @Author  : DannyDong
# @File    : CatchError.py
# @Describe: 捕获异常装饰器

def catcherr(func):
    def wapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except:
            # 抛出异常，信息为方法注释信息
            raise Exception('【{}】操作错误'.format(func.__doc__))
        return res
    return wapper


if __name__ == '__main__':
    pass
