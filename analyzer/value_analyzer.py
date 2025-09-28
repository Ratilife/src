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
        

    def get_index_info(self, slice_node):
        """Извлекает информацию об индексе/срезе"""
        if isinstance(slice_node, ast.Index):
            # Устаревший формат (Python < 3.9)
            return self.value_analyzer.get_value(slice_node.value)
        elif isinstance(slice_node, ast.Constant):
            # Простой индекс: list[0]
            return slice_node.value
        elif isinstance(slice_node, ast.Slice):
            # Срез: list[1:10:2]
            return {
                'type': 'slice',
                'start': self.value_analyzer.get_value(slice_node.lower),
                'stop': self.value_analyzer.get_value(slice_node.upper),
                'step': self.value_analyzer.get_value(slice_node.step)
            }
        elif isinstance(slice_node, ast.Name):
            # Переменная как индекс: list[index]
            return f"variable:{slice_node.id}"
        else:
            return "complex_index"
            