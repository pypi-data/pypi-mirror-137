import re
import unittest

from dipas.utils import get_type_hints_with_boundary, PatternDict


class TestGetTypeHintsWithBoundary(unittest.TestCase):
    def test(self):
        class A:
            a: int

        class B(A):
            b: int

        class C(B):
            c: int

        self.assertSequenceEqual(list(get_type_hints_with_boundary(C)), ['a', 'b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=object)), ['a', 'b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=A)), ['a', 'b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=B)), ['b', 'c'])
        self.assertSequenceEqual(list(get_type_hints_with_boundary(C, boundary=C)), ['c'])


# noinspection PyStatementEffect
class TestPatternDict(unittest.TestCase):
    def test_plain_strings(self):
        d = PatternDict()
        d['abc'] = 1
        self.assertTrue(all(isinstance(k, re.Pattern) for k in d))
        self.assertEqual(d['abc'], 1)
        with self.assertRaises(KeyError) as err:
            d['a']
        self.assertEqual(str(err.exception), "'a'")

    def test_wildcard(self):
        d = PatternDict()
        d['a*c'] = 1
        d['a*d'] = 2
        self.assertTrue(all(isinstance(k, re.Pattern) for k in d))
        self.assertEqual(d['ac'], 1)
        self.assertEqual(d['axc'], 1)
        self.assertEqual(d['axxc'], 1)
        self.assertEqual(d['ad'], 2)
        self.assertEqual(d['axd'], 2)
        self.assertEqual(d['axxd'], 2)
        with self.assertRaises(KeyError) as err:
            d['a']
        self.assertEqual(str(err.exception), "'a'")

    def test_regex(self):
        d = PatternDict()
        d[re.compile('[0-9]{1,3}')] = 1
        self.assertTrue(all(isinstance(k, re.Pattern) for k in d))
        self.assertEqual(d['1'], 1)
        self.assertEqual(d['12'], 1)
        self.assertEqual(d['123'], 1)
        with self.assertRaises(KeyError) as err:
            d['1234']
        self.assertEqual(str(err.exception), "'1234'")

    # noinspection PyTypeChecker
    def test_invalid_type_for_setitem(self):
        d = PatternDict()
        with self.assertRaises(TypeError):
            d[1] = 1
        with self.assertRaises(TypeError):
            d[(1, 2)] = 1

    # noinspection PyTypeChecker
    def test_invalid_type_for_getitem(self):
        d = PatternDict()
        with self.assertRaises(TypeError):
            d[1]
        with self.assertRaises(TypeError):
            d[re.compile('a')]


if __name__ == '__main__':
    unittest.main()
