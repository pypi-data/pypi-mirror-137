# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import iscoroutinefunction


def is_function(value) -> bool:
    return callable(value)


def is_async_function(value) -> bool:
    return iscoroutinefunction(value)
