from lispPy.Ast import *
from lispPy.Token import *
from lispPy.Error import ParserError

'''
    Current Grammar: 
    Statement_list: (statement)+
    Statement: parenth | single_expr
    parenth: LPAREN (var_decl | op_expr | proc_decl | proc_call) RPAREN
    proc_decl: DEFINE LPAREN ID ID(ID)* RPAREN (LPAREN proc_decl RPAREN)* LPAREN (op_expr | proc_call) RPAREN
    proc_call: ID (num_expr)+
    var_decl: DEFINE ID num_expr
    num_expr: single_expr | LPAREN op_expr RPAREN
    op_expr: (PLUS | MINUS | MUL | DIV) (num_expr)+
    single_expr: (PLUS | MINUS | empty) (INT | REAL | ID)

'''

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer 
        self.curr_token = self.lexer.get_next_token()

    def get_ast_from_code(self):
        lines_of_code = []
        while self.curr_token != None:
            lines_of_code.append(self.get_ast_from_single_line())
        return Root(lines_of_code)
    
    def get_ast_from_single_line(self):
        if self.curr_token.is_type(LPAREN):
            return self.process_parenthesis_expr()
        elif self.curr_token.get_type() in (PLUS, MINUS, INT_CONST, REAL_CONST, ID): 
            return self.get_single_value()
        else:
            raise ParserError('Unable to parse token {}'.format(self.curr_token.get_type()))
    
    def process_parenthesis_expr(self):
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(DEFINE):
            paren_expr = self.process_define_expr()
        elif self.curr_token.is_type(ID):
            paren_expr = self.process_proc_call()
        else:
            paren_expr = self.process_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return paren_expr

    def process_define_expr(self):
        self.process_token_of_type(DEFINE)
        if self.curr_token.is_type(ID):
            return self.process_variable_decl_expr()
        else:
            return self.process_proc_decl_expr()
    
    def process_variable_decl_expr(self):
        var_name = self.process_token_of_type(ID) 
        var_value = self.process_arith_expr_args()
        return VariableDeclaration(var_name, var_value)

    def process_proc_decl_expr(self):
        proc_name, proc_params = self.process_formal_variables()
        proc_body = self.get_proc_body()
        return ProcedureDeclaration(proc_name, proc_params, proc_body)

    def process_formal_variables(self):
        self.process_token_of_type(LPAREN)
        proc_name = self.process_token_of_type(ID)
        proc_params = self.get_proc_parameters()
        self.process_token_of_type(RPAREN)
        return proc_name, proc_params
    
    def get_proc_parameters(self):
        proc_params = []
        while self.still_reading_from_proc():
            proc_params.append(self.process_token_of_type(ID))
        return proc_params

    def get_proc_body(self):
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(ID):
            proc_body = self.process_proc_call()
        else:
            proc_body = self.process_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return proc_body
    
    def process_proc_call(self):
        proc_name = self.process_token_of_type(ID)
        proc_args = self.get_proc_call_args()
        return ProcedureCall(proc_name, proc_args)
    
    def get_proc_call_args(self):
        proc_args = [] 
        while self.still_reading_from_proc():
            proc_args.append(self.process_arith_expr_args())
        return proc_args

    def still_reading_from_proc(self):
        return not (self.curr_token.is_type(RPAREN) or self.curr_token == None)

    def process_arith_expr_args(self):
        if self.curr_token.is_type(LPAREN):
            return self.process_arith_paren_expr()
        else:
            return self.get_single_value()

    def get_single_value(self):
        curr_token_type = self.curr_token.get_type()
        if curr_token_type in (PLUS, MINUS):
            operand = self.process_token_of_type(curr_token_type)
            return UnaryOperator(operand, self.get_single_value())
        elif curr_token_type == INT_CONST:
            return NumericConstant(curr_token_type, self.process_token_of_type(INT_CONST))
        elif curr_token_type == REAL_CONST:
            return NumericConstant(curr_token_type, self.process_token_of_type(REAL_CONST))
        elif curr_token_type == ID:
            return SingleVariable(self.process_token_of_type(ID))
        else:
            raise ParserError('Unexpected Token type {}'.format(curr_token_type))

    def process_arith_paren_expr(self):
        self.process_token_of_type(LPAREN)
        if self.curr_token.is_type(ID):
            parenth_expr = self.process_proc_call()
        else:
            parenth_expr = self.process_arith_op_expr()
        self.process_token_of_type(RPAREN)
        return parenth_expr

    def process_arith_op_expr(self):
        if self.curr_token != None and self.curr_token.get_type() in (PLUS,MINUS,MUL,DIV):
            operator = self.process_token_of_type(self.curr_token.get_type())
            return ArithmeticOperator(operator, self.get_arith_expr_params())
        else:
            raise ParserError('Expected Binary Operator, instead got {}'.format(self.curr_token))

    def get_arith_expr_params(self):
        group_of_params = [self.process_arith_expr_args()]
        while not (self.curr_token == None or self.curr_token.is_type(RPAREN)):
            group_of_params.append(self.process_arith_expr_args())
        return group_of_params

    def process_token_of_type(self, type):
        self.check_error_in_token(type)
        type_adapted_content = self.adapt_content_to_type(self.curr_token.get_content(), type)
        self.curr_token = self.lexer.get_next_token()
        return type_adapted_content

    def adapt_content_to_type(self, content, type):
        if type == INT_CONST:
            return int(content)
        elif type == REAL_CONST:
            return float(content)
        elif type == ID:
            return str(content)
        return content

    def check_error_in_token(self, type):
        if self.curr_token == None:
            raise ParserError('Expected {}, instead got None'.format(type))
        elif not self.curr_token.is_type(type):
            raise ParserError('Expected {}, instead got {}'.format(type, self.curr_token.get_type()))