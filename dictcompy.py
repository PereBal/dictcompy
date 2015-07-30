# coding: utf-8

u"""
Python dictionary/list comparator, take a look at the readme to underestand
better how it works and what it does.

Grammar & usage:
    from comparador import Comparator

    <instance_name> = Comparator()

    <instance_name>.compare(dst, model[, evalf])

    dst::= dict

    model::= cdict

    evalf::= two args evaluation function 'dst operand model' to be applied on
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
          |  <instance_name>.Val, celem [, evalf]
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

    ·In: test if dst key is in cin set.

    ·Date: test if dst field is cdate formatted.

    ·Like: test if dst field matches clike.

    ·Val: test (with evalf or equality test if, evalf not provided) if dst field
          is equal to celem.

    ·Excl: test if celem contains only one of cexcl key fields. Has no effect on
           lists.

Version: 0.1

Examples:
    TODO
"""
# TODO: 
#   -afegir soport al multi{threading, processing}
import sys
import re
from time import strptime
from types import StringTypes
from inspect import isclass

# TODO
def Evalf(resp, kwargs):
    return kwargs[2](resp, kwargs[1])

# TODO
def Opt(resp, kwargs):
    return kwargs[2](resp, kwargs[1])

# TODO
def Value(resp, kwargs):
    if len(kwargs) == 4:
        return kwargs[2](resp, kwargs[1])
    else:
        return resp == kwargs[1]

def Excl(resp, items):
    r = tuple(set(items[1]) & set(resp))
    if len(r) != 1:
        return False
    return _compare_dict(resp, dict.fromkeys(r[0], items[2][r[0]]), items[3])

def In(resp, iset):
    return resp in iset[1]

def Like(resp, pattern):
    pat = re.compile(pattern[1])
    return pat.match(resp)

def Date(resp, form):
    try:
        strptime(resp, form[1])
    except ValueError:
        return False
    else:
        return True

def _decompose(v):
    if isinstance(v, tuple):
        t = v[0]
        if len(v) > 1:
            v = v[1]
    else:
        ta = type(v)
        t = v if ta == type else ta

    return (t, v)

module = sys.modules[__name__]
def _dispatch(resp, kwargs, evalf, t, v):
    ok = False
    if t == dict:
        ok = _compare_dict(resp, v, evalf)
    elif t in (list, tuple, set):
        ok = _compare_list(resp, v, evalf)
    elif (isclass(t) and issubclass(t, StringTypes)) or isinstance(t, StringTypes):
        ok = evalf(resp, StringTypes)
    elif getattr(module, t.__name__, None):
        ok = t(resp, (kwargs + (evalf,)))
    else:
        ok = evalf(resp, t)

    return ok

def _compare_dict(resp, kwargs, evalf):
    for k,v in kwargs.iteritems():
        if not k in resp:
            if not (isinstance(v, tuple) and v[0] == Opt):
                return False
            continue

        t, v = _decompose(v)

        if not _dispatch(resp[k], kwargs[k], evalf, t, v):
            return False

    return True


def _compare_list(resp, kwargs, evalf):
    # allow 'key: list'
    try:
        if len(kwargs) != len(resp):
            if len(kwargs) != 1:
                return False
            iterset = resp
        else:
            iterset = kwargs
    except AttributeError:
        return type(resp) == kwargs
    else:
        # allow 'key: [1, ...]' and 'key: [1] for each elem of resp'
        for k in range(0, len(iterset)):
            v = iterset[k]

            t, v = _decompose(v)

            if not _dispatch(resp[k], kwargs[k], evalf, t, v):
                return False

        return True

class DCPException(Exception):

    def __init__(self, *args, **kwargs):
        super(DCPException, self).__init__()

class DictComPy(object):

    def __init__(self, model, evalf=None):
        super(DictComPy, self).__init__()
        if not evalf:
            evalf = lambda a,b: isinstance(a,b)
        self.evalf = evalf

        if not isinstance(model, dict):
            raise DCPException('The model MUST be a dictionary')

        self.model = model

    def match(self, resp):
        if isinstance(resp, dict):
            return _compare_dict(resp, self.model, self.evalf)

        else:
            raise DCPException('The response MUST be a dictionary')

