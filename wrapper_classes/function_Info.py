from typing import List, Dict, Any, Optional, Set
class FunctionInfo:
    def __init__(self, name, args):
        self.name = name                    # Имя функции/метода
        self.args = args                    # список VariableInfo для аргументов
        
        # Сигнатура метода
        self.parameters = []                # Список параметров функции с детальной информацией  ?
        self.default_values = {}            # Значения по умолчанию для параметров {имя_параметра: значение}

        self.has_varargs = False            # Наличие *args параметра
        self.has_kwargs = False             # Наличие **kwargs параметра
        self.kwonly_args = []               # Keyword-only аргументы (аргументы после * или *args)
        self.return_type_annotation = None  # Аннотация возвращаемого типа
        self.returns_value = False          # Возвращает ли функция значение (есть ли return с значением)

        # Декораторы
        self.decorators = []                # Список декораторов, примененных к функции
        self.is_staticmethod = False        # Является ли статическим методом (@staticmethod)
        self.is_classmethod = False         # Является ли методом класса (@classmethod)
        self.is_property = False            # Является ли свойством (@property)
        self.is_abstract = False            # Является ли абстрактным методом (@abstractmethod)
        
         # Структура тела
        self.line_count = 0                 # Количество строк кода в функции
        self.nesting_level = 0              # Уровень вложенности (максимальная глубина блоков)
        self.return_count = 0               # Количество операторов return
        self.docstring = None               # Строка документации функции
        self.complexity_metrics = {}        # Метрики сложности (цикломатическая сложность и др.)

         # Вызовы и зависимости
        self.function_calls = []            # Список вызовов других функций
        self.method_calls = []              # Список вызовов методов объектов
        self.recursive_calls = 0            # Количество рекурсивных вызовов (вызовов самой себя)
        self.used_variables = []            # Переменные, которые читаются в функции (load)
        self.modified_variables = []        # Переменные, которые изменяются в функции (store)
        self.variables = []                 # локальные переменные
        self.dependencies = []              # Внешние зависимости (модули, классы, функции)
       
        # Обработка исключений
        self.try_blocks = []                # Блоки try-except
        self.raise_statements = []          # Операторы raise (выброс исключений)
        self.handled_exceptions = []        # Типы исключений, которые обрабатываются
        self.has_finally = False            # Наличие блока finally

        # Контроль потока
        self.if_statements = 0              # Количество условных операторов if/elif
        self.loops = 0                      # Количество циклов (for, while)
        self.break_statements = 0           # Количество операторов break
        self.continue_statements = 0        # Количество операторов continue
        self.yield_statements = 0           # Количество операторов yield
        self.is_generator = False           # Является ли функция генератором (содержит yield)

        # Работа с классами (актуально для методов)
        self.uses_super = False             # Используется ли вызов super()
        self.accesses_self = False          # Обращается ли к атрибутам self (для методов экземпляра)
        self.accesses_cls = False           # Обращается ли к атрибутам cls (для методов класса)
        
         # Связи с другими элементами кода
        self.calls = []                     # вызовы других функций
        self.called_by = []                 # кто вызывает эту функцию
        self.overrides = None               # Метод родительского класса, который переопределяется
        self.overridden_by = []             # Методы дочерних классов, которые переопределяют данный мето
