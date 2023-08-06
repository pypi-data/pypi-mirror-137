from string import printable


class Ast(object):
    pass

class Root(Ast):
    def __init__(self, group_of_children):
        super().__init__()
        self.group_of_children = group_of_children
    
    def get_children(self):
        return self.group_of_children

    def __repr__(self):
        printable_repr = ""
        for child in self.group_of_children:
            printable_repr += child.__repr__()
        return printable_repr

class ArithmeticOperator(Ast):
    def __init__(self, operator, group_of_children):
        super().__init__()
        self.operator = operator
        self.group_of_children = group_of_children
    
    def get_operator(self):
        return self.operator
    
    def get_children(self):
        return self.group_of_children

    def __repr__(self):
        printable_repr = ""
        for child in self.group_of_children:
            printable_repr += child.__repr__()
        printable_repr += self.operator + ", "
        return printable_repr

class ProcedureDeclaration(Ast):
    def __init__(self, proc_name, proc_args, body, inner_procedures=None):
        super().__init__()
        self.proc_name = proc_name
        self.proc_args = proc_args
        self.body = body
        self.inner_procedures = inner_procedures

    def get_proc_args(self):
        return self.proc_args

    def get_proc_name(self):
        return self.proc_name
    
    def get_proc_body(self):
        return self.body

    def __repr__(self):
        printable_repr = 'name: {} args: {} '.format(self.proc_name, self.proc_args)
        printable_repr += self.body.__repr__()
        return printable_repr

class ProcedureCall(Ast):
    def __init__(self, proc_name, proc_args):
        super().__init__()
        self.proc_name = proc_name
        self.proc_args = proc_args
    
    def get_proc_name(self):
        return self.proc_name

    def get_passed_args(self):
        return self.proc_args
    
    def __repr__(self):
        return 'Called Procedure name: {} Procedure Args: {}'.format(self.proc_name, self.proc_args)

class VariableDeclaration(Ast):
    def __init__(self, var_name, var_value):
        super().__init__()
        self.var_name = var_name
        self.var_value = var_value
    
    def get_var_name(self):
        return self.var_name

    def get_var_value(self):
        return self.var_value

    # Function right now returns None - in more advanced versions, we will save type of variables
    def get_var_type(self):
        return None

    def __repr__(self):
        printable_repr = 'Variable_Declaration({}, {}), '.format(self.var_name, self.var_value)
        return printable_repr

class SingleVariable(Ast):
    def __init__(self, var_name):
        super().__init__()
        self.var_name = var_name
    
    def get_var_name(self):
        return self.var_name

    def __repr__(self):
        printable_repr = 'SingleVariable({})'.format(self.var_name)
        return printable_repr

class UnaryOperator(Ast):
    def __init__(self, operator, child):
        super().__init__()
        self.operator = operator
        self.child = child 
    
    def get_operator(self):
        return self.operator
    
    def get_child(self):
        return self.child

    def __repr__(self):
        printable_repr = '{}UnOp({}), '.format(self.child, self.operator)
        return printable_repr

class NumericConstant(Ast):
    def __init__(self, type, value):
        super().__init__()
        self.type = type
        self.value = value
    
    def get_value(self):
        return self.value

    def get_type(self):
        return self.type

    def __repr__(self):
        printable_repr = str(self.value) + ", "
        return printable_repr