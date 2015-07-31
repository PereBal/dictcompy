import unittest

import dictcompy as dcm

class TestDictComPy(unittest.TestCase):
    def test_basics(self):
        cm = dcm.DictComPy({'a': int})
        self.assertFalse(cm.match({'b': 1}))
        self.assertFalse(cm.match({'a': 1.0}))
        self.assertTrue(cm.match({'a': 1}))

        cm = dcm.DictComPy({'a': str})
        self.assertFalse(cm.match({'b': u'a'}))
        self.assertFalse(cm.match({'a': 23}))
        self.assertTrue(cm.match({'a': 'a'}))
        self.assertTrue(cm.match({'a': u'a'}))

        cm = dcm.DictComPy({'a': {'b': int}})
        self.assertFalse(cm.match({'b': {'b': 1}}))
        self.assertFalse(cm.match({'a': {'a': 1}}))
        self.assertFalse(cm.match({'a': {'b': ''}}))
        self.assertTrue(cm.match({'a': {'b': 1}}))

        cm = dcm.DictComPy({'a': list})
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': 1}))
        self.assertFalse(cm.match({'a': {}}))
        self.assertFalse(cm.match({'a': [1]}))
        self.assertTrue(cm.match({'a': []}))

    def test_In(self):
        cm = dcm.DictComPy({'a': (dcm.In, range(0,5,2))})
        self.assertFalse(cm.match({'a': 1}))
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': 10}))
        self.assertTrue(cm.match({'a': 2}))

    def test_Like(self):
        cm = dcm.DictComPy({'a': (dcm.Like, '\d,\w+')})
        self.assertFalse(cm.match({'a': '1,'}))
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': '10'}))
        self.assertTrue(cm.match({'a': '1,0102dsada_dede'}))

    def test_Date(self):
        cm = dcm.DictComPy({'a': (dcm.Date, '%Y-%d-%m')})
        self.assertFalse(cm.match({'a': '2015-02-31'}))
        self.assertFalse(cm.match({'a': ''}))
        self.assertFalse(cm.match({'a': '2015-32-01'}))
        self.assertTrue(cm.match({'a': '2015-30-01'}))

    def test_Excl(self):
        cm = dcm.DictComPy({'a': (dcm.Excl, ('1', '2'), {'1': int, '2': str})})
        self.assertFalse(cm.match({'a': {'1': 's'}}))
        self.assertFalse(cm.match({'a': {'2': 1}}))
        self.assertFalse(cm.match({'a': {'1': 1, '2': 's'}}))
        self.assertTrue(cm.match({'a': {'1': 1}}))
        self.assertTrue(cm.match({'a': {'2': 's'}}))


    def test_Opt(self):
        cm = dcm.DictComPy({'a': (dcm.Opt, int)})
        self.assertTrue(cm.match({'a': 1}))
        self.assertTrue(cm.match({'b': 1}))

    def test_Eq(self):
        cm = dcm.DictComPy({'a': (dcm.Eq, 3)})
        self.assertFalse(cm.match({'a': 1}))
        self.assertFalse(cm.match({'a': 4}))
        self.assertTrue(cm.match({'a': 3}))

if __name__ == '__main__':
    unittest.main()
