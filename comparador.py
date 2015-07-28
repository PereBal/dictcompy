# coding: utf-8

u"""
Python dictionary/list comparator, take a look at the readme to underestand
better how it works and what it does.

Grammar & usage:
    from comparador import Komparator

    <instance_name> = Komparator()

    <instance_name>.comparar(dst, model[, evalf])

    dst::= dict | list

    model::= kdict |  klist

    evalf::= two args evaluation function 'dst operand model' to be applied on
             each field.

    kdict::= '{' key: kfield {, key: kfield} '}'
          |  '{' '}'

    klist::= '[' kfield {, kfield} ']'
          |  '[' ']'

    kfield::= ['('] python built-in basic type name [')']
           |  '(' kfunc ')'
           |  kdict
           |  klist

    kfunc::= <instance_name>.Opt, kelem
          |  <instance_name>.In, kin
          |  <instance_name>.Date, kdate
          |  <instance_name>.Like, klike
          |  <instance_name>.Val, kelem [, evalf]
          |  <instance_name>.Excl, '(' kexcl, kexcl {, kexcl} ')', kelem

    kelem::= kdict
          |  klist
          |  kfield

    kin::= set of elements

    kdate::= date format (string)

    klike::= regex (string)

    kexcl::= python built-in type variable (1, 'a', True, ...)

Kfunc description:
    ·Opt: mark the left-closest dictionary key appearance as optional. Has no
          effect on lists.

    ·In: test if dst key is in kin set.

    ·Date: test if dst field is kdate formatted.

    ·Like: test if dst field matches klike.

    ·Val: test (with evalf or equality test if, evalf not provided) if dst field
          is equal to kelem.

    ·Excl: test if kelem contains only one of kexcl key fields. Has no effect on
           lists.

Version: 0.1

Examples:
    TODO
"""
# TODO: 
#   -per millorar els missatges a llistes-> pila que guarda la darrera key
#   -canviar els prints per excepcions i montar-ho perque executant cada
#   subfunció es pugui saber si algo ha anat malament.
#   -afegir soport al multi{threading, processing}
#   -afegir soport a les tuples com a elements
import re
from time import strftime
class Komparator(object):

    def __init__(self, *args, **kwargs):
        super(Komparator, self).__init__(*args, **kwargs)


    def __decompose(self, v):
        if isinstance(v, tuple):
            t = v[0]
            if len(v) > 1:
                v = v[1]
        else:
            t = v

        return (t, v)


    def __excl(self, resp, excl):
        err = None
        for k in excl:
            if k in resp:
                if err:
                    print(u'' + str(k) + ' and ' + str(err) + ' are not'
                    + ' exclusive')
                    return None
                else:
                    err = str(k)
        return 1


    def __dispatch(self, resp, kwargs, t, k, v):
        err = False
        if t == dict:
            self.__comparar_dict(resp[k], v)
        elif t == list:
            self.__comparar_list(resp[k], v)
        elif t == str or t == unicode:
            # el orden es este por python 2 & roiback
            err = not self.evalf(resp[k], unicode)
            if err:
                err = not self.evalf(resp[k], str)
        elif getattr(self, t.__name__, None): # es una de las funciones
            err = not t(resp[k], kwargs[k])
        else:
            err = not self.evalf(resp[k], v)

        return err

    def __comparar_dict(self, resp, kwargs, excl=None):
        if excl:
            if not self.__excl(resp, excl):
                return None

        for k,v in kwargs.iteritems():
            if not k in resp:
                if isinstance(v, tuple) and v[0] != self.Opt:
                    print(u'key ' + str(k) + ' not in reponse')
                return None

            t, v = self.__decompose(v)

            if self.__dispatch(resp, kwargs, t, k, v):
                print(u'{' + str(k) + ',' + str(resp[k]) + '} non conformant'
                        + ' with expected {' + str(k) + ',' + str(v) + '}')
                return None

        return 1


    def __comparar_list(self, resp, kwargs):
        if len(kwargs) != len(resp):
            if len(kwargs) != 1:
                print(u'' + str(kwargs) + ' and ' + str(resp) + ' have different'
                      + ' lenghts')
                return None

            iterset = resp
        else:
            iterset = kwargs

        for k in range(0, len(iterset)):
            v = iterset[k]

            t, v = self.__decompose(v)

            if self.__dispatch(resp, kwargs, t, k, v):
                print(u'resp[' + str(k) + ']:(' + str(resp[k]) + ') non '
                      + 'conformant with expected kwargs[' + str(k) + ']:('
                      + str(v) + ')')
                return None

        return 1

    def Opt(self, resp, kwargs):
        return self.evalf(resp, kwargs[1])

    def Value(self, resp, kwargs):
        if len(kwargs) == 3:
            return kwargs[2](resp, kwargs[1])
        else:
            return resp == kwargs[1]

    def Excl(self, resp, items):
        return self.__comparar_dict(resp, items[2], items[1])

    def In(self, resp, iset):
        return resp in iset[1]

    # TODO
    def Like(self, resp, pattern):
        return re.match(u''+pattern[1], resp)

    # TODO
    def Date(self, resp, form):
        try:
            strftime(resp, form[1])
        except ValueError:
            return False
        else:
            return True

    def comparar(self, resp, kwargs, evalf=None):
        if not evalf:
            evalf = lambda a,b: isinstance(a,b)

        self.evalf = evalf
        if isinstance(kwargs, dict):
            self.__comparar_dict(resp, kwargs)
        else: # it's a trap i meaaan a list
            self.__comparar_list(resp, kwargs)
