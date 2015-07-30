import unittest

import comparador as c

class TestComparator(unittest.TestCase):
    def test_basics(self):
        cm = c.Comparator({'a': int})
        self.assertFalse(cm.match({'b': 1}))
        self.assertFalse(cm.match({'a': 1.0}))
        self.assertTrue(cm.match({'a': 1}))

        cm = c.Comparator({'a': str})
        self.assertFalse(cm.match({'b': u'a'}))
        self.assertFalse(cm.match({'a': 23}))
        self.assertTrue(cm.match({'a': 'a'}))

        cm = c.Comparator({'a': {'b': int}})
        self.assertFalse(cm.match({'b': {'b': 1}}))
        self.assertFalse(cm.match({'a': {'a': 1}}))
        self.assertFalse(cm.match({'a': {'b': ''}}))
        self.assertTrue(cm.match({'a': {'b': 1}}))

    def test_In(self):
        cm = c.Comparator({'a': (c.In, range(0,5,2))})
        self.assertFalse(cm.match({'a': 1}))
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': 10}))
        self.assertTrue(cm.match({'a': 2}))

    def test_Like(self):
        cm = c.Comparator({'a': (c.Like, '\d,\w+')})
        self.assertFalse(cm.match({'a': '1,'}))
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': '10'}))
        self.assertTrue(cm.match({'a': '1,0102dsada_dede'}))

    def test_Date(self):
        cm = c.Comparator({'a': (c.Date, '%Y-%d-%m')})
        self.assertFalse(cm.match({'a': '2015-02-31'}))
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': '2015-32-01'}))
        self.assertTrue(cm.match({'a': '2015-30-01'}))

    def test_Excl(self):
        cm = c.Comparator({'a': (c.Excl, ('1', '2'), {'1': int, '2': str})})
        self.assertFalse(cm.match({'a': {'1': 's'}}))
        self.assertFalse(cm.match({'a': {'2': 1}}))
        self.assertFalse(cm.match({'a': {'1': 1, '2': 's'}}))
        self.assertTrue(cm.match({'a': {'1': 1}}))
        self.assertTrue(cm.match({'a': {'2': 's'}}))

if __name__ == '__main__':
    unittest.main()
