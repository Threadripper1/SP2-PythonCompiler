
import sys
from imp_lexer import *

if __name__ == '__main__':
   #filename = sys.argv[1]
    file = open('6-12-Python-IO-83-Kolomiets.imp')
    characters = file.read()
    file.close()
    tokens = imp_lex(characters)
    for token in tokens:
        print (token)
