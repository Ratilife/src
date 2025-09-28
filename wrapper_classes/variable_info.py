from typing import List, Dict, Any, Optional, Set

class VariableInfo:
    def __init__(self, name):
        self.name = name        # Имя                                                              ← _get_or_create_variable 
        self.type = None        # Тип                                                              ←visit_Assign 
        self.type_annotation = None  # статические аннотации типов                                 ← visit_AnnAssign 
        self.scope = None  # масштаб: 'global', 'local', 'class', 'instance'                       ← _get_or_create_variable 
        self.access_modifier = None  # модификатор доступа: 'public', 'protected', 'private'       ← _get_or_create_variable 
        
        # Жизненный цикл
        self.declaration_location = None  # местонахождение (file, line, module)                   ← _get_or_create_variable 
        self.initialization_location = None  # местоположение инициализации (file, line, module)   ← visit_AnnAssign (если есть присваивание)
        self.usage_scope = []    # области где используется                                        ← _get_or_create_variable 
        self.lifetime_info = {}  # Время жизни (определяется по использованиям)                    ←visit_Assign 
        
        # Использование
        self.usage_count = 0    # Счетчик показывает, сколько раз переменная была прочитана или изменена ← _get_or_create_variable 
        self.operations = []  # список операций                                                    ← _get_or_create_variable 
        self.usage_pattern = None  # 'counter', 'flag', 'buffer', etc.                             ←visit_Assign
        self.dependencies = []  # локальные зависимости                                            ← visit_AnnAssign
        
        # Межмодульные связи
        self.imported_from = None  # если переменная импортирована                                 ← _get_or_create_variable 
        self.exported_to = []  # модули, куда экспортируется                                       ← _get_or_create_variable 
        self.cross_module_references = []  # ссылки из других модулей                              ← _get_or_create_variable 
        
        # Значения
        self.initial_value = None      # начальное значение                                        ←visit_Assign
        self.value_range = None        # диапазон значений                                         ←visit_Assign
        self.is_constant = False       # флаг константности                                        ← visit_AnnAssign 
        self.value_history = []        # история изменений                                         ←visit_Assign
        
        # Декораторы и аннотации
        self.decorators = []  # декораторы для переменных (например, @property)                    ← visit_AnnAssign
        self.annotations = {}  # дополнительные аннотации                                          ← visit_AnnAssign
        
        # Связи
        self.related_variables = []  # связанные переменные                                        ← _get_or_create_variable  
        self.parent_variable = None  # для наследования                                            ← _get_or_create_variable 
        self.overrides = None  # если переопределяет переменную родителя                           ← _get_or_create_variable 
