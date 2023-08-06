# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from asyncio import iscoroutine, isfuture, Task


def is_coroutine(value) -> bool:
    return iscoroutine(value)


def is_future(value) -> bool:
    return isfuture(value)


def is_task(value) -> bool:
    return isinstance(value, Task)
