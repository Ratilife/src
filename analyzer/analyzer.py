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

            # ИНИЦИАЛИЗИРУЕМ пустой список для использования
            var_info.usage_scope = []  # ← будет заполняться в visit_Name
            var_info.operations = []   # ← для операций типа +=, -= и т.д.

            #  СОХРАНЯЕМ в словарь
            self.existing_variables[var_name] = var_info
            self.variable_infos.append(var_info)    # ← ДОБАВЛЯЕМ!
                    
            #  ЗАПОЛНЯЕМ информацию о  Области видимости, в которой объявлена переменная
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
            
            var_info.usage_count = 0
        else:
            # Берем существующую переменную
            var_info = self.existing_variables[var_name]    
               
        
        return var_info 

    def _get_current_context(self):
        """Возвращает текущий контекст (функция, класс, модуль)"""
        context = {
            'module': self.module_name,
            'class': self.current_class.name if self.current_class else None,
            'function': self.current_function.name if self.current_function else None,
            'scope': self.current_scope
        }
        return context
    
    def _handle_variable_augassign(self, node):
        """Обрабатывает augmented assignment для простых переменных"""
        var_name = node.target.id
        var_info = self._get_or_create_variable(var_name, node)
    
        op_type = type(node.op).__name__.lower()
    
        # Записываем операцию
        var_info.operations.append({
            'type': f'augmented_{op_type}',
            'value': self.value_analyzer.get_value(node.value),
            'location': (self.module_name, node.lineno)
        })
    
        # Обновляем использование
        var_info.usage_scope.append({
            'type': 'write',
            'operation': f'augmented_{op_type}',
            'location': (self.module_name, node.lineno),
            'context': self._get_current_context()
        })

    def _handle_attribute_augassign(self, node):
        """Обрабатывает augmented assignment для атрибутов (self.count += 1)"""
        attr_name = node.target.attr  # имя атрибута ('count', 'name')
    
        # Создаем/получаем VariableInfo для атрибута
        var_info = self._get_or_create_variable(attr_name, node)
    
        op_type = type(node.op).__name__.lower()
        owner = self._get_attribute_owner(node.target.value)
    
        # Записываем операцию
        var_info.operations.append({
            'type': f'attribute_augmented_{op_type}',
            'value': self.value_analyzer.get_value(node.value),
            'owner': owner,
            'location': (self.module_name, node.lineno)
        })
    
        # Обновляем использование (НЕ увеличиваем usage_count - это запись)
        var_info.usage_scope.append({
            'type': 'write',
            'operation': f'attribute_augmented_{op_type}',
            'owner': owner,
            'location': (self.module_name, node.lineno),
            'context': self._get_current_context()
        })

    def _handle_subscript_augassign(self, node):
        """Обрабатывает augmented assignment для индексов (list[0] += 1)"""
        collection_name = self._get_collection_name(node.target.value)
    
        if collection_name and collection_name in self.existing_variables:
            var_info = self.existing_variables[collection_name]
        
            op_type = type(node.op).__name__.lower()
            index_info = self.value_analyzer.get_index_info(node.target.slice)
        
            # Записываем операцию
            var_info.operations.append({
                'type': f'subscript_augmented_{op_type}',
                'value': self.value_analyzer.get_value(node.value),
                'index': index_info,
                'location': (self.module_name, node.lineno)
            })
        
            # Обновляем использование (НЕ увеличиваем usage_count - это запись)
            var_info.usage_scope.append({
                'type': 'write',
                'operation': f'subscript_augmented_{op_type}',
                'index': index_info,
                'location': (self.module_name, node.lineno),
                'context': self._get_current_context()
            })

    def _get_attribute_owner(self, owner_node):
        """
        Определяет владельца атрибута (self, obj, module и т.д.)
        """
        if isinstance(owner_node, ast.Name):
            return owner_node.id  # 'self', 'obj', 'module'
        elif isinstance(owner_node, ast.Attribute):
            return ast.unparse(owner_node)  # 'obj.subobj'
        else:
            return "unknown"    

    def _get_collection_name(self, value_node):
        """Извлекает имя коллекции из узла"""
        if isinstance(value_node, ast.Name):
            return value_node.id  # list, dict, arr
        elif isinstance(value_node, ast.Attribute):
            return value_node.attr  # obj.data, self.items
        return None

    def _handle_subscript_write(self, var_info, node):
        """Обрабатывает запись в индекс"""
        index_info = self.value_analyzer.get_index_info(node.slice)
    
        usage_info = {
            'type': 'subscript_write',
            'location': (self.module_name, node.lineno, node.col_offset),
            'context': self._get_current_context(),
            'index': index_info
        }
    
        var_info.usage_scope.append(usage_info)
        #var_info.usage_count += 1
    
        # Записываем операцию
        var_info.operations.append({
            'type': 'subscript_assignment',
            'index': index_info,
            'location': (self.module_name, node.lineno)
        })

    def _handle_subscript_read(self, var_info, node):
        """Обрабатывает чтение по индексу"""
        index_info = self.value_analyzer.get_index_info(node.slice)
    
        usage_info = {
            'type': 'subscript_read',
            'location': (self.module_name, node.lineno, node.col_offset),
            'context': self._get_current_context(),
            'index': index_info
        }
    
        var_info.usage_scope.append(usage_info)
        var_info.usage_count += 1

    def _handle_subscript_delete(self, var_info, node):
        """Обрабатывает удаление по индексу"""
        index_info = self.value_analyzer.get_index_info(node.slice)
    
        usage_info = {
            'type': 'subscript_delete',
            'location': (self.module_name, node.lineno, node.col_offset),
            'context': self._get_current_context(),
            'index': index_info
        }
    
        var_info.usage_scope.append(usage_info)
        var_info.operations.append({
            'type': 'subscript_deletion',
            'index': index_info,
            'location': (self.module_name, node.lineno)
        })
     
   
    def _is_definition_context(self, node):
        """Проверяет, является ли узел определением (а не использованием)"""
        # Простая реализация - можно улучшить
        parent = getattr(node, 'parent', None)
        return isinstance(parent, (ast.ClassDef, ast.FunctionDef))    
    #------------

    def visit_Name(self, node):
        """
            Обрабатывает все упоминания переменных по имени.
            Определяет: чтение, запись, удаление.
        """
        if node.id in [cls.name for cls in self.class_infos]:
            return  # это класс, пропускаем
        
        if node.id in [func.name for func in self.function_infos]:
            return  # это функция, пропускаем

        if isinstance(node.ctx, ast.Store) and self._is_definition_context(node):
            return  # это определение
        
        if node.id in self.existing_variables:
            # Обрабатываем как переменную
            var_info = self.existing_variables[node.id]
        
         # Определяем тип операции
            usage_info = {
                'location': (self.module_name, node.lineno, node.col_offset),
                'context': self._get_current_context(),
                'timestamp': len(var_info.usage_scope)  # порядковый номер использования
            }

            if isinstance(node.ctx, ast.Load):
                usage_info['type'] = 'read'
                var_info.usage_count += 1

            elif isinstance(node.ctx, ast.Store):
                usage_info['type'] = 'write'
                # usage_count НЕ увеличиваем - уже сделано в visit_Assign   

            elif isinstance(node.ctx, ast.Del):
                usage_info['type'] = 'delete'
                var_info.lifetime_info['deleted_at'] = usage_info['location']    

            # Добавляем информацию об использовании
            var_info.usage_scope.append(usage_info)    

            # Логируем операцию
            var_info.operations.append({
                'type': 'name_reference',
                'context': node.ctx.__class__.__name__,
                'location': usage_info['location']
            })
    
        self.generic_visit(node)

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

    def  visit_AugAssign (self, node):
        """Обрабатывает операции типа +=, -=, *=, /= для переменных и атрибутов"""
    
        # Случай 1: Простая переменная (x += 5)
        if isinstance(node.target, ast.Name):
            # Простая переменная: x += 5
            self._handle_variable_augassign(node)
    
        # Случай 2: Атрибут объекта (self.count += 1)
        elif isinstance(node.target, ast.Attribute):
            self._handle_attribute_augassign(node)
    
        # Случай 3: Элемент коллекции (arr[0] += 1)
        elif isinstance(node.target, ast.Subscript):
            self._handle_subscript_augassign(node)
    
        self.generic_visit(node)    

    def visit_Attribute(self, node):
        """Обрабатывает obj.attr, self.value, module.function"""
        attr_name = node.attr  # имя атрибута ('count', 'name', 'value')
    
        # Обрабатываем только присваивания в атрибуты (obj.attr = value)
        if isinstance(node.ctx, ast.Store):
            # Создаем/получаем VariableInfo для атрибута
            var_info = self._get_or_create_variable(attr_name, node)
        
            usage_info = {
                'type': 'attribute_write',
                'location': (self.module_name, node.lineno, node.col_offset),
                'context': self._get_current_context(),
                'attribute_of': self._get_attribute_owner(node.value)  # кто владелец
            }
        
            var_info.usage_scope.append(usage_info)
        
            # Записываем операцию
            var_info.operations.append({
                'type': 'attribute_assignment',
                'owner': self._get_attribute_owner(node.value),
                'location': (self.module_name, node.lineno)
            })
    
        # Также обрабатываем чтение атрибутов (value = obj.attr)
        elif isinstance(node.ctx, ast.Load):
            if attr_name in self.existing_variables:
                var_info = self.existing_variables[attr_name]
            
            usage_info = {
                'type': 'attribute_read',
                'location': (self.module_name, node.lineno, node.col_offset),
                'context': self._get_current_context(),
                'attribute_of': self._get_attribute_owner(node.value)
            }
            
            var_info.usage_scope.append(usage_info)
            var_info.usage_count += 1
    
        self.generic_visit(node)



    def visit_Subscript(self, node):
        """
        Обрабатывает операции с индексами: list[index], dict[key], obj[slice]
        """
        # Получаем имя коллекции (если это простая переменная)
        collection_name = self._get_collection_name(node.value)
    
        if collection_name and collection_name in self.existing_variables:
            var_info = self.existing_variables[collection_name]
        
            # Определяем тип операции
            if isinstance(node.ctx, ast.Store):
                # Запись в индекс: list[0] = value
                self._handle_subscript_write(var_info, node)
            elif isinstance(node.ctx, ast.Load):
                # Чтение по индексу: x = list[0]
                self._handle_subscript_read(var_info, node)
            elif isinstance(node.ctx, ast.Del):
                # Удаление по индексу: del dict[key]
                self._handle_subscript_delete(var_info, node)
        
        self.generic_visit(node)

    # Метод для обработки узлов импорта (import ...)
    def visit_Import(self, node):
        for alias in node.names:
            import_info = ImportInfo()
        
            # Базовые характеристики
            import_info.import_type = 'import'
            import_info.module_name = alias.name
            import_info.imported_objects = [alias.name]
            import_info.location = (self.module_name, node.lineno)
        
            # Типы импортов
            import_info.has_alias = alias.asname is not None
            import_info.is_multiple_import = len(node.names) > 1
        
            # Контекст
            import_info.context = self._get_import_context()
            import_info.parent_scope = self._get_current_context()
            import_info.nesting_level = len(self.scope_stack)
        
            self.import_infos.append(import_info)
    
        self.generic_visit(node)

    # Метод для обработки узлов импорта из модуля (from ... import ...)
    def visit_ImportFrom(self, node):
        import_info = ImportInfo()
    
        # Базовые характеристики
        import_info.import_type = 'import_from'
        import_info.module_name = node.module
        import_info.location = (self.module_name, node.lineno)
    
        # Относительные импорты
        if node.level > 0:
            import_info.is_relative_import = True
            import_info.relative_level = node.level
            import_info.import_category = self._get_relative_category(node.level)
        else:
            import_info.is_absolute_import = True
    
        # Импортируемые объекты
        for alias in node.names:
            if alias.name == '*':
                import_info.is_star_import = True
            import_info.imported_objects.append({
                'name': alias.name,
                'alias': alias.asname
            })
    
        # Контекст и дополнительные поля
        import_info.context = self._get_import_context()
        import_info.is_conditional = self._detect_conditional_import(node)
        import_info.is_multiple_import = len(node.names) > 1
    
        self.import_infos.append(import_info)
        self.generic_visit(node)                       

    
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