from typing import List, Dict, Any, Optional, Set
class FunctionInfo:
    def __init__(self, name, args):
        self.name = name
        self.args = args # список VariableInfo для аргументов
        self.return_type_annotation = None
        self.variables = []  # локальные переменные
        self.decorators = []  # декораторы функции
        self.calls = []  # вызовы других функций
        self.called_by = []  # кто вызывает эту функцию
