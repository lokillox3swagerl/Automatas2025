import json
from lexer.lexer import tokenize
from parser.parser import Parser
from utility.print import print_ast
from samantica.semantic_analyzer import analyze
from codegen.code_generator import CodeGenerator

if __name__ == "__main__":
    with open("Compilador/examples/miniscript.ms") as f:
        code = f.read()

    # 1. Análisis Léxico
    print("🔤 Tokenizando código fuente...")
    tokens = tokenize(code)

    # 2. Análisis Sintáctico
    print("🧱 Construyendo AST...")
    parser = Parser(tokens)

    try:
        ast = parser.parse()
        print("✅ Análisis sintáctico completado.\n")

        # Mostrar e imprimir AST
        #print("🌲 Árbol de derivación (AST):")
        #print_ast(ast)

        with open("Compilador/output/ast.json", "w") as f:
            json.dump(ast, f, indent=2)
        print("📄 AST guardado en Compilador/output/ast.json")

        # 3. Análisis Semántico
        print("\n🧠 Iniciando análisis semántico...")
        analyze(ast)

        # 4. Generación de Código Intermedio
        print("\n⚙️ Generando código intermedio...")
        gen = CodeGenerator()
        intermediate_code = gen.generate(ast)

        with open("Compilador/output/code.txt", "w") as f:
            for line in intermediate_code:
                f.write(line + "\n")

        print("✅ Código intermedio guardado en Compilador/output/code.txt")

    except Exception as e:
        print(f"\n❌ Error durante compilación: {e}")
