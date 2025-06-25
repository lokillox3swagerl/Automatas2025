import re

KEYWORDS = {'var', 'if', 'else', 'while', 'function', 'return'}

token_specification = [
    ('NUMBER',   r'\d+(\.\d+)?'),
    ('STRING',   r'"[^"\n]*"'),
    ('ID',       r'[A-Za-z_][A-Za-z0-9_]*'),
    ('OP',       r'==|!=|<=|>=|=|\+|-|\*|/|<|>'),
    ('DELIM',    r'[()\{\};,]'),
    ('NEWLINE',  r'\n'),
    ('SKIP',     r'[ \t]+'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    tokens = []
    line_num = 1
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group()
        if kind == 'NUMBER':
            tokens.append((kind, float(value) if '.' in value else int(value)))
        elif kind == 'STRING':
            tokens.append((kind, value.strip('"')))
        elif kind == 'ID':
            kind = 'KEYWORD' if value in KEYWORDS else 'ID'
            tokens.append((kind, value))
        elif kind in {'OP', 'DELIM'}:
            tokens.append((kind, value))
        elif kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"[LÉXICO] Error: carácter inesperado '{value}' en línea {line_num}")
    return tokens

if __name__ == "__main__":
    with open("examples/miniscript.ms", "r") as f:
        code = f.read()
    tokens = tokenize(code)
    with open("output/tokens.txt", "w") as f:
        for token in tokens:
            f.write(f"{token}\n")
    print("✅ Análisis léxico completado.")
