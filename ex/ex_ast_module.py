import ast

with open("example.py", "r", encoding="utf-8") as f:
    tree = ast.parse(f.read(), filename="example.py")

print(ast.dump(tree, indent=4))  # структурированный вывод дерева




class ModuleInfo:
    def __init__(self, name):
        self.name = name
        self.imports = []
        self.variables = []
        self.functions = []
        self.classes = []

class FunctionInfo:
    def __init__(self, name, args):
        self.name = name
        self.args = args

class ClassInfo:
    def __init__(self, name):
        self.name = name
        self.methods = []

# Анализатор через NodeVisitor
class Analyzer(ast.NodeVisitor):
    def __init__(self):
        self.module = ModuleInfo("example")

    def visit_Import(self, node):
        self.module.imports.extend(alias.name for alias in node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.module.imports.extend(alias.name for alias in node.names)
        self.generic_visit(node)

    def visit_Assign(self, node):
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)]
        self.module.variables.extend(targets)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        func = FunctionInfo(node.name, [arg.arg for arg in node.args.args])
        self.module.functions.append(func)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        cls = ClassInfo(node.name)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                cls.methods.append(FunctionInfo(item.name, [arg.arg for arg in item.args.args]))
        self.module.classes.append(cls)
        self.generic_visit(node)

# --- Запуск ---
with open("example.py", "r", encoding="utf-8") as f:
    tree = ast.parse(f.read(), filename="example.py")

analyzer = Analyzer()
analyzer.visit(tree)

# Проверим результат
print("Импорты:", analyzer.module.imports)
print("Переменные:", analyzer.module.variables)
print("Функции:", [f.name for f in analyzer.module.functions])
for cls in analyzer.module.classes:
    print("Класс:", cls.name, "Методы:", [m.name for m in cls.methods])
