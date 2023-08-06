# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


class TestCaseLang4pyNull(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.null = None
        cls.not_null = not None

    def test_is_null(self):
        self.assertTrue(lang4py.is_null(self.null))

    def test_is_not_null(self):
        self.assertTrue(lang4py.is_not_null(self.not_null))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyNull("test_is_null"),
        TestCaseLang4pyNull("test_is_not_null")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
