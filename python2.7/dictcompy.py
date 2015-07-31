# coding: utf-8

u"""
Python dictionary/list comparator, take a look at the readme to underestand
better how it works and what it does.

Grammar & usage:
    from comparador import Comparator

    <instance_name> = Comparator()

    <instance_name>.compare(expr, model[, evalf])

    expr::= dict
         |  list

    model::= cdict
          |  clist

    evalf::= two args evaluation function 'expr operand model' to be applied on
             each field.

    cdict::= '{' key: cfield {, key: cfield} '}'
          |  '{' '}'

    clist::= '[' cfield {, cfield} ']'
          |  '[' ']'

    cfield::= ['('] python built-in basic type name [')']
           |  '(' cfunc ')'
           |  cdict
           |  clist

    cfunc::= <instance_name>.Opt, celem
          |  <instance_name>.In, cin
          |  <instance_name>.Date, cdate
          |  <instance_name>.Like, clike
          |  <instance_name>.Eq, celem
          |  <instance_name>.Excl, '(' cexcl, cexcl {, cexcl} ')', celem

    celem::= cdict
          |  clist
          |  cfield

    cin::= set of elements

    cdate::= date format (string)

    clike::= regex (string)

    cexcl::= python built-in type variable (1, 'a', True, ...)

cfunc description:
    ·Opt: mark the left-closest dictionary key appearance as optional. Has no
          effect on lists.

    ·In: test if expr key is in cin set.

    ·Date: test if expr field is cdate formatted.

    ·Like: test if expr field matches clike.

    ·Eq: test if expr field is equal to celem.

    ·Excl: test if celem contains only one of cexcl key fields. Has no effect on
           lists.

Version: 0.1

Examples:
    TODO
"""
from sys import modules
from time import strptime
import re

# TODO
def Evalf(expr, model):
    _dispatch(expr, model[2], model[1])

def Opt(expr, model):
    _dispatch(expr, model[1], model[2])

def Eq(expr, model):
    if expr != model[1]:
        raise DCPNonEqualException()

def Excl(expr, items):
    r = tuple(set(items[1]) & set(expr))
    if len(r) != 1:
        raise DCPNonEqualException()
    _dispatch(expr, dict.fromkeys(r[0], items[2][r[0]]), items[3])

def In(expr, iset):
    if expr not in iset[1]:
        raise DCPNonEqualException()

def Like(expr, pattern):
    pat = re.compile(pattern[1])
    if not pat.match(expr):
        raise DCPNonEqualException()

def Date(expr, form):
    try:
        strptime(expr, form[1])
    except ValueError:
        raise DCPNonEqualException()

def _type(field):
    if isinstance(field, tuple):
        return field[0]
    elif isinstance(field, type):
        return field
    else:
        return type(field)

def _mandatory_key(field):
    return not (isinstance(field, tuple) and
                field[0] == Opt)

module = modules[__name__]
def _dispatch(expr, model, evalf):
    t = _type(field=model)

    if t == dict:
        _compare_dict(expr, model, evalf)
    elif t in (list, tuple, set):
        _compare_list(expr, model, evalf)
    elif getattr(module, t.__name__, None):
        t(expr, (model + (evalf,)))
    # TODO
    elif isinstance(t, basestring):
        # empty strings evaluate falsly so if the evalf test has failed, it
        # might be due to an empty string. Thats the reason behind the 'and
        # expr' part
        if not evalf(expr, basestring) and expr:
            raise DCPNonEqualException()
    else:
        if not evalf(expr, t):
            raise DCPNonEqualException()

def _compare_dict(expr, model, evalf):
    for k in model.keys():
        if not k in expr:
            if _mandatory_key(field=model[k]):
                raise DCPNonEqualException()
            else:
                continue

        _dispatch(expr[k], model[k], evalf)


def _compare_list(expr, model, evalf):
    if len(model) != len(expr):
        if len(model) != 1:
            raise DCPNonEqualException()

        iterset = expr
        ITERINC = 0
    else:
        iterset = model
        ITERINC = 1

    model_key = 0
    for expr_key in range(model_key, len(iterset)):
        _dispatch(expr[expr_key], model[model_key], evalf)
        model_key = model_key + ITERINC

class DCPException(Exception):

    def __init__(self, *args, **kwargs):
        super(DCPException, self).__init__(*args, **kwargs)

class DCPNonEqualException(Exception):

    def __init__(self, *args, **kwargs):
        super(DCPNonEqualException, self).__init__(*args, **kwargs)

class DictComPy(object):

    def __init__(self, model, evalf=None):
        super(DictComPy, self).__init__()

        if evalf:
            self._evalf = evalf
        else:
            self._evalf = isinstance

        if type(model) not in (dict, list):
            raise DCPException('The model MUST be a dictionary or a list')

        self._model = model

    def __unicode__(self):
        return unicode(self._model).encode('utf-8')

    def __str__(self):
        return unicode(self._model).encode('utf-8')

    @property
    def model(self):
        return self._model

    def match(self, expr):
        if not isinstance(expr, (dict, list)):
            raise DCPException('The expression MUST be a dictionary or a list')

        try:
            if isinstance(expr, dict):
                if not isinstance(self._model, dict):
                    raise DCPNonEqualException()
                _compare_dict(expr, self._model, self._evalf)
            else:
                if not isinstance(self._model, list):
                    raise DCPNonEqualException()
                _compare_list(expr, self._model, self._evalf)
        except DCPNonEqualException:
            return False
        else:
            return True


