# TODO
# model: (int, 1) -> funciona com toca. Les tuples son especials x)
# faltaria afegir un parseig del model
import unittest

from dictcompy import (DictComPy, Opt, Eq, Excl, In, Like, Date, Or_None,
                       Or_Empty)

MODELS = {
    'int': [{'a': int}],
    'float': [{'a': float}],
    'complex': [{'a': complex}],
    'bool': [{'a': bool}],
    'str': [{'a': str}],
    'list': [{'a': list}, {'a': []}, {'a': (list, [])}, {'a': [int]},
             {'a': [int, str, bool]}],
    'tuple': [{'a': tuple}, {'a': (tuple, (int,))},
              {'a': (tuple, (int,str,bool))}],
    'dict': [],
}

class TestDictComPy(unittest.TestCase):

    def test_plain_int(self):
        dcp = DictComPy(model=MODELS['int'][0])
        self.assertFalse(dcp.match(expr={'b': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': True}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 'as'}))
        self.assertTrue(dcp.match(expr={'a': 1}))
        self.assertTrue(dcp.match(expr={'a': 0}))

    def test_plain_float(self):
        dcp = DictComPy(model=MODELS['float'][0])
        self.assertFalse(dcp.match(expr={'b': 1.0}))
        self.assertFalse(dcp.match(expr={'a': 0}))
        self.assertFalse(dcp.match(expr={'a': True}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 'as'}))
        self.assertTrue(dcp.match(expr={'a': 1.0}))

    def test_plain_complex(self):
        dcp = DictComPy(model=MODELS['complex'][0])
        c = complex(1, 2)
        self.assertFalse(dcp.match(expr={'b': c}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': True}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 'as'}))
        self.assertTrue(dcp.match(expr={'a': c}))

    def test_plain_bool(self):
        dcp = DictComPy(model=MODELS['bool'][0])
        self.assertFalse(dcp.match(expr={'b': True}))
        self.assertFalse(dcp.match(expr={'a': 0}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 'as'}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertTrue(dcp.match(expr={'a': True}))
        self.assertTrue(dcp.match(expr={'a': False}))

    def test_plain_string(self):
        dcp = DictComPy(model=MODELS['str'][0])
        self.assertFalse(dcp.match(expr={'b': u'a'}))
        self.assertFalse(dcp.match(expr={'a': 23}))
        self.assertFalse(dcp.match(expr={'a': True}))
        self.assertTrue(dcp.match(expr={'a': 'a'}))
        self.assertTrue(dcp.match(expr={'a': u'a'}))
        self.assertTrue(dcp.match(expr={'a': u''}))
        self.assertTrue(dcp.match(expr={'a': ''}))

    def test_plain_list(self):
        dcp = DictComPy(model=MODELS['list'][0])
        self.assertFalse(dcp.match(expr={'b': []}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertTrue(dcp.match(expr={'a': []}))
        self.assertTrue(dcp.match(expr={'a': [1]}))
        self.assertTrue(dcp.match(expr={'a': [1, '1021', True]}))

        dcp = DictComPy(model=MODELS['list'][1])
        self.assertFalse(dcp.match(expr={'b': []}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': [1]}))
        self.assertFalse(dcp.match(expr={'a': [1, '1021', True]}))
        self.assertTrue(dcp.match(expr={'a': []}))

        dcp = DictComPy(model=MODELS['list'][2])
        self.assertFalse(dcp.match(expr={'b': []}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': [1]}))
        self.assertFalse(dcp.match(expr={'a': [1, '1021', True]}))
        self.assertTrue(dcp.match(expr={'a': []}))

        dcp = DictComPy(model=MODELS['list'][3])
        self.assertFalse(dcp.match(expr={'b': [1]}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': []}))
        self.assertFalse(dcp.match(expr={'a': [1, '1021', True]}))
        self.assertTrue(dcp.match(expr={'a': [1]}))
        self.assertTrue(dcp.match(expr={'a': [1, 2, 3]}))

        dcp = DictComPy(model=MODELS['list'][4])
        self.assertFalse(dcp.match(expr={'b': []}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': []}))
        self.assertFalse(dcp.match(expr={'a': [1]}))
        self.assertFalse(dcp.match(expr={'a': [1, '1021', True, 1.0]}))
        self.assertTrue(dcp.match(expr={'a': [1, '1021', True]}))

    def test_plain_tuple(self):
        dcp = DictComPy(model=MODELS['tuple'][0])
        self.assertFalse(dcp.match(expr={'b': ()}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertTrue(dcp.match(expr={'a': ()}))
        self.assertTrue(dcp.match(expr={'a': (1,)})) # 1, <-- common mistake
        self.assertTrue(dcp.match(expr={'a': (1, '1021', True)}))

        dcp = DictComPy(model=MODELS['tuple'][1]) # ',' <--
        self.assertFalse(dcp.match(expr={'b': (1,)}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': ()}))
        self.assertFalse(dcp.match(expr={'a': (1, '1021', True)}))
        self.assertFalse(dcp.match(expr={'a': ('',)}))
        self.assertTrue(dcp.match(expr={'a': (1,)}))
        self.assertTrue(dcp.match(expr={'a': (1, 2, 3)}))

        dcp = DictComPy(model=MODELS['tuple'][2]) # ',' <--
        self.assertFalse(dcp.match(expr={'b': (1,)}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': ()}))
        self.assertFalse(dcp.match(expr={'a': (1,)}))
        self.assertFalse(dcp.match(expr={'a': (1, 2, 3)}))
        self.assertFalse(dcp.match(expr={'a': (1, '1021', True, 1.0)}))
        self.assertTrue(dcp.match(expr={'a': (1, '1021', True)}))

    def test_nested_int(self):
        dcp = DictComPy({'a': {'b': int}})
        self.assertFalse(dcp.match(expr={'b': {'b': 1}}))
        self.assertFalse(dcp.match(expr={'a': {'a': 1}}))
        self.assertFalse(dcp.match(expr={'a': {'b': ''}}))
        self.assertTrue(dcp.match(expr={'a': {'b': 1}}))

    def test_In(self):
        dcp = DictComPy({'a': (In, range(0,5,2))})
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 10}))
        self.assertTrue(dcp.match(expr={'a': 2}))

    def test_Like(self):
        dcp = DictComPy({'a': (Like, '\d,\w+')})
        self.assertFalse(dcp.match(expr={'a': '1,'}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': '10'}))
        self.assertTrue(dcp.match(expr={'a': '1,0102dsada_dede'}))

    def test_Date(self):
        dcp = DictComPy({'a': (Date, '%Y-%d-%m')})
        self.assertFalse(dcp.match(expr={'a': '2015-02-31'}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': '2015-32-01'}))
        self.assertTrue(dcp.match(expr={'a': '2015-30-01'}))

    def test_Excl(self):
        dcp = DictComPy({'a': (Excl, ('1', '2'), {'1': int, '2': str})})
        self.assertFalse(dcp.match(expr={'a': {'1': 's'}}))
        self.assertFalse(dcp.match(expr={'a': {'2': 1}}))
        self.assertFalse(dcp.match(expr={'a': {'1': 1, '2': 's'}}))
        self.assertTrue(dcp.match(expr={'a': {'1': 1}}))
        self.assertTrue(dcp.match(expr={'a': {'2': 's'}}))


    def test_Opt(self):
        dcp = DictComPy({'a': (Opt, int)})
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': 's'}))
        self.assertFalse(dcp.match(expr={'a': True}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertTrue(dcp.match(expr={'a': 1}))
        self.assertTrue(dcp.match(expr={'b': 1}))

    def test_Eq(self):
        dcp = DictComPy({'a': (Eq, 3)})
        self.assertFalse(dcp.match(expr={'a': 1}))
        self.assertFalse(dcp.match(expr={'a': 4}))
        self.assertTrue(dcp.match(expr={'a': 3}))

        dcp = DictComPy({'a': (Eq, dict)})
        self.assertFalse(dcp.match(expr={'a': {}}))
        self.assertFalse(dcp.match(expr={'a': list}))
        self.assertTrue(dcp.match(expr={'a': dict}))

    def test_Or_None(self):
        dcp = DictComPy({'a': (Or_None, int)})
        self.assertFalse(dcp.match(expr={'b': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': False}))
        self.assertTrue(dcp.match(expr={'a': None}))
        self.assertTrue(dcp.match(expr={'a': 1}))

        dcp = DictComPy({'a': (Or_None, (tuple, int))})
        self.assertFalse(dcp.match(expr={'b': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': False}))
        self.assertFalse(dcp.match(expr={'a': []}))
        self.assertFalse(dcp.match(expr={'a': None}))
        self.assertFalse(dcp.match(expr={'a': ('df',)}))
        self.assertTrue(dcp.match(expr={'a': ()}))
        self.assertTrue(dcp.match(expr={'a': (1,)}))

    def test_Or_Empty(self):
        dcp = DictComPy({'a': (Or_Empty, {'b': int})})
        self.assertFalse(dcp.match(expr={'b': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': False}))
        self.assertFalse(dcp.match(expr={'a': []}))
        self.assertFalse(dcp.match(expr={'a': None}))
        self.assertFalse(dcp.match(expr={'a': ('df',)}))
        self.assertTrue(dcp.match(expr={'a': {}}))
        self.assertTrue(dcp.match(expr={'a': {'b': 1}}))

        dcp = DictComPy({'a': (Or_Empty, [int])})
        self.assertFalse(dcp.match(expr={'b': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': False}))
        self.assertFalse(dcp.match(expr={'a': None}))
        self.assertFalse(dcp.match(expr={'a': ['df']}))
        self.assertTrue(dcp.match(expr={'a': []}))
        self.assertTrue(dcp.match(expr={'a': [1]}))

        """ Failing
        dcp = DictComPy({'a': (Or_Empty, (tuple, int))})
        self.assertFalse(dcp.match(expr={'b': 1}))
        self.assertFalse(dcp.match(expr={'a': 1.0}))
        self.assertFalse(dcp.match(expr={'a': ''}))
        self.assertFalse(dcp.match(expr={'a': False}))
        self.assertFalse(dcp.match(expr={'a': []}))
        self.assertFalse(dcp.match(expr={'a': None}))
        self.assertFalse(dcp.match(expr={'a': ('df',)}))
        self.assertTrue(dcp.match(expr={'a': ()}))
        self.assertTrue(dcp.match(expr={'a': (1,)}))
        """

if __name__ == '__main__':
    unittest.main()
