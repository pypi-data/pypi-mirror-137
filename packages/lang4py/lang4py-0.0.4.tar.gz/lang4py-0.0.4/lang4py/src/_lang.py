# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
def is_boolean(value) -> bool:
    return isinstance(value, bool)


def is_float(value) -> bool:
    return isinstance(value, float)


def is_integer(value) -> bool:
    return isinstance(value, int)


def is_number(value) -> bool:
    return any((is_int(value), is_float(value)))


def is_string(value) -> bool:
    return isinstance(value, str)
