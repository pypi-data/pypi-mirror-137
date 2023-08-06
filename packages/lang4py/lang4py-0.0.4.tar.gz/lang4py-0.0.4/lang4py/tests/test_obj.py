# @Time     : 2021/11/1
# @Project  : wanba_py
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
import unittest

from lang4py import lang4py


class TestCaseLang4pyPyObj(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.dict = {}
        cls.list = []
        cls.set = set()
        cls.tup = ()
        cls.int = 1
        cls.float = 1.0
        cls.str = "abc"
        cls.none = None
        cls.bool = False

    def test_is_json_dict(self):
        self.assertTrue(lang4py.is_json(self.dict))

    def test_is_json_list(self):
        self.assertTrue(lang4py.is_json(self.list))

    def test_is_json_set(self):
        self.assertFalse(lang4py.is_json(self.set))

    def test_is_json_str(self):
        self.assertTrue(lang4py.is_json(self.str))

    def test_is_json_tup(self):
        self.assertTrue(lang4py.is_json(self.tup))

    def test_is_json_bool(self):
        self.assertTrue(lang4py.is_json(self.bool))

    def test_is_json_none(self):
        self.assertTrue(lang4py.is_json(self.none))

    def test_is_json_int(self):
        self.assertTrue(lang4py.is_json(self.int))

    def test_is_json_float(self):
        self.assertTrue(lang4py.is_json(self.float))


def main():
    suite = unittest.TestSuite()
    suite.addTests([
        TestCaseLang4pyPyObj("test_is_json_dict"),
        TestCaseLang4pyPyObj("test_is_json_list"),
        TestCaseLang4pyPyObj("test_is_json_set"),
        TestCaseLang4pyPyObj("test_is_json_str"),
        TestCaseLang4pyPyObj("test_is_json_tup"),
        TestCaseLang4pyPyObj("test_is_json_bool"),
        TestCaseLang4pyPyObj("test_is_json_none"),
        TestCaseLang4pyPyObj("test_is_json_int"),
        TestCaseLang4pyPyObj("test_is_json_float")
    ])
    runner = unittest.TextTestRunner()
    runner.run(suite)


if __name__ == '__main__':
    main()
