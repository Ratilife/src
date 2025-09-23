from typing import List, Dict, Any, Optional, Set
class ClassInfo:
    def __init__(self, name):
        self.name = name
        self.base_classes = []  # родительские классы
        self.type_annotation = None  # аннотации класса
        self.decorators = []  # декораторы класса
        
        # Переменные класса с учётом наследования
        self.class_attributes = []  # атрибуты класса (через ClassVar)
        self.instance_attributes = []  # атрибуты экземпляра
        self.inherited_attributes = []  # унаследованные атрибуты
        self.overridden_attributes = []  # переопределённые атрибуты
        
        self.methods = []  # список FunctionInfo
        
        # Наследование
        self.parent_classes = []  # прямые родители
        self.ancestor_classes = []  # все предки
        self.child_classes = []  # прямые потомки
        self.descendant_classes = []  # все потомки
