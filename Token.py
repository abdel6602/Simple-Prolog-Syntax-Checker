# class token to hold string and token type
class Token:
    def __init__(self, lexeme, token_type):
        self.lexeme = lexeme
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lexeme': self.lexeme,
            'token_type': self.token_type
        }
