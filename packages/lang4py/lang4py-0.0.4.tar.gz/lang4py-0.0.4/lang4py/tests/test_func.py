# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


def fn():
    pass


async def afn():
    pass


class TestCaseLang4pyFn(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.fn = fn
        cls.afn = afn

    def test_is_func_fn(self):
        self.assertTrue(lang4py.is_function(self.fn))

    def test_is_func_afn(self):
        self.assertTrue(lang4py.is_async_function(self.afn))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyFn("test_is_func_fn"),
        TestCaseLang4pyFn("test_is_func_afn")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
