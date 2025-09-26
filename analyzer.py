import ast                                              # Импорт модуля для работы с абстрактными синтаксическими деревьями (AST) Python
from wrapper_classes.module_Info import ModuleInfo  # type: ignore
from wrapper_classes.function_Info import FunctionInfo # type: ignore
from wrapper_classes.class_Info import ClassInfo # type: ignore
from wrapper_classes.variable_info import VariableInfo
from wrapper_classes.imports_info import ImportInfo


class Analyzer(ast.NodeVisitor):              # Определение класса Analyzer, наследующего от ast.NodeVisitor для обхода AST
    # Конструктор класса, принимающий имя модуля                                           
    def __init__(self, name_module):
        self.module_name = name_module
       # Хранилища данных
        self.class_infos = []      #  для классов
        self.function_infos = []   #  для функций  
        self.variable_infos = []   #  для переменных  всех VariableInfo объектов
        self.import_infos = []     #  для импортов
        self.existing_variables = {}  # словарь: имя_переменной → VariableInfo
       

        # СИСТЕМА КОНТЕКСТА
        self.current_class = None      # Текущий класс (ClassInfo объект)
        self.current_function = None   # Текущая функция (FunctionInfo объект)
        self.current_scope = "global"  # Текущая область видимости
        self.scope_stack = []          # Стек для вложенных областей

    def _infer_type(self, value_node):  # TODO убрать, перегружает класс
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

    def _get_value(self, value_node):       # TODO убрать, перегружает класс
        """Извлекает значение из узла AST"""
        if isinstance(value_node, ast.Constant):
            return value_node.value  # 10, "hello", True, None
    
        elif isinstance(value_node, ast.List):
            return [self._get_value(element) for element in value_node.elts]
    
        elif isinstance(value_node, ast.Dict):
            return {self._get_value(k): self._get_value(v) 
                for k, v in zip(value_node.keys, value_node.values)}
    
        elif isinstance(value_node, ast.Tuple):
            return tuple(self._get_value(element) for element in value_node.elts)
    
        elif isinstance(value_node, ast.Name):
            return f"variable:{value_node.id}"  # ссылка на другую переменную
    
        elif isinstance(value_node, ast.Call):
            return f"call:{ast.unparse(value_node)}"  # вызов функции
    
        elif isinstance(value_node, ast.BinOp):
            return "expression"  # сложное выражение
    
        else:
            return "unknown_value"
    
    # Метод для обработки узлов импорта (import ...)
    def visit_Import(self, node):
        import_info = ImportInfo()
        import_info.module_name = node.names[0].name
        self.import_infos.append(import_info)
        self.generic_visit(node)

    # Метод для обработки узлов импорта из модуля (from ... import ...)
    def visit_ImportFrom(self, node):
        pass                            

    # Метод для обработки узлов присваивания (переменные)
    def visit_Assign(self, node): 
        for target in node.targets:
            if isinstance(target, ast.Name):                                                     
                var_name = target.id
                # ПРОВЕРЯЕМ, существует уже переменная
                if var_name not in self.existing_variables:
                    # 1. СОЗДАЕМ новую переменную ПЕРВЫМ делом
                    # Создаем только если переменная НОВАЯ
                    var_info = VariableInfo(var_name)

                    # 2. СОХРАНЯЕМ в словарь
                    self.existing_variables[var_name] = var_info
                    self.variable_infos.append(var_info)    # ← ДОБАВЛЯЕМ!
                    
                    # 3. ЗАПОЛНЯЕМ информацию
                    if self.current_class and self.current_function is None:
                        var_info.scope = "class_attribute"     # атрибут класса
                    elif self.current_class and self.current_function:
                        var_info.scope = "instance_attribute"  # атрибут экземпляра  
                    elif self.current_function:
                        var_info.scope = "local_variable"      # локальная переменная
                    else:
                        var_info.scope = "global_variable"     # глобальная переменная

                    # ОПРЕДЕЛЯЕМ ТИП из правой части (node.value)
                    var_info.type = self._infer_type(node.value)

                    # Заполняем местоположение 
                    var_info.declaration_location = (self.module_name, node.lineno)  
                    var_info.initialization_location = (self.module_name, node.lineno)
                    var_info.usage_count = 1
            else:
                # Берем существующую переменную
                var_info = self.existing_variables[var_name]    
                var_info.usage_count += 1  # увеличиваем счетчик использования
            
            var_info.initial_value = self._get_value(node.value)    #  ←  нужно изменить обращение к методу

        self.generic_visit(node)

    def visit_AnnAssign(self, node):
         if isinstance(node.target, ast.Name):
            var_info = VariableInfo(node.target.id)
            # ... заполняем + аннотации ...
            self.variable_infos.append(var_info)  # ← ДОБАВЛЯЕМ!
                    


    # Метод для обработки определений функций
    def visit_FunctionDef(self, node):                                  
        # СОХРАНЯЕМ предыдущий контекст
        previous_function = self.current_function
        previous_scope = self.current_scope

        # УСТАНАВЛИВАЕМ новый контекст
        self.current_function = FunctionInfo(node.name)
        self.current_scope = "local" if self.current_class else "function"

        # ТОЛЬКО параметры функций: def func(param1, param2)
        for arg in node.args.args:
            param_info = VariableInfo(arg.arg)
            param_info.scope = "parameter"
            self.variable_infos.append(param_info)  # ← ДОБАВЛЯЕМ!

        # Обрабатываем тело метода
        self.generic_visit(node)

        # ВОССТАНАВЛИВАЕМ предыдущий контекст
        self.current_function = previous_function  
        self.current_scope = previous_scope


    # Метод для обработки определений классов
    def visit_ClassDef(self, node):
        # СОХРАНЯЕМ предыдущий контекст
        previous_class = self.current_class
        previous_scope = self.current_scope

         # УСТАНАВЛИВАЕМ новый контекст
        self.current_class = ClassInfo(node.name)  # ← теперь мы внутри класса!
        self.current_scope = "class"

        # Обрабатываем тело класса
        self.generic_visit(node)

        # ВОССТАНАВЛИВАЕМ предыдущий контекст
        self.current_class = previous_class
        self.current_scope = previous_scope