from lexer.lexer import tokenize  # ajusta si tu lexer.py está en otra ruta

class ParserError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', None)

    def match(self, expected_type, expected_value=None):
        tok_type, tok_val = self.current_token()
        if tok_type == expected_type and (expected_value is None or tok_val == expected_value):
            self.pos += 1
            return tok_val
        raise ParserError(f"Error de sintaxis: Se esperaba {expected_type} '{expected_value}', pero se encontró {tok_type} '{tok_val}'")

    def parse(self):
        return self.program()

    def program(self):
        return {"type": "Program", "body": self.statement_list()}

    def statement_list(self):
        statements = []
        while self.current_token()[0] in {'KEYWORD', 'ID'}:
            statements.append(self.statement())
        return statements

    def statement(self):
        tok_type, tok_val = self.current_token()
        if tok_val == 'var':
            return self.var_decl()
        elif tok_val == 'if':
            return self.if_stmt()
        elif tok_val == 'while':
            return self.while_stmt()
        elif tok_val == 'function':
            return self.func_decl()
        elif tok_type == 'ID':
            next_tok = self.tokens[self.pos + 1]
            if next_tok[1] == '=':
                return self.assignment()
            elif next_tok[1] == '(':
                stmt = self.func_call()
                self.match('DELIM', ';')
                return stmt
        raise ParserError(f"Error de sintaxis en '{tok_val}'")

    def var_decl(self):
        self.match('KEYWORD', 'var')
        name = self.match('ID')
        self.match('OP', '=')
        expr = self.expression()
        self.match('DELIM', ';')
        return {"type": "VarDecl", "name": name, "value": expr}

    def assignment(self):
        name = self.match('ID')
        self.match('OP', '=')
        expr = self.expression()
        self.match('DELIM', ';')
        return {"type": "Assignment", "name": name, "value": expr}

    def if_stmt(self):
        self.match('KEYWORD', 'if')
        self.match('DELIM', '(')
        cond = self.expression()
        self.match('DELIM', ')')
        then_block = self.block()
        else_block = None
        if self.current_token() == ('KEYWORD', 'else'):
            self.match('KEYWORD', 'else')
            else_block = self.block()
        return {"type": "If", "condition": cond, "then": then_block, "else": else_block}

    def while_stmt(self):
        self.match('KEYWORD', 'while')
        self.match('DELIM', '(')
        cond = self.expression()
        self.match('DELIM', ')')
        body = self.block()
        return {"type": "While", "condition": cond, "body": body}

    def func_decl(self):
        self.match('KEYWORD', 'function')
        name = self.match('ID')
        self.match('DELIM', '(')
        params = self.params()
        self.match('DELIM', ')')
        body = self.block()
        return {"type": "Function", "name": name, "params": params, "body": body}

    def func_call(self):
        name = self.match('ID')
        self.match('DELIM', '(')
        args = self.args()
        self.match('DELIM', ')')
        return {"type": "FuncCall", "name": name, "args": args}

    def params(self):
        params = []
        if self.current_token()[0] == 'ID':
            params.append(self.match('ID'))
            while self.current_token() == ('DELIM', ','):
                self.match('DELIM', ',')
                params.append(self.match('ID'))
        return params

    def args(self):
        args = []
        if self.current_token()[0] in {'NUMBER', 'STRING', 'ID', 'DELIM'}:
            args.append(self.expression())
            while self.current_token() == ('DELIM', ','):
                self.match('DELIM', ',')
                args.append(self.expression())
        return args

    def block(self):
        self.match('DELIM', '{')
        body = self.statement_list()
        self.match('DELIM', '}')
        return body

    def expression(self):
        expr = self.arithmetic()
        while self.current_token()[1] in ('==', '!=', '<', '>', '<=', '>='):
            op = self.match('OP')
            right = self.arithmetic()
            expr = {"type": "BinOp", "op": op, "left": expr, "right": right}
        return expr

    def arithmetic(self):
        expr = self.term()
        while self.current_token()[1] in ('+', '-'):
            op = self.match('OP')
            right = self.term()
            expr = {"type": "BinOp", "op": op, "left": expr, "right": right}
        return expr
    
    def term(self):
        expr = self.factor()
        while self.current_token()[1] in ('*', '/'):
            op = self.match('OP')
            right = self.factor()
            expr = {"type": "BinOp", "op": op, "left": expr, "right": right}
        return expr

    def factor(self):
        tok_type, tok_val = self.current_token()
        if tok_type == 'NUMBER':
            self.match('NUMBER')
            return {"type": "Number", "value": tok_val}
        elif tok_type == 'STRING':
            self.match('STRING')
            return {"type": "String", "value": tok_val}
        elif tok_type == 'ID':
            if self.tokens[self.pos + 1][1] == '(':
                return self.func_call()
            self.match('ID')
            return {"type": "Variable", "name": tok_val}
        elif tok_val == '(':
            self.match('DELIM', '(')
            expr = self.expression()
            self.match('DELIM', ')')
            return expr
        raise ParserError(f"Error de sintaxis: token inesperado {tok_val}")

