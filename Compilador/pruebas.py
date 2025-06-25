import json
from lexer.lexer import tokenize
from parser.parser import Parser
from utility.print import print_ast

if __name__ == "__main__":
    with open("examples/miniscript.ms") as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)
    
    try:
        ast = parser.parse()
        print("✅ Análisis sintáctico completado.")
        
        with open("output/ast.json", "w") as f:
            json.dump(ast, f, indent=2)

        print("📄 AST guardado en output/ast.json")
    except Exception as e:
        print(f"❌ Error de sintaxis: {e}")
    # después de generar el AST

#print("\n🌲 Árbol de derivación (AST):")
#print_ast(ast)