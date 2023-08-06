# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ._collection import is_dict, is_list, is_tuple
from ._lang import is_boolean, is_float, is_integer, is_string
from ._null import is_null


def is_json(value) -> bool:
    return any((
        is_null(value),
        is_dict(value),
        is_list(value),
        is_tuple(value),
        is_boolean(value),
        is_float(value),
        is_integer(value),
        is_string(value)
    ))
