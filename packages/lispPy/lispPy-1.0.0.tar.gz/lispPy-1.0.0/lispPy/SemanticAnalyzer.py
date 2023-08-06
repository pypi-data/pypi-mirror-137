from lispPy.Token import *
from lispPy.Error import SemanticError

class SymbolTable(object):
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent
    
    def get_parent(self):
        return self.parent

    def add_symbol(self, symbol):
        self.table[symbol.get_name()] = symbol

    def contains_symbol(self, symb_name):
        if symb_name in self.table.keys():
            return True
        elif self.parent != None:
            return self.parent.contains_symbol(symb_name)
        else:
            return False

    def get_symbol(self, symb_name):
        if symb_name in self.table.keys():
            return self.table[symb_name]
        elif self.parent != None:
            return self.parent.get_symbol(symb_name)
        else:
            return None

class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type

    def get_name(self):
        return self.name 
    
    def get_type(self):
        return self.type 

class VarSymbol(Symbol):
    def __init__(self, name, type):
        super().__init__(name, type)

class ProcSymbol(Symbol):
    def __init__(self, name, proc):
        super().__init__(name)
        self.proc = proc
    
    def get_proc(self):
        return self.proc

class BuiltInType(Symbol):
    def __init__(self, name):
        super().__init__(name)

class SemanticAnalyzer():
    def __init__(self):
        pass 

    def check_logic_of_ast(self, ast):
        self.curr_scope = SymbolTable()
        self.generic_visit(ast)
        return
        
    def generic_visit(self, ast):
        name_of_visit_func = 'visit_' + type(ast).__name__
        visit_function = getattr(self, name_of_visit_func, self.visit_unknown)
        return visit_function(ast)
    
    def visit_unknown(self, ast):
        raise Exception('Given AST class {} does not exist'.format(type(ast).__name__))
    
    def visit_Root(self, root):
        for child in root.get_children():
            self.generic_visit(child)
    
    def visit_ArithmeticOperator(self, arithmatic_op):
        for child in arithmatic_op.get_children():
            self.generic_visit(child)
    
    def visit_ProcedureDeclaration(self, proc_decl):
        self.throw_error_if_in_scope(proc_decl.get_proc_name())
        self.curr_scope.add_symbol(ProcSymbol(proc_decl.get_proc_name(), proc_decl))
        self.create_new_scope()
        self.add_proc_args_to_scope(proc_decl)
        self.generic_visit(proc_decl.get_proc_body())
        self.remove_curr_scope()

    def create_new_scope(self):
        self.curr_scope = SymbolTable(self.curr_scope)
    
    def add_proc_args_to_scope(self, proc_decl):
        for arg in proc_decl.get_proc_args():
            self.curr_scope.add_symbol(VarSymbol(arg, None))

    def remove_curr_scope(self):
        self.curr_scope = self.curr_scope.get_parent()
 
    def visit_VariableDeclaration(self, var_decl):
        self.throw_error_if_in_scope(var_decl.get_var_name())
        self.curr_scope.add_symbol(VarSymbol(var_decl.get_var_name(), var_decl.get_var_type()))
        self.generic_visit(var_decl.get_var_value())

    def throw_error_if_in_scope(self, given_name):
        if self.curr_scope.contains_symbol(given_name):
            raise SemanticError('"{}" has already been defined'.format(given_name))

    def visit_ProcedureCall(self, proc_call):
        proc_name = proc_call.get_proc_name()
        self.throw_error_if_not_in_scope(proc_name)
        self.check_type(proc_name, 'ProcSymbol')
        self.check_call_args_match_exp_args(proc_name, proc_call)
        self.visit_each_call_arg(proc_call.get_passed_args())

    def check_call_args_match_exp_args(self, proc_name, proc_call):
        num_call_args = len(proc_call.get_passed_args())
        num_expected_args = len(self.curr_scope.get_symbol(proc_name).get_proc().get_proc_args())
        if num_call_args != num_expected_args:
            raise SemanticError('{} expected {} arguments, but received {}'.format(proc_name, num_expected_args, num_call_args))

    def visit_each_call_arg(self, proc_args):
        for arg in proc_args:
            self.generic_visit(arg)

    def visit_SingleVariable(self, var):
        var_name = var.get_var_name()
        self.throw_error_if_not_in_scope(var_name)
        self.check_type(var_name, 'VarSymbol')
 
    def throw_error_if_not_in_scope(self, name):
        if not self.curr_scope.contains_symbol(name):
            raise SemanticError('"{}" referenced but not defined'.format(name))

    def check_type(self, symbol_name, symbol_type):
        if type(self.curr_scope.get_symbol(symbol_name)).__name__ != symbol_type:
            raise SemanticError('"{}" was not declared as a {}'.format(symbol_name, symbol_type))

    def visit_UnaryOperator(self, unary_op):
        self.generic_visit(unary_op.get_child())

    def visit_NumericConstant(self, num_const):
        return 


