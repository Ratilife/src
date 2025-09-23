from typing import List, Dict, Any, Optional, Set
from wrapper_classes.variable_info import VariableInfo
class ProjectInfo:
    """Хранит информацию обо всём проекте"""
    def __init__(self, name="MyProject"):
        self.name = name
        self.modules = []                # все модули проекта
        self.variable_graph = {}         # граф связей между переменными
        self.import_graph = {}           # граф импортов между модулями
        self.inheritance_hierarchy = {}  # иерархия наследования
        
    def find_variable_references(self, variable_name: str) -> List[VariableInfo]:
        """Найти все ссылки на переменную по имени"""
        pass
    
    def get_variable_lineage(self, variable: VariableInfo) -> List[VariableInfo]:
        """Получить lineage переменной (наследование)"""
        pass
    
    def analyze_cross_module_dependencies(self):
        """Анализ межмодульных зависимостей"""
        pass

    def add_module(self, module_info):
        self.modules.append(module_info)
