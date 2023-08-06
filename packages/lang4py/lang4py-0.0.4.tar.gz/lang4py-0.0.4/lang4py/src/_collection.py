# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
def is_dict(value) -> bool:
    return isinstance(value, dict)


def is_list(value) -> bool:
    return isinstance(value, list)


def is_set(value) -> bool:
    return isinstance(value, set)


def is_tuple(value) -> bool:
    return isinstance(value, tuple)
