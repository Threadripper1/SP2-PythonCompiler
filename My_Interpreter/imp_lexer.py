
import lexer

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'
HEX      = 'HEX'

token_exprs = [
    (r'#[^\n]*',               None),
    (r'[\t]+',                 None),
    (r'[ \t]+',                None),
    (r'[#]+',                  None),
    (r'[ \n]',                 RESERVED),
    (r'\=',                    RESERVED),
    (r'\(',                    RESERVED),
    (r'\)',                    RESERVED),
    (r':',                     RESERVED),
    (r'\+',                    RESERVED),
    (r'-',                     RESERVED),
    (r'\*',                    RESERVED),
    (r'/',                     RESERVED),
    (r'<=',                    RESERVED),
    (r'<',                     RESERVED),
    (r'>=',                    RESERVED),
    (r'>',                     RESERVED),
    (r'!=',                    RESERVED),
    (r'\^=',                   RESERVED),
    (r',',                     RESERVED),
    (r'=',                     RESERVED),
    (r'\^',                    RESERVED),
    (r'main',                  RESERVED),
    (r'def',                   RESERVED),
    (r'return',                RESERVED),
    (r'and',                   RESERVED),
    (r'or',                    RESERVED),
    (r'~',                     RESERVED),
    (r'not',                   RESERVED),
    (r'if',                    RESERVED),
    (r'else',                  RESERVED),
    (r'while',                 RESERVED),
    (r'for',                   RESERVED),
    (r'in',                    RESERVED),
    (r'\,',                    RESERVED),
    (r'range',                 RESERVED),
    (r'print',                 RESERVED),
    (r'True',                  RESERVED),
    (r'False',                 RESERVED),
    (r'None',                  RESERVED),
    (r'"',                     RESERVED),
    (r'.([0x0-9A-Fa-f]+)',     INT),
    (r'[0-9]+',                INT),
    (r'[A-Za-z][A-Za-z0-9_]*', ID),
]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs)
