import ast
from src.wrapper_classes.module_Info import ModuleInfo  # type: ignore
from src.wrapper_classes.function_Info import FunctionInfo # type: ignore
from src.wrapper_classes.class_Info import ClassInfo # type: ignore

class Analyzer(ast.NodeVisitor):
    def __init__(self, name_module):
        self.module = ModuleInfo(name_module)

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