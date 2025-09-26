from typing import List, Dict, Any, Optional, Set

class VariableInfo:
    def __init__(self, name):
        self.name = name        # Имя
        self.type = None        # Тип    
        self.type_annotation = None  # статические аннотации типов
        self.scope = None  # масштаб: 'global', 'local', 'class', 'instance'
        self.access_modifier = None  # модификатор доступа: 'public', 'protected', 'private'
        
        # Жизненный цикл
        self.declaration_location = None  # местонахождение (file, line, module)
        self.initialization_location = None  # местоположение инициализации (file, line, module)
        self.usage_scope = []  # области где используется
        self.lifetime_info = {}
        
        # Использование
        self.usage_count = 0    # Счетчик показывает, сколько раз переменная была прочитана или изменена
        self.operations = []  # список операций
        self.usage_pattern = None  # 'counter', 'flag', 'buffer', etc.
        self.dependencies = []  # локальные зависимости
        
        # Межмодульные связи
        self.imported_from = None  # если переменная импортирована
        self.exported_to = []  # модули, куда экспортируется
        self.cross_module_references = []  # ссылки из других модулей
        
        # Значения
        self.initial_value = None      # начальное значение 
        self.value_range = None
        self.is_constant = False
        self.value_history = []
        
        # Декораторы и аннотации
        self.decorators = []  # декораторы для переменных (например, @property)
        self.annotations = {}  # дополнительные аннотации
        
        # Связи
        self.related_variables = []  # связанные переменные
        self.parent_variable = None  # для наследования
        self.overrides = None  # если переопределяет переменную родителя
