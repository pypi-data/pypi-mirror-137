# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


class TestCaseLang4pyLang(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.str = "abc"
        cls.bool = False
        cls.int = 123
        cls.float = 123.0

    def test_is_lang_bool(self):
        self.assertTrue(lang4py.is_boolean(self.bool))

    def test_is_lang_float(self):
        self.assertTrue(lang4py.is_float(self.float))

    def test_is_lang_int(self):
        self.assertTrue(lang4py.is_integer(self.int))

    def test_is_lang_str(self):
        self.assertTrue(lang4py.is_string(self.str))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyLang("test_is_lang_bool"),
        TestCaseLang4pyLang("test_is_lang_float"),
        TestCaseLang4pyLang("test_is_lang_int"),
        TestCaseLang4pyLang("test_is_lang_str")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
