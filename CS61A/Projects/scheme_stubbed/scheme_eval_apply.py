import sys
import os

from pair import *
from scheme_utils import *
from ucb import main, trace

import scheme_forms
from scheme_builtins import *

##############
# Eval/Apply #
##############
@builtin("eval", need_env=True)
def scheme_eval(expr, env, _=None):  # Optional third argument is ignored
    """Evaluate Scheme expression EXPR in Frame ENV.
    >>> expr = read_line('(+ 2 2)')
    >>> expr
    Pair('+', Pair(2, Pair(2, nil)))
    >>> scheme_eval(expr, create_global_frame())
    4
    """
    # BEGIN Problem 1/2
    "*** YOUR CODE HERE ***"
    # END Problem 1/2
    if self_evaluating(expr):
        return expr
    elif scheme_symbolp(expr):
        py_func, need_env = find_buildin_func(expr)
        if py_func == None:
            res = env.lookup(expr)
            if res is not None:
                return res
            else:
                raise SchemeError("env don't have this",expr)
        else:
            return BuiltinProcedure(py_func, need_env, expr)

    elif scheme_listp(expr):
        op = expr.first
        if scheme_symbolp(op) and op in scheme_forms.SchemeForms.keys():
            return scheme_forms.SchemeForms[op](expr.rest, env)
        proc = scheme_eval(op, env)

        def scheme_eval_helper(expr):
            return scheme_eval(expr, env)

        args = expr.rest.map(scheme_eval_helper)

        return scheme_apply(proc,args ,env)
    else:
        raise SchemeError("Error: error type")
def scheme_apply(procedure, args, env):
    """Apply Scheme PROCEDURE to argument values ARGS (a Scheme list) in
    Frame ENV, the current environment."""
    # BEGIN Problem 1/2
    "*** YOUR CODE HERE ***"


    validate_procedure(procedure)
    if isinstance(procedure, BuiltinProcedure):
        func = procedure.py_func
        arg_len = len(args)
        next_arg = args
        arglist = []
        res = None
        for _ in range(arg_len):
            arglist.append(next_arg.first)
            next_arg = next_arg.rest

        if procedure.need_env:
            arglist.append(env)
        try:
            res = func(*arglist)
        except TypeError as err:
            raise SchemeError("args num is not right")
        return res

    if isinstance(procedure, LambdaProcedure):
        formals = procedure.formals
        body = procedure.body
        new_frame = procedure.env.make_new_frame(formals, args)

        return eval_all( body, new_frame)
    if isinstance(procedure,MuProcedure):
        formals = procedure.formals
        body = procedure.body
        validate_formals(formals)
        validate_form(body,1)
        new_frame = env.make_new_frame(formals, args)
        return eval_all( body, env)

    # END Problem 1/2
def eval_all(expr, env):
    next_expr = expr
    res = None
    while next_expr != nil :
        res = scheme_eval(next_expr.first, env)
        next_expr = next_expr.rest
    return res

##################
# Tail Recursion #
##################

# Make classes/functions for creating tail recursive programs here!
# BEGIN Problem EC 1
"*** YOUR CODE HERE ***"
def find_buildin_func(name):
    for builtin_name, py_func, proc_name, need_env in BUILTINS:
        if name == builtin_name:
            return py_func, need_env
    return None, None

# END Problem EC 1


def complete_apply(procedure, args, env):
    """Apply procedure to args in env; ensure the result is not Unevaluated.
    Right now it just calls scheme_apply, but you will need to change this
    if you attempt the extra credit."""
    validate_procedure(procedure)
    # BEGIN
    return val
    # END
