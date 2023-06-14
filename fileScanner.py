import re


#---------- NEW CODE -------------
def find_next(i, character, text):
    for j in range(i, len(text)):
        if text[j] == character:
            return j


def scan(directory):
    # Open the file and read its contents into a string
    with open(directory, encoding='utf-8') as f:
        text = str(f.read())

    # removing all comments
    uncommented_text = ''
    i = 0
    while i < len(text):
        if text[i] == '%':
            i = find_next(i + 1, '\n', text)
        elif text[i] == '/' and text[i + 1] == '*':
            i = find_next(i + 2, '*', text) + 2
        else:
            uncommented_text += text[i]
            i += 1

    # Split the text into lexemes
    lexemes = re.findall(r'\w+|[^\w\s]', uncommented_text)

    # combine Strings
    x = 0
    while x < len(lexemes):
        if lexemes[x] == '\"':
            new_string = '\"'
            end_index = -1
            for n in range(x + 1, len(lexemes)):
                if lexemes[n] == '\"':
                    end_index = n
                    # new_string += '\n'
                    new_string += '\"'
                    break
                elif n == x + 1:
                    new_string += lexemes[n]
                else:
                    new_string += ' ' + lexemes[n]
            for n in range(x, end_index + 1):
                del lexemes[x]
            lexemes.insert(x, new_string)
        x += 1

    for n in range(len(lexemes)):
        if lexemes[n] == ':' and lexemes[n+1] == '-':
            del lexemes[n]
            lexemes[n] = ':-'
            lexemes.append(None)

    while lexemes[-1] is None:
        lexemes.pop()


    for n in range(len(lexemes)):
        if lexemes[n] == '<' and lexemes[n+1] == '=':
            del lexemes[n]
            lexemes[n] = '<='
            lexemes.append(None)

    while lexemes[-1] is None:
        lexemes.pop()


    for n in range(len(lexemes)):
        if lexemes[n] == '>' and lexemes[n+1] == '=':
            del lexemes[n]
            lexemes[n] = '>='
            lexemes.append(None)

    while lexemes[-1] is None:
        lexemes.pop()


    for n in range(len(lexemes)):
        if lexemes[n] == '<' and lexemes[n+1] == '>':
            del lexemes[n]
            lexemes[n] = '<>'
            lexemes.append(None)

    while lexemes[-1] is None:
        lexemes.pop()

    # combine floating numbers together
    numbers_pattern = re.compile('^[1-9][0-9]*$')
    numbers_pattern_2 = re.compile('^[0-9]+$')
    j = 0
    for lexeme in lexemes:
        new_lexeme = ''
        if (re.match(numbers_pattern, lexeme) and lexemes[j + 1] == '.') or (lexeme == '0' and lexemes[j + 1] == '.'):
            if re.match(numbers_pattern_2, lexemes[j + 2]):
                new_lexeme = lexeme + lexemes[j + 1] + lexemes[j + 2]
                del lexemes[j]
                del lexemes[j]
                del lexemes[j]
                lexemes.insert(j, new_lexeme)
        j += 1

    print("List of all lexemes of the program:")
    print(lexemes)
    return lexemes









#---------- OLD CODE -------------
# def find_next(i, character, text):
#     for j in range(i, len(text)):
#         if text[j] == character:
#             return j
#
#
# def scan(directory):
#     # Open the file and read its contents into a string
#     with open(directory, encoding='utf-8') as f:
#         text = str(f.read())
#
#     # removing all comments
#     uncommented_text = ''
#     i = 0
#     while i < len(text):
#         if text[i] == '%':
#             i = find_next(i + 1, '\n', text)
#         elif text[i] == '/' and text[i + 1] == '*':
#             i = find_next(i + 2, '*', text) + 2
#         else:
#             uncommented_text += text[i]
#             i += 1
#
#     # Split the text into lexemes
#     lexemes = re.findall(r'\w+|[^\w\s]', uncommented_text)
#
#     # combine Strings
#     x = 0
#     while x < len(lexemes):
#         if lexemes[x] == '\"':
#             new_string = '\"'
#             end_index = -1
#             for n in range(x + 1, len(lexemes)):
#                 if lexemes[n] == '\"':
#                     end_index = n
#                     # new_string += '\n'
#                     new_string += '\"'
#                     break
#                 elif n == x + 1:
#                     new_string += lexemes[n]
#                 else:
#                     new_string += ' ' + lexemes[n]
#             for n in range(x, end_index + 1):
#                 del lexemes[x]
#             lexemes.insert(x, new_string)
#         x += 1
#
#     for n in range(len(lexemes)):
#         if lexemes[n] == ':' and lexemes[n+1] == '-':
#             del lexemes[n]
#             lexemes[n] = ":-"
#
#     # combine floating numbers together
#     numbers_pattern = re.compile('^[1-9][0-9]*$')
#     j = 0
#     for lexeme in lexemes:
#         new_lexeme = ''
#         if re.match(numbers_pattern, lexeme) and lexemes[j + 1] == '.':
#             if re.match(numbers_pattern, lexemes[j + 2]):
#                 new_lexeme = lexeme + lexemes[j + 1] + lexemes[j + 2]
#                 del lexemes[j]
#                 del lexemes[j]
#                 del lexemes[j]
#                 lexemes.insert(j, new_lexeme)
#         j += 1
#     return lexemes


