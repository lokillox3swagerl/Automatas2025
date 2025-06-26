import json
from lexer.lexer import tokenize
from parser.parser import Parser
from utility.print import print_ast
from samantica.semantic_analyzer import analyze

if __name__ == "__main__":
    with open("Compilador/examples/miniscript.ms") as f:
        code = f.read()

    tokens = tokenize(code)
    parser = Parser(tokens)

    try:
        ast = parser.parse()
        print("✅ Análisis sintáctico completado.")
        
        with open("Compilador/output/ast.json", "w") as f:
            json.dump(ast, f, indent=2)

        print("📄 AST guardado en Compilador/output/ast.json")

        # 🔍 Análisis semántico
        print("\n🧠 Iniciando análisis semántico...")
        analyze(ast)

    except Exception as e:
        print(f"❌ Error de sintaxis: {e}")
