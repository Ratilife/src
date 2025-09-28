import ast                                              # Импорт модуля для работы с абстрактными синтаксическими деревьями (AST) Python
from wrapper_classes.module_Info import ModuleInfo  # type: ignore
from wrapper_classes.function_Info import FunctionInfo # type: ignore
from wrapper_classes.class_Info import ClassInfo # type: ignore
from wrapper_classes.variable_info import VariableInfo
from wrapper_classes.imports_info import ImportInfo
from analyzer.value_analyzer import ValueAnalyzer


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

        self.value_analyzer = ValueAnalyzer()
    
    def _get_or_create_variable(self, var_name, node):
        # ПРОВЕРЯЕМ, существует уже переменная
        if var_name not in self.existing_variables:
            # 1. СОЗДАЕМ новую переменную ПЕРВЫМ делом
            # Создаем только если переменная НОВАЯ
            var_info = VariableInfo(var_name)

            # 2. СОХРАНЯЕМ в словарь
            self.existing_variables[var_name] = var_info
            self.variable_infos.append(var_info)    # ← ДОБАВЛЯЕМ!
                    
            # 3. ЗАПОЛНЯЕМ информацию о  Области видимости, в которой объявлена переменная
            if self.current_class and self.current_function is None:
                var_info.scope = "class_attribute"     # атрибут класса
            elif self.current_class and self.current_function:
                var_info.scope = "instance_attribute"  # атрибут экземпляра  
            elif self.current_function:
                var_info.scope = "local_variable"      # локальная переменная
            else:
                var_info.scope = "global_variable"     # глобальная переменная

            # Заполняем местоположение 
            var_info.declaration_location = (self.module_name, node.lineno)  
            
            var_info.usage_count = 1
        else:
            # Берем существующую переменную
            var_info = self.existing_variables[var_name]    
            var_info.usage_count += 1  # увеличиваем счетчик использования      
        
        return var_info 


    # Метод для обработки узлов присваивания (переменные)
    def visit_Assign(self, node): 
        for target in node.targets:
            if isinstance(target, ast.Name):                                                     
                var_info = self._get_or_create_variable(target.id, node)
                
                # ОПРЕДЕЛЯЕМ ТИП из правой части (node.value)
                var_info.type = self.value_analyzer.infer_type(node.value)          
                var_info.initial_value = self.value_analyzer.get_value(node.value)    #  ←  нужно изменить обращение к методу
                var_info.initialization_location = (self.module_name, node.lineno)  

        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        if isinstance(node.target, ast.Name):
            var_info = self._get_or_create_variable(node.target.id, node)
            
            # Заполняем ТОЛЬКО специфичные для AnnAssign поля
            var_info.type_annotation = ast.unparse(node.annotation)

            if node.value is not None:  # если есть присваивание: x: int = 10
                var_info.type = self.value_analyzer.infer_type(node.value)
                var_info.initial_value = self.value_analyzer.get_value(node.value)
                var_info.initialization_location = (self.module_name, node.lineno)
            
        self.generic_visit(node)    
                        

    # Метод для обработки узлов импорта (import ...)
    def visit_Import(self, node):
        import_info = ImportInfo()
        import_info.module_name = node.names[0].name
        self.import_infos.append(import_info)
        self.generic_visit(node)

    # Метод для обработки узлов импорта из модуля (from ... import ...)
    def visit_ImportFrom(self, node):
        pass                            

    
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