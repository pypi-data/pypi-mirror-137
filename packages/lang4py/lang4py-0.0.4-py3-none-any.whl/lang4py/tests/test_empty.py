# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


class TestCaseLang4pyEmpty(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.e_dict = {}
        cls.e_list = []
        cls.e_set = set()
        cls.e_str = ""
        cls.e_tup = ()
        cls.false = False
        cls.none = None

    def test_is_empty_dict(self):
        self.assertTrue(lang4py.is_empty(self.e_dict))

    def test_is_empty_list(self):
        self.assertTrue(lang4py.is_empty(self.e_list))

    def test_is_empty_set(self):
        self.assertTrue(lang4py.is_empty(self.e_set))

    def test_is_empty_str(self):
        self.assertTrue(lang4py.is_empty(self.e_str))

    def test_is_empty_tup(self):
        self.assertTrue(lang4py.is_empty(self.e_tup))

    def test_is_empty_false(self):
        self.assertTrue(lang4py.is_empty(self.false))

    def test_is_empty_none(self):
        self.assertTrue(lang4py.is_empty(self.none))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyEmpty("test_is_empty_dict"),
        TestCaseLang4pyEmpty("test_is_empty_list"),
        TestCaseLang4pyEmpty("test_is_empty_set"),
        TestCaseLang4pyEmpty("test_is_empty_str"),
        TestCaseLang4pyEmpty("test_is_empty_tup"),
        TestCaseLang4pyEmpty("test_is_empty_false"),
        TestCaseLang4pyEmpty("test_is_empty_none")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
