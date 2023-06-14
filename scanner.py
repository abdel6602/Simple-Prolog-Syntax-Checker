from enum import Enum
import re
from Token import Token
from fileScanner import scan


# directory_flag = str(input("Please Enter the Directory:"))
# lexemes = []
#
# match directory_flag:
#     case '1':
#         lexemes = scan('example.txt')
#     case '2':
#         lexemes = scan('example2.txt')
#     case '3':
#         lexemes = scan('example3.txt')
#     case _:
#         lexemes = scan('example4.txt')


tokens = []
errors = []

#----- NEW CODE --------
class TokenType(Enum):
    PREDICATE_KEYWORD = 1
    CLAUSES_KEYWORD = 2
    GOAL_KEYWORD = 3
    AND_OP = 4
    OR_OP = 5
    READ_LN_KEYWORD = 6
    READ_INT_KEYWORD = 7
    READ_CHAR_KEYWORD = 8
    WRITE_KEYWORD = 9
    LESS_THAN_OP = 10
    LESS_THAN_EQUAL_OP = 11
    GREATER_THAN_OP = 12
    GREATER_THAN_EQUAL_OP = 13
    EQUAL_OP = 14
    ANGLED_BRACKETS_OP = 15
    PLUS_OP = 16
    MINUS_OP = 17
    MULTIPLY_OP = 18
    DIVIDE_OP = 19
    UNDERSCORE_OP = 20
    VARIABLE = 21
    DOT_OP = 22
    OPEN_BRACKET = 23
    CLOSE_BRACKET = 24
    PREDICATE_NAME = 25
    INTEGER_DATA_TYPE = 26
    SYMBOL_DATA_TYPE = 27
    STRING_DATA_TYPE = 28
    CHAR_DATA_TYPE = 29
    REAL_DATA_TYPE = 30
    INTEGER_VALUE = 31
    REAL_VALUE = 32
    STRING_VALUE = 33
    IDENTIFIER = 34
    ASSIGNMENT_OP = 35
    SYMBOL_VALUE = 36
    ERROR = 37


# Reserved word Dictionary
reserved_words = {
    "predicates": TokenType.PREDICATE_KEYWORD,
    "clauses": TokenType.CLAUSES_KEYWORD,
    'goal': TokenType.GOAL_KEYWORD,
    'readLn': TokenType.READ_LN_KEYWORD,
    'readint': TokenType.READ_INT_KEYWORD,
    'readchar': TokenType.READ_CHAR_KEYWORD,
    'write': TokenType.WRITE_KEYWORD,
    'integer': TokenType.INTEGER_DATA_TYPE,
    'symbol': TokenType.SYMBOL_DATA_TYPE,
    'string': TokenType.STRING_DATA_TYPE,
    'char': TokenType.CHAR_DATA_TYPE,
    'real': TokenType.REAL_DATA_TYPE
}


# operators Dictionary
operators = {
    '<': TokenType.LESS_THAN_OP,
    '<=': TokenType.LESS_THAN_EQUAL_OP,
    '>': TokenType.GREATER_THAN_OP,
    '>=': TokenType.GREATER_THAN_EQUAL_OP,
    '=': TokenType.EQUAL_OP,
    '<>': TokenType.ANGLED_BRACKETS_OP,
    '+' : TokenType.PLUS_OP,
    '-': TokenType.MINUS_OP,
    '*': TokenType.MULTIPLY_OP,
    '/' : TokenType.DIVIDE_OP,
    ',' : TokenType.AND_OP,
    ';' : TokenType.OR_OP,
    '.': TokenType.DOT_OP,
    '_' : TokenType.UNDERSCORE_OP,
    '(': TokenType.OPEN_BRACKET,
    ')': TokenType.CLOSE_BRACKET,
    ':-': TokenType.ASSIGNMENT_OP
}


def find_token(text):
    for lexeme in text:
        if lexeme in reserved_words:
            tok = Token(lexeme, reserved_words[lexeme])
            tokens.append(tok)
        elif lexeme in operators:
            tok = Token(lexeme, operators[lexeme])
            tokens.append(tok)
        # regular expression to match a real
        elif re.match('^[1-9][0-9]*[/.][0-9]+$', lexeme) or re.match('0[/.][0-9]+$', lexeme):
            tok = Token(lexeme, TokenType.REAL_VALUE)
            tokens.append(tok)
        # regular expression to match an integer
        elif re.match('^[1-9][0-9]*$', lexeme) or lexeme == '0':
            tok = Token(lexeme, TokenType.INTEGER_VALUE)
            tokens.append(tok)
        # regular expression to match a string
        elif re.match('^[\"].*[\"]$', lexeme):
            tok = Token(lexeme, TokenType.STRING_VALUE)
            tokens.append(tok)
        # regular expression to match variables
        elif re.match('^[A-Z_][A-Za-z0-9]*$', lexeme):
            tok = Token(lexeme, TokenType.VARIABLE)
            tokens.append(tok)
        # matching an identifier ->  predicate name or a symbol value
        elif re.match('^[a-z_][a-zA-Z0-9_]*$', lexeme):
            tok = Token(lexeme, TokenType.IDENTIFIER)
            tokens.append(tok)
        else:
            tok = Token(lexeme, TokenType.ERROR)
            errors.append("Lexical error  " + lexeme)







#----- OLD CODE --------
# class TokenType(Enum):
#     PREDICATE_KEYWORD = 1
#     CLAUSES_KEYWORD = 2
#     GOAL_KEYWORD = 3
#     AND_OP = 4
#     OR_OP = 5
#     READ_LN_KEYWORD = 6
#     READ_INT_KEYWORD = 7
#     READ_CHAR_KEYWORD = 8
#     WRITE_KEYWORD = 9
#     LESS_THAN_OP = 10
#     LESS_THAN_EQUAL_OP = 9
#     GREATER_THAN_OP = 10
#     GREATER_THAN_EQUAL_OP = 11
#     EQUAL_OP = 12
#     ANGLED_BRACKETS_OP = 13
#     PLUS_OP = 14
#     MINUS_OP = 15
#     MULTIPLY_OP = 16
#     DIVIDE_OP = 17
#     UNDERSCORE_OP = 18
#     VARIABLE = 19
#     DOT_OP = 20
#     OPEN_BRACKET = 21
#     CLOSE_BRACKET = 22
#     PREDICATE_NAME = 23
#     INTEGER_DATA_TYPE = 24
#     SYMBOL_DATA_TYPE = 25
#     STRING_DATA_TYPE = 26
#     CHAR_DATA_TYPE = 27
#     REAL_DATA_TYPE = 28
#     INTEGER_VALUE = 29
#     REAL_VALUE = 30
#     STRING_VALUE = 31
#     IDENTIFIER = 32
#     ASSIGNMENT_OP = 33
#     SYMBOL_VALUE = 34
#     ERROR = 35
#
#
# # Reserved word Dictionary
# reserved_words = {
#     "predicates": TokenType.PREDICATE_KEYWORD,
#     "clauses": TokenType.CLAUSES_KEYWORD,
#     'goal': TokenType.GOAL_KEYWORD,
#     'readLn': TokenType.READ_LN_KEYWORD,
#     'readint': TokenType.READ_INT_KEYWORD,
#     'readchar': TokenType.READ_CHAR_KEYWORD,
#     'write': TokenType.WRITE_KEYWORD,
#     'integer': TokenType.INTEGER_DATA_TYPE,
#     'symbol': TokenType.SYMBOL_DATA_TYPE,
#     'string': TokenType.STRING_DATA_TYPE,
#     'char': TokenType.CHAR_DATA_TYPE,
#     'real': TokenType.REAL_DATA_TYPE
# }
#
#
# # operators Dictionary
# operators = {
#     '<': TokenType.LESS_THAN_OP,
#     '<=': TokenType.LESS_THAN_EQUAL_OP,
#     '>': TokenType.GREATER_THAN_OP,
#     '>=': TokenType.GREATER_THAN_EQUAL_OP,
#     '=': TokenType.EQUAL_OP,
#     '<>': TokenType.ANGLED_BRACKETS_OP,
#     '+' : TokenType.PLUS_OP,
#     '-': TokenType.MINUS_OP,
#     '*': TokenType.MULTIPLY_OP,
#     '/' : TokenType.DIVIDE_OP,
#     ',' : TokenType.AND_OP,
#     ';' : TokenType.OR_OP,
#     '.': TokenType.DOT_OP,
#     '_' : TokenType.UNDERSCORE_OP,
#     '(': TokenType.OPEN_BRACKET,
#     ')': TokenType.CLOSE_BRACKET,
#     ':-': TokenType.ASSIGNMENT_OP
# }
#
#
# def find_token(text):
#     for lexeme in text:
#         if lexeme in reserved_words:
#             tok = Token(lexeme, reserved_words[lexeme])
#             tokens.append(tok)
#         elif lexeme in operators:
#             tok = Token(lexeme, operators[lexeme])
#             tokens.append(tok)
#         # regular expression to match a real
#         elif re.match('^[1-9][0-9]*[/.][0-9]+$', lexeme):
#             tok = Token(lexeme, TokenType.REAL_VALUE)
#             tokens.append(tok)
#         # regular expression to match an integer
#         elif re.match('^[1-9][0-9]*$', lexeme):
#             tok = Token(lexeme, TokenType.INTEGER_VALUE)
#             tokens.append(tok)
#         # regular expression to match a string
#         elif re.match('^[\"].*[\"]$', lexeme):
#             tok = Token(lexeme, TokenType.STRING_VALUE)
#             tokens.append(tok)
#         # regular expression to match variables
#         elif re.match('^[A-Z_][A-Za-z0-9]*$', lexeme):
#             tok = Token(lexeme, TokenType.VARIABLE)
#             tokens.append(tok)
#         # matching an identifier ->  predicate name or a symbol value
#         elif re.match('^[a-z_][a-zA-Z0-9_]*$', lexeme):
#             tok = Token(lexeme, TokenType.IDENTIFIER)
#             tokens.append(tok)
#         else:
#             tok = Token(lexeme, TokenType.ERROR)
#             errors.append("Lexical error  " + lexeme)


# print(lexemes)
# find_token(text=lexemes)
# print(tokens)
# for token in tokens:
#     token_dict = token.to_dict()
#     print(token_dict['Lexeme'], ": ", token_dict['token_type'])


