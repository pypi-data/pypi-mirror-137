# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


class TestCaseLang4pyString(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.b_str = b"abc"
        cls.b_strings = bytearray()

    def test_is_bytes(self):
        self.assertTrue(lang4py.is_bytes(self.b_str))

    def test_is_bytearray(self):
        self.assertTrue(lang4py.is_bytearray(self.b_strings))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyString("test_is_bytes"),
        TestCaseLang4pyString("test_is_bytearray")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
