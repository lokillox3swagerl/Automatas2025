def print_ast(node, indent=0):
    spacing = "  " * indent
    if isinstance(node, dict):
        print(f"{spacing}{node.get('type', 'Unknown')}")
        for key, value in node.items():
            if key != 'type':
                print(f"{spacing}  {key}:")
                print_ast(value, indent + 2)
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent + 1)
    else:
        print(f"{spacing}{node}")
