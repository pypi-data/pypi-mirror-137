from distutils.log import error


class Error(Exception):
    def __init__(self, message):
        self.message = message 
    
    def __str__(self):
        return self.message

class LexerError(Error):
    def __init__(self, error_msg):
        super().__init__(error_msg)

class ParserError(Error):
    def __init__(self, error_msg):
        super().__init__(error_msg)

class SemanticError(Error):
    def __init__(self, error_msg):
        super().__init__(error_msg)

class RuntimeError(Error):
    def __init__(self, error_msg):
        super().__init__(error_msg)
    