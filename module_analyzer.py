import ast
from typing import Optional

class ModuleAnalyzer:
    #TODO ⌛ в разработке: 17.09.2025 
    def __init__(self):
        self.current_module_path: str =""       # путь к текущему анализируемому модулю
        self.current_module_name: str =""       # имя текущего модуля (извлечено из пути)
        self.module_ast: Optional[ast.Module] =  ast.Module(
                                                       body=[], 
                                                       type_ignores=[]
                                                    )    #AST дерево текущего модуля (результат ast.parse)
        self.classes_info: dict = {}            #словарь с информацией о всех классах в модуле
        self.module_level_imports: list =[]     #список всех импортов на уровне модуля
        self.analysis_errors:list =[]           #список ошибок, возникших при анализе

    #Начало Публичные методы

    def analyze_module(self, module_path:str):
        """главный метод, анализирует один модуль полностью"""
        pass

    def get_module_info(self):
        """возвращает всю собранную информацию о модуле"""
        return None  # #TODO 17.09.2025 возврат в модуле не определен

    def get_classes_dict(self)->dict:
        """возвращает список всех найденных классов"""
        return self.classes_info

    def get_imports_list(self)->list:
        """возвращает список всех импортов модуля"""
        return self.module_level_imports

    #Конец Публичные методы   