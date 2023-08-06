from lispPy.Token import *
from lispPy.Error import LexerError

class Lexer(object):
    def __init__(self, code_to_tokenize):
        self.code_to_tokenize = code_to_tokenize
        self.pos_in_code = 0 
    
    def get_next_token(self):
        self.skip_whitespace()
        if self.at_end_of_code():
            return None
        else:
            return self.get_token_from_char(self.get_curr_char())
    
    def skip_whitespace(self):
        while not self.at_end_of_code() and self.get_curr_char() in (' ', '\n'):
            self.pos_in_code += 1
    
    def get_token_from_char(self, curr_char):
        if self.is_builtin_type(curr_char):
            self.advance()
            return Token(curr_char)
        elif self.is_int(curr_char):
            numeric_value = self.get_numeric_value()
            return Token(numeric_value)
        elif self.is_valid_varchar(curr_char):
            var_name = self.get_full_var_name()
            return Token(var_name)
        else:
            raise LexerError('Unable to tokenize {} at position {}'.format(self.code_to_tokenize, self.pos_in_code))
    
    def is_builtin_type(self, curr_char):
        return curr_char in str_to_token.keys()
    
    def get_full_var_name(self):
        var_name = ''
        while not self.at_end_of_code() and self.is_valid_varchar(self.get_curr_char()):
            var_name += self.get_curr_char()
            self.advance()
        return var_name
    
    def is_valid_varchar(self, curr_char):
        return curr_char.isalnum() or curr_char == '_'

    def get_numeric_value(self):
        numeric_value = ""
        while not self.at_end_of_code() and self.is_valid_num_operator(self.get_curr_char()):
            numeric_value += self.get_curr_char()
            self.advance()
        return numeric_value
    
    def advance(self):
        self.pos_in_code += 1

    def at_end_of_code(self):
        return self.pos_in_code >= len(self.code_to_tokenize)

    def is_valid_num_operator(self, curr_char):
        return self.is_int(curr_char) or curr_char == '.'

    def is_int(self, curr_char):
        return curr_char.isdigit()

    def get_curr_char(self):
        return self.code_to_tokenize[self.pos_in_code]