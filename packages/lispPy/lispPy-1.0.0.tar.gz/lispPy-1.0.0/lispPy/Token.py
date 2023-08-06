###############################################

#      Class for tokens allowed in code       #

###############################################

# List of tokens
INT_CONST = 'IntConst'
REAL_CONST = 'RealConst'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
DEFINE = 'DEFINE'
ID = 'ID'
PLUS, MINUS, MUL, DIV = 'PLUS', 'MINUS', 'MUL', 'DIV'

# Dictionary mapping characters to respective tokens 
str_to_token = {
    '(' : LPAREN,
    ')' : RPAREN,
    '+' : PLUS,
    '-' : MINUS,
    '*' : MUL,
    '/' : DIV,
    'define': DEFINE
}

class Token(object):
    def __init__(self, orig_char_stream):
        self.content = orig_char_stream
        self.token_type = self.match_to_token(orig_char_stream)

    def match_to_token(self, orig_char_stream):
        if orig_char_stream in str_to_token.keys():
            return str_to_token[orig_char_stream]
        elif self.is_integer(orig_char_stream):
            return INT_CONST
        elif self.is_real(orig_char_stream):
            return REAL_CONST
        else:
            return ID

    def is_integer(self, stream_of_chars):
        for char in stream_of_chars:
            if not char.isdigit():
                return False 
        return True

    def is_real(self, stream_of_chars):
        num_of_dots = 0
        for curr_char in stream_of_chars:
            if curr_char == '.':
                num_of_dots += 1
            if not self.is_valid_num_char(curr_char, num_of_dots):
                return False
        return True

    def is_valid_num_char(self, char, num_of_dots):
        return char.isdigit() or (char == '.' and num_of_dots <= 1)

    def is_type(self, given_type):
        return given_type == self.token_type
    
    def get_content(self):
        return self.content
    
    def get_type(self):
        return self.token_type

    def __repr__(self):
        return '("{}", {})'.format(self.content, self.token_type)
