from typing import List, Dict, Any, Optional, Set
class ClassInfo:
    def __init__(self, name):
        
        self.name = name
    
        # Базовые характеристики
        self.location = None                # (файл, строка, столбец)
        self.docstring = None               # Строка документации класса
        self.module = None                  # Модуль, в котором определен класс
        
        # Иерархия наследования
        self.base_classes = []              # Прямые родительские классы
        self.multiple_inheritance = False   # Множественное наследование
        self.metaclass = None               # Метакласс класса
        self.decorators = []                # Декораторы класса
        
        # Атрибуты класса
        self.class_attributes = []          # Атрибуты класса (ClassVar)
        self.instance_attributes = []       # Атрибуты экземпляра
        self.typed_attributes = []          # Типизированные атрибуты (с аннотациями)
        self.constants = []                 # Константы (UPPERCASE)
        self.inherited_attributes = []      # Унаследованные атрибуты
        self.overridden_attributes = []     # Переопределённые атрибуты
        
        # Методы класса (детальная классификация)
        self.methods = []                   # Все методы как FunctionInfo
        self.instance_methods = []          # Методы экземпляра
        self.class_methods = []             # Методы класса (@classmethod)
        self.static_methods = []            # Статические методы (@staticmethod)
        self.magic_methods = []             # Магические методы (__name__)
        self.property_methods = []          # Свойства (@property)
        
        # Специальные методы
        self.has_constructor = False        # Наличие __init__
        self.has_destructor = False         # Наличие __del__
        self.string_representation = []     # __str__, __repr__
        self.comparison_operators = []      # __eq__, __lt__, etc.
        self.arithmetic_operators = []      # __add__, __sub__, etc.
        self.container_operators = []       # __getitem__, __setitem__
        self.iterator_methods = []          # __iter__, __next__
        self.context_managers = []          # __enter__, __exit__
        
        # Метрики размера и сложности
        self.method_count = 0               # Общее количество методов
        self.attribute_count = 0            # Общее количество атрибутов
        self.line_count = 0                 # Размер класса в строках кода
        self.cohesion_metrics = {}          # Метрики сцепления (LCOM и др.)
        
        # Связи и зависимости
        self.composition = []               # Композиция (атрибуты-объекты)
        self.aggregation = []               # Агрегация (внешние объекты)
        self.associations = []              # Ассоциации (типы параметров)
        
        # Шаблоны проектирования
        self.design_patterns = {
            'singleton': False,             # Singleton pattern
            'factory': False,               # Factory pattern
            'observer': False,              # Observer pattern
            'builder': False,               # Builder pattern
            'decorator': False,             # Decorator pattern
            'strategy': False               # Strategy pattern
        }
        
        # Иерархия наследования
        self.parent_classes = []            # Прямые родители
        self.ancestor_classes = []          # Все предки
        self.child_classes = []             # Прямые потомки
        self.descendant_classes = []        # Все потомки
        self.mro = []                       # Method Resolution Order