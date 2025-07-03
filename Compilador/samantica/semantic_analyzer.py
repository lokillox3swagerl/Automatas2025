class SemanticError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, data_type):
        if name in self.symbols:
            raise SemanticError(f"Symbol '{name}' ya esta declarado.")
        self.symbols[name] = data_type #Que tome el tipo de dato

    def get(self, name):
        if name not in self.symbols:
            raise SemanticError(f"Error: La variable '{name}' no ha sido declarada.")
        return self.symbols[name]
    

def analyze_node(node, table):
    node_type = node.get("type")

    if node_type == "VarDecl":
        var_name = node["name"]#Retorna nombre de la variable, Ejemplo x
        expr_type = analyze_node(node["value"], table) #Retorna el tipo de dato de la expresión del sub nodo
        table.declare(var_name, expr_type) #Declara la variable en la tabla de símbolos
        return expr_type

    elif node_type == "Assignment":
        var_name = node["name"]
        var_type = table.get(var_name)
        expr_type = analyze_node(node["value"], table)
        if var_type != expr_type:
            raise SemanticError(f"Error de tipo: No se puede asignar {expr_type} a {var_type}.")
        return var_type

    elif node_type == "BinOp":
        left = analyze_node(node["left"], table)
        right = analyze_node(node["right"], table)
        op = node["op"]
        if left != right:
            raise SemanticError(f"Error de tipo: {left} {op} {right} no son compatibles.")
        # Puedes ajustar esta lógica para distintos operadores
        if op in ["+", "-", "*", "/"]:
            return left  # numérico
        elif op in ["<", ">", "<=", ">=", "==", "!="]:
            return "bool"
        else:
            raise SemanticError(f"Operador desconocido: {op}")

    elif node_type == "Number":
        return "int"
    elif node_type == "String":
        return "str"
    elif node_type == "Variable":
        return table.get(node["name"])

    elif node_type == "If":
        cond_type = analyze_node(node["condition"], table)
        if cond_type != "bool":
            raise SemanticError("La condición del 'if' debe ser de tipo bool.")
        for stmt in node["then"]:
            analyze_node(stmt, table)
        if node.get("else"):
            for stmt in node["else"]:
                analyze_node(stmt, table)

    elif node_type == "Program":
        for stmt in node["body"]:
            analyze_node(stmt, table)
    else:
        print(f"Advertencia: Tipo de nodo no manejado: {node_type}")

def analyze(ast):
    table = SymbolTable()
    try:
        analyze_node(ast, table)
        print("✅ Análisis semántico completado sin errores.")
    except SemanticError as e:
        print(f"❌ {e}")