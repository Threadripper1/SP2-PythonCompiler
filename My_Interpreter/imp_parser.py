
from imp_lexer import *
from combinators import *
from imp_ast import *
from functools import *
import sys

# Basic parsers
def keyword(kw):
    return Reserved(kw, RESERVED)

num = Tag(INT) ^ (lambda i: int(i, 16))
id = Tag(ID)

# Top level parser
def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast

def parser():
    return Phrase(stmt_list())

# Statements
def stmt_list():
    separator = keyword('\n') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)

def print_stmt():
    def process(parsed):
        (((_, _), exp), _) = parsed
        return PrintStatement(exp)
    return keyword("print") + keyword("(") + aexp() + keyword(")") ^ process

def stmt():
    return assign_stmt() | \
           if_stmt()     | \
           while_stmt()  | \
           print_stmt()  | \
           function_stmt() | \
           ternary_stmt() | \
           xor_stmt() | \
           for_stmt() | \
           range_stmt()

def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)
    return id + keyword('=') + aexp() ^ process

def xor_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return XorStatement(name, exp)
    return aexp() + keyword('^=') + aexp() ^ process

def function_stmt():
    def process(parsed):
        (((((((((_, _), _), _), _), _), body), _), _), result) = parsed
        return DefStatement(result, body)
    return keyword('def') + keyword("main") + keyword("(") + keyword(")") + keyword(":") + keyword("\n")  + \
           Lazy(stmt_list) + keyword("\n") + \
           keyword("return") + aexp() ^ process

def if_stmt():
    def process(parsed):
        ((((((((_, _), condition), _), _), _), true_stmt), _), false_parsed) = parsed
        if false_parsed:
            ((_, _), false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfStatement(condition, true_stmt, false_stmt)
    return keyword('if') + keyword("(") + bexp() + keyword(")") +\
           keyword(':') + keyword("\n") +  Lazy(stmt_list) + keyword("\n") + \
           Opt(keyword('else') + keyword(':') + keyword("\n") + Lazy(stmt_list)) ^ process

def ternary_stmt():
    def process(parsed):
        (((true_stmt, _), condition), false_parsed) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return TernaryStatement(condition, true_stmt, false_stmt)
    return aexp() + keyword("if") + bexp() + Opt(keyword("else") + aexp()) ^ process

def while_stmt():
    def process(parsed):
        ((((_, condition), _), _), body)  = parsed
        return WhileStatement(condition, body)
    return keyword('while') + bexp() + \
           keyword(":") + keyword('\n') + Lazy(stmt_list) ^ process

def range_stmt():
    def process(parsed):
        (((((_, _), index1), _), index2), _) = parsed
        return RangeStatement(index2, index2)
    return keyword("range") + keyword("(")+ aexp() + keyword(",") + aexp() + keyword(")")  ^ process

def for_stmt():
    def process(parsed):
        (((((((((((_, counter), _), _), _), index1), _), index2), _), _), _), body) = parsed
        return ForStatement(counter, index1, index2, body)
    return keyword("for") + aexp() + keyword("in") + keyword("range") + keyword("(") + \
           aexp() + keyword(",") + aexp() + keyword(")") + keyword(":") + \
           keyword("\n") + Lazy(stmt_list) ^ process

# Boolean expressions
def bexp():
    return precedence(bexp_term(),
                      bexp_precedence_levels,
                      process_logic)

def bexp_term():
    return bexp_not()   | \
           bexp_relop() | \
           bexp_group()

def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotBexp(parsed[1]))

def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop

def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group

# Arithmetic expressions
def aexp():
    return precedence(aexp_term(),
                      aexp_precedence_levels,
                      process_binop)

def aexp_term():
    return aexp_value() | aexp_group()

def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group

def aexp_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id  ^ (lambda v: VarAexp(v)))

# An IMP-specific combinator for binary operator expressions (aexp and bexp)
def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine
    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser

"""# Unary operators

def unary():
    return precedence(unary_term(),
                      unary_precedence_levels,
                      process_unary)

def unary_term():
    return unary_value() | unary_group()

def unary_value():
    return (num ^ (lambda i: IntAexp(i))) | \
           (id ^  (lambda v: VarAexp(v)))

def unary_group():
    return keyword('(') + Lazy(unary) + keyword(')') ^ process_group

def process_unary(op):
    return lambda r: BinopAexp(op, r)
"""
# Miscellaneous functions for binary and relational operators
def process_binop(op):
    return lambda l, r: BinopAexp(op, l, r)

def process_relop(parsed):
    ((left, op), right) = parsed
    return RelopBexp(op, left, right)

def process_logic(op):
    if op == 'and':
        return lambda l, r: AndBexp(l, r)
    elif op == 'or':
        return lambda l, r: OrBexp(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)

def process_group(parsed):
    ((_, p), _) = parsed
    return p

def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser

# Operator keywords and precedence levels
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
    ['~', '^']
]

unary_precedence_levels = [['~']]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]
