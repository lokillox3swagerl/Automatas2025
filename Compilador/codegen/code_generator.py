class CodeGenerator:
    def __init__(self):
        self.code = []
        self.temp_counter = 0

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def generate(self, node):
        method_name = f"gen_{node['type'].lower()}"
        method = getattr(self, method_name, self.gen_default)
        return method(node)

    def gen_default(self, node):
        raise NotImplementedError(f"Generador no implementado para tipo {node['type']}")

    def gen_program(self, node):
        for stmt in node['body']:
            self.generate(stmt)
        return self.code

    def gen_vardecl(self, node):
        temp = self.generate(node["value"])
        self.code.append(f"{node['name']} = {temp}")

    def gen_assignment(self, node):
        temp = self.generate(node["value"])
        self.code.append(f"{node['name']} = {temp}")

    def gen_number(self, node):
        return str(node["value"])

    def gen_string(self, node):
        return f'"{node["value"]}"'

    def gen_variable(self, node):
        return node["name"]

    def gen_binop(self, node):
        left = self.generate(node["left"])
        right = self.generate(node["right"])
        temp = self.new_temp()
        self.code.append(f"{temp} = {left} {node['op']} {right}")
        return temp

    def gen_if(self, node):
        cond = self.generate(node["condition"])
        else_label = f"L{self.temp_counter + 1}"
        end_label = f"L{self.temp_counter + 2}"
        self.code.append(f"IF_FALSE {cond} GOTO {else_label}")
        for stmt in node["then"]:
            self.generate(stmt)
        self.code.append(f"GOTO {end_label}")
        self.code.append(f"{else_label}:")
        if node.get("else"):
            for stmt in node["else"]:
                self.generate(stmt)
        self.code.append(f"{end_label}:")
