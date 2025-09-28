import ast


class ValueAnalyzer:
    
    def infer_type(self, value_node):
        """Определяет тип значения"""
        if isinstance(value_node, ast.Constant):
            return type(value_node.value).__name__  # 'int', 'str', 'bool'
        elif isinstance(value_node, ast.List):
            return 'list'
        elif isinstance(value_node, ast.Dict):
            return 'dict'
        elif isinstance(value_node, ast.Set):
            return 'set'
        elif isinstance(value_node, ast.Tuple):
            return 'tuple'
        elif isinstance(value_node, ast.Call):
            return 'function_call'  # или анализировать глубже
        else:
            return 'unknown'
    
    
    def get_value(self, value_node):
        """Извлекает значение из узла AST"""
        if isinstance(value_node, ast.Constant):
            return value_node.value  # 10, "hello", True, None
    
        elif isinstance(value_node, ast.List):
            return [self.get_value(element) for element in value_node.elts]
    
        elif isinstance(value_node, ast.Dict):
            return {self.get_value(k): self.get_value(v) 
                for k, v in zip(value_node.keys, value_node.values)}
    
        elif isinstance(value_node, ast.Tuple):
            return tuple(self.get_value(element) for element in value_node.elts)
    
        elif isinstance(value_node, ast.Name):
            return f"variable:{value_node.id}"  # ссылка на другую переменную
    
        elif isinstance(value_node, ast.Call):
            return f"call:{ast.unparse(value_node)}"  # вызов функции
    
        elif isinstance(value_node, ast.BinOp):
            return "expression"  # сложное выражение
    
        else:
            return "unknown_value"