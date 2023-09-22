from scheme_eval_apply import *
from scheme_utils import *
from scheme_classes import *
from scheme_builtins import *

#################
# Special Forms #
#################

"""
How you implement special forms is up to you. We recommend you encapsulate the
logic for each special form separately somehow, which you can do here.
"""

# BEGIN PROBLEM 2/3
"*** YOUR CODE HERE ***"
def do_define_form(expr,env):
    validate_form(expr,2)
    sig = expr.first
    if scheme_symbolp(sig):
        res = scheme_eval(expr.rest.first, env)
        env.bindings[sig] = res
        return sig
    elif isinstance(sig, Pair):
        name = sig.first
        formals = sig.rest
        body = expr.rest
        proc = LambdaProcedure(formals, body, env)
        env.bindings[name] = proc
        return name
    else:
        raise SchemeError("Error: non-symbol:",sig)

def do_if_form(expr,env):
    validate_form(expr,2)
    predicate = expr.first
    consequent = expr.rest.first
    alternative = expr.rest.rest
    res= scheme_eval(predicate, env)
    if res is not False :
        return scheme_eval(consequent, env)
    elif len(expr) == 3:
        return scheme_eval(alternative.first, env)
    return None

def do_and_form(expr,env):
    next_expr = expr
    res = True
    while next_expr != nil :
        res = scheme_eval(next_expr.first, env)
        if res is False:
            return res
        next_expr = next_expr.rest
    return res

def do_cond_form(expr,env):
    next_expr = expr
    res = True
    while next_expr != nil :
        clause = next_expr.first
        if clause.first == "else":
            return scheme_eval(clause.rest.first, env)
        test = clause.first
        exp =clause.rest
        res = scheme_eval(test, env)
        if res is not False:
            if exp == nil:
                return res
            return do_begin_form(exp, env)

        next_expr = next_expr.rest
    return None

def do_or_form(expr,env):
    next_expr = expr
    res = False
    while next_expr != nil :
        res = scheme_eval(next_expr.first, env)
        if res is not False:
            return res
        next_expr = next_expr.rest
    return res

def do_let_form(expr,env):
    bindings = expr.first
    next_bindings = bindings
    new_frame = Frame(env)
    while next_bindings!= nil:
        binding = next_bindings.first
        next_bindings = next_bindings.rest
        validate_form(binding,2)
        if len(binding) == 2 and scheme_symbolp(binding.first) :
            new_frame.define(binding.first, scheme_eval(binding.rest.first,env) )
        else:
            raise SchemeError("Let parameter num error")

    body = expr.rest
    return do_begin_form(body, new_frame)

def do_begin_form(expr,env):
    next_expr = expr
    res = None
    while next_expr != nil :
        res = scheme_eval(next_expr.first, env)
        next_expr = next_expr.rest
    return res

def do_lambda_form(expr,env):
    formals = expr.first
    body = expr.rest
    validate_formals(formals)
    validate_form(body, 1)
    proc = LambdaProcedure(formals, body, env) 
    return proc

def do_quote_form(expr,env):
    return expr.first

def do_quasiquote_form(expr,env):
    return NotImplemented

def do_unquote_form(expr,env):
    return NotImplemented

def do_mu_form(expr,env):
    param = expr.first
    body = expr.rest
    validate_form(body, 1)
    muproc = MuProcedure(param, body)
    return muproc

def do_define_macro_form(expr,env):
    return NotImplemented

def do_expect_form(expr,env):
    return NotImplemented

def do_unquote_splicing_form(expr,env):
    return NotImplemented

def do_delay_form(expr,env):
    return NotImplemented

def do_cons_stream_form(expr,env):
    return NotImplemented

def do_set_form(expr,env):
    return NotImplemented


SchemeForms = {'define': do_define_form,
               'if': do_if_form,
               'and': do_and_form,
               'cond': do_cond_form,
               'or': do_or_form,
               'let': do_let_form,
               'begin': do_begin_form,
               'lambda': do_lambda_form,
               'quote': do_quote_form,
               'quasiquote': do_quasiquote_form,
               'unquote': do_unquote_form,
               'mu': do_mu_form,
               'define-marco': do_define_macro_form,
               'expect': do_expect_form,
               'unquote-splicing': do_unquote_splicing_form,
               'delay': do_delay_form}
# END PROBLEM 2/3
