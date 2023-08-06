# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
def is_bytes(value) -> bool:
    return isinstance(value, bytes)


def is_bytearray(value) -> bool:
    return isinstance(value, bytearray)
