from typing import List, Dict, Any, Optional, Set
class ModuleInfo:
    def __init__(self, name):
        self.name = name
        self.file_path = None
        self.imports = []  # детальная информация об импортах
        
        # Переменные сгруппированные по типам
        self.global_variables = []  # глобальные переменные
        self.functions = []  # функции модуля
        self.classes = []  # классы модуля
        
        # Межмодульные связи
        self.imported_modules = []  # какие модули импортирует
        self.imported_by = []  # какие модули импортируют этот
        self.exported_elements = []  # что экспортирует модуль

    def set_path(self, path):
        self.file_path = path

           
