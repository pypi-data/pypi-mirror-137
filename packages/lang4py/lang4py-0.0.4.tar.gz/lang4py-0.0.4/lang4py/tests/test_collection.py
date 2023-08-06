# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


class TestCaseLang4pyCollection(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dict = {}
        cls.list = []
        cls.set = set()
        cls.tuple = ()

    def test_is_collection_dict(self):
        self.assertTrue(lang4py.is_dict(self.dict))

    def test_is_collection_list(self):
        self.assertTrue(lang4py.is_list(self.list))

    def test_is_collection_set(self):
        self.assertTrue(lang4py.is_set(self.set))

    def test_is_collection_tup(self):
        self.assertTrue(lang4py.is_tuple(self.tuple))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyCollection("test_is_lang_dict"),
        TestCaseLang4pyCollection("test_is_collection_list"),
        TestCaseLang4pyCollection("test_is_collection_set"),
        TestCaseLang4pyCollection("test_is_collection_tup")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
