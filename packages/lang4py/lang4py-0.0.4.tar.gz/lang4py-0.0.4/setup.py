# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from scripts.install import install

_version = "0.0.4"
requires = []

if __name__ == '__main__':
    install("lang4py", _version, filename="README.md")
