from typing import List, Dict, Any, Optional, Set
from imports_info import ImportAnalysis
class ModuleInfo:
    def __init__(self, name):
        self.name = name
        self.file_path = None
        
        # Базовые характеристики
        self.loc = 0                            # Lines of Code
        self.ast_tree = None                    # AST дерево модуля
        self.top_level_nodes = []               # Узлы верхнего уровня
        self.nesting_level = 0                  # Максимальный уровень вложенности
        self.code_blocks = 0                    # Количество блоков кода
        
        # Импорты и зависимости
        self.imports = []                           # Детальная информация об импортах
        self.import_analysis = ImportAnalysis()     # Детальный анализ импортов
        self.unused_imports = []                    # Неиспользуемые импорты
        self.conditional_imports = []               # Условные импорты
        
        # Определения в модуле
        self.global_variables = []                  # Глобальные переменные
        self.constants = []                         # Константы (UPPERCASE)
        self.functions = []                         # Функции модуля
        self.classes = []                           # Классы модуля
        self.enums = []                             # Перечисления
        self.exceptions = []                        # Пользовательские исключения
        
        # Документация
        self.docstring = None                       # Module docstring
        self.comments = []                          # Список комментариев
        self.multiline_comments = []                # Многострочные комментарии
        self.todos = []                             # Будет содержать объекты типа:
        # {
        #   'type': 'TODO' или 'FIXME',
        #   'text': 'текст комментария',
        #   'location': (file, line, column),
        #   'context': 'функция/класс, где найден'
        # }
        
        # Экспортируемый интерфейс
        self.all_export = []                        # Содержимое __all__
        self.public_functions = []                  # Публичные функции
        self.private_functions = []                 # Приватные функции
        self.public_classes = []                    # Публичные классы
        self.private_classes = []                   # Приватные классы
        self.exported_variables = []                # Экспортируемые переменные
        
        # Выполняемость
        self.has_main_guard = False                 # Наличие if __name__ == "__main__"
        self.main_function = None                   # Точка входа
        self.is_script = False                      # Скрипт или модуль
        self.uses_argparse = False                  # Использует argparse
        self.uses_sys_argv = False                  # Использует sys.argv
        
        # Качество кода и безопасность
        self.code_duplication = []                  # Дублирование кода
        self.unsafe_operations = []                 # eval, exec, pickle и т.д.
        self.security_issues = []                   # Потенциальные уязвимости
        self.unsafe_imports = []                    # Небезопасные импорты
        
        # Совместимость
        self.python_version = None                  # Минимальная версия Python
        self.future_imports = []                    # Импорты из __future__
        self.platform_dependencies = []             # Зависимости от платформы
        
        # Метрики сложности
        self.metrics = {
            'loc': 0,  # Lines of Code
            'noc': 0,  # Number of Classes
            'nom': 0,  # Number of Methods
            'dit': 0,  # Depth of Inheritance
            'complexity': 0  # Общая сложность
        }
        
        # Межмодульные связи
        self.imported_modules = []                  # Какие модули импортирует
        self.imported_by = []                       # Какие модули импортируют этот
        self.exported_elements = []                 # Что экспортирует модуль
        self.dependency_graph = {}                  # Граф зависимостей

    def set_path(self, path):
        self.file_path = path
           
       