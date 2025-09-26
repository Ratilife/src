import ast
from pathlib import Path
from typing import Optional
from analyzer_old import Analyzer
from wrapper_classes.module_Info  import ModuleInfo
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
        self._parse_module_file(module_path)

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

    #Приватные методы для работы с AST

    def _parse_module_file(self, file_path: str)->None:
        #TODO ⌛ в разработке: 20.09.2025

        name_module = Path(file_path).name
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=name_module)

        # Шаг 1: Analyzer создает и заполняет все контейнеры    
        analyzer = Analyzer()
        analyzer.visit(tree)

        # Шаг 2: Создаем ModuleInfo и упаковываем всё вместе
        module_info = ModuleInfo(name_module)
        module_info.classes = analyzer.class_infos                      # все классы
        module_info.functions = analyzer.function_infos                 # все функции
        module_info.import_analysis.imports = analyzer.import_infos     # импорты

    

    #Конец Приватные методы для работы с AST