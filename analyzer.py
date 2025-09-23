import ast                                              # Импорт модуля для работы с абстрактными синтаксическими деревьями (AST) Python
from src.wrapper_classes.module_Info import ModuleInfo  # type: ignore
from src.wrapper_classes.function_Info import FunctionInfo # type: ignore
from src.wrapper_classes.class_Info import ClassInfo # type: ignore

def _get_base_name(base):
    """
    Вспомогательная функция для извлечения имени базового класса.
    Обрабатывает простые имена, составные (module.BaseClass) и сложные выражения.
    """
    if isinstance(base, ast.Name):
        # Простой случай: class MyClass(Base)
        return base.id
    elif isinstance(base, ast.Attribute):
        # Составное имя: module.BaseClass
        return f"{_get_base_name(base.value)}.{base.attr}"
    else:
        # Fallback: для Generic[T], typing.List[int] и т.п.
        try:
            return ast.unparse(base)  # доступно с Python 3.9+
        except Exception:
            return ast.dump(base)     # универсальный отладочный вывод

class Analyzer(ast.NodeVisitor):                                        # Определение класса Analyzer, наследующего от ast.NodeVisitor для обхода AST
    # Конструктор класса, принимающий имя модуля                                           
    def __init__(self, name_module):
        self.module = ModuleInfo(name_module)                           # Создание экземпляра ModuleInfo для хранения информации о модуле
        # Хранилище для результатов анализа
        self.classes = []

    # Метод для обработки узлов импорта (import ...)
    def visit_Import(self, node):
        self.module.imports.extend(alias.name for alias in node.names)  # Добавление имен импортируемых модулей в список импортов
        self.generic_visit(node)                                        # Продолжение обхода дочерних узлов

    # Метод для обработки узлов импорта из модуля (from ... import ...)
    def visit_ImportFrom(self, node):
        self.module.imports.extend(alias.name for alias in node.names)  # Добавление имен импортируемых объектов в список импортов
        self.generic_visit(node)                                        # Продолжение обхода дочерних узлов

    # Метод для обработки узлов присваивания (переменные)
    def visit_Assign(self, node):                                                      
        targets = [t.id for t in node.targets if isinstance(t, ast.Name)] # Извлечение имен переменных из целей присваивания
        self.module.variables.extend(targets)                             # Добавление имен переменных в список переменных модуля
        self.generic_visit(node)                                          # Продолжение обхода дочерних узлов                                         

    # Метод для обработки определений функций
    def visit_FunctionDef(self, node):                                  
        func = FunctionInfo(node.name, [arg.arg for arg in node.args.args]) # Создание объекта FunctionInfo с именем функции и списком аргументов
        self.module.functions.append(func)                                  # Добавление информации о функции в модуль
        self.generic_visit(node)                                            # Продолжение обхода дочерних узлов (тела функции)

    # Метод для обработки определений классов
    def visit_ClassDef(self, node):
        """
        Обрабатывает узлы типа ClassDef (определения классов).
        """

        # Имя класса
        class_name = node.name

        # Базовые классы (с использованием безопасного извлечения)
        bases = [_get_base_name(base) for base in node.bases]

        # Методы (обычные и асинхронные)
        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

        # Атрибуты (простые и аннотированные)
        attributes = []
        for n in node.body:
            if isinstance(n, ast.Assign):
                for target in n.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
            elif isinstance(n, ast.AnnAssign):
                if isinstance(n.target, ast.Name):
                    attributes.append(n.target.id)

        # Вложенные классы
        nested_classes = [n.name for n in node.body if isinstance(n, ast.ClassDef)]

        # Докстринг
        docstring = ast.get_docstring(node)

        # Сохраняем информацию
        self.classes.append({
            "name": class_name,         # имя класса
            "bases": bases,             # список базовых классов
            "methods": methods,         # список методов
            "attributes": attributes,   # список атрибутов
            "nested": nested_classes,   # вложенные классы
            "docstring": docstring,     # строка документации
            "lineno": node.lineno       # номер строки в исходнике
        })

        # Продолжаем обход (для вложенных классов)
        self.generic_visit(node)