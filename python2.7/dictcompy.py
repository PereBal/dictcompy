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

    ·Excl: test if celem contains only one of cexcl key fields. Has no effect
           on lists.

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
    u"""
    Mark the left associated dictionary key as optional
    """
    _dispatch(expr, model[1], model[2])

def Eq(expr, model):
    u"""
    Test if the expression is equal (literaly) to the model
    """
    if expr != model[1]:
        raise DCPNoMatchException()

def Excl(expr, items):
    u"""
    Test if the listed fields are mutually exclusive on the expression and keep
    comparing through the remaining field.
    """
    r = tuple(set(items[1]) & set(expr))
    if len(r) != 1:
        raise DCPNoMatchException()
    _dispatch(expr, dict.fromkeys(r[0], items[2][r[0]]), items[3])

def In(expr, iset):
    u"""
    Test if expression is on the listed set
    """
    if expr not in iset[1]:
        raise DCPNoMatchException()

def Like(expr, pattern):
    u"""
    Match the expression field against a regex pattern to see if they come along
    """
    pat = re.compile(pattern[1])
    if not pat.match(expr):
        raise DCPNoMatchException()

def Date(expr, form):
    u"""
    Match the expression against a date format to see if it fits, aka, it's 
    equally formatted
    """
    try:
        strptime(expr, form[1])
    except ValueError:
        raise DCPNoMatchException()

def _field_type(field):
    u"""
    Returns the type of the field and the relevant part of the field itself. 
    That part it's only used in 'sets(list, set, ...)' or dicts as is the next
    part of the model that must be evaluated (specially needed with tuples
    """
    if isinstance(field, tuple):
        return (field[0], field[1])
    elif isinstance(field, type):
        return (field, field)
    else:
        return (type(field), field)

def _mandatory_key(field):
    u"""
    Test if a key is mandatory (aka, its not Opt)
    """
    return not (isinstance(field, tuple) and
                field[0] == Opt)

def _valid_type(expr, model, type_):
    u"""
    It's a warpper to allow the use of keywords to match lists, dicts, etc and
    guarantee a correct identification of matching elements even if an empty 
    tuple-list-dict is provided
    """
    # type(expr) != t it's used to avoid true matches when empty dictionary
    # or list,tuple,set is on the model
    if type(expr) != type_:
        raise DCPNoMatchException()
    else:
        # the model has a 'dict', 'list', 'set', ... keyword. The only check
        # needed is the one we made before
        return isinstance(model, type)

module = modules[__name__]
def _dispatch(expr, model, evalf):
    u"""
    This function picks the necessary evaluation/call (based on the type of the
    field) and executes it
    """
    type_, field = _field_type(field=model)

    if type_ == dict:
        if not _valid_type(expr, model, type_):
            _compare_dict(expr, field, evalf)
    elif type_ in (list, tuple, set):
        if not _valid_type(expr, model, type_):
            _compare_list(expr, field, evalf)
    elif getattr(module, type_.__name__, None):
        # evalf might be used on t to call another _dispatch with diferent
        # paramethers
        type_(expr, (model + (evalf,)))
    elif issubclass(type_, basestring):
        # empty strings evaluate falsly so if the evalf test has failed, it
        # might be due to an empty string. Thats the reason behind the 'and
        # expr' part
        if not evalf(expr, basestring) and expr:
            raise DCPNoMatchException()
    else:
        # type(expr) != t -> it's necessary to avoid true match when integer
        # and boolean (for example) are evaluated through isinstance
        if type(expr) != type_ or not evalf(expr, type_):
            raise DCPNoMatchException()

def _compare_dict(expr, model, evalf):
    u"""
    Compare expr vs model dicts field by field, recursively if needed
    """
    for k in model.keys():
        if not k in expr:
            if _mandatory_key(field=model[k]):
                raise DCPNoMatchException()
            else:
                continue

        _dispatch(expr[k], model[k], evalf)


def _compare_list(expr, model, evalf):
    u"""
    Compare expr vs model lists, tuples, sets field by field, recursively if 
    needed
    """
    if len(model) != len(expr):
        if len(model) != 1 or len(expr) < len(model):
            raise DCPNoMatchException()

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
    u"""
    Just a user defined exception class. It's used to raise internal errors
    """
    def __init__(self, *args, **kwargs):
        super(DCPException, self).__init__(*args, **kwargs)

class DCPNoMatchException(Exception):
    u"""
    Just a user defined exception class. It's used to raise a 'non matching'
    element
    """

    def __init__(self, *args, **kwargs):
        super(DCPNoMatchException, self).__init__(*args, **kwargs)

class DictComPy(object):

    def __init__(self, model, evalf=None):
        u"""
        model: dictionary or list that will be used as reference when matching.
        evalf: isinstance alternative function to apply on fields to see if 
               they match.
        """
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
        u"""
        Test if expression is equal (equality test made with the evalf) to model
        Return True on equality False otherwise
        """
        if not isinstance(expr, (dict, list)):
            raise DCPException('The expression MUST be a dictionary or a list')

        try:
            if isinstance(expr, dict):
                if not isinstance(self._model, dict):
                    raise DCPNoMatchException()
                _compare_dict(expr, self._model, self._evalf)
            else:
                if not isinstance(self._model, list):
                    raise DCPNoMatchException()
                _compare_list(expr, self._model, self._evalf)
        except DCPNoMatchException:
            return False
        else:
            return True


