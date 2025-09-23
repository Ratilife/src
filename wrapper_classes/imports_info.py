class ImportInfo:
    def __init__(self):
        # Базовые характеристики
        self.import_type = None             # 'import' или 'import_from'
        self.module_name = None             # Имя модуля
        self.imported_objects = []          # Список импортируемых объектов
        self.location = None                # (файл, строка, столбец)
        self.nesting_level = 0              # Уровень вложенности
        
        # Типы импортов
        self.has_alias = False              # Есть ли алиас
        self.is_star_import = False         # Импорт всего (*)
        self.is_multiple_import = False     # Множественный импорт
        self.is_relative_import = False     # Относительный импорт
        self.is_absolute_import = False     # Абсолютный импорт
        
        # Относительные импорты
        self.relative_level = 0         # Уровень относительности
        self.import_category = None     # 'parent', 'grandparent', 'sibling', 'current'
        
        # Условные импорты
        self.is_conditional = False     # Условный импорт
        self.condition_type = None      # 'try_except', 'if_block', 'function'
        self.alternative_imports = []   # Альтернативные импорты
        
        # Контекст импорта
        self.context = 'global'         # 'global', 'function', 'class', 'method'
        self.parent_scope = None        # Родительская область видимости
        
        # Структура в файле
        self.import_block = 0           # Номер блока импортов
        self.has_comments = False       # Есть ли комментарии
        self.comments = []              # Текст комментариев
        
        # Дополнительная информация
        self.is_used = False            # Используется ли импорт
        self.usage_count = 0            # Количество использований

class ImportAnalysis:
    def __init__(self):
        self.imports = []               # Список всех ImportInfo
        
        # Метрики файла
        self.total_imports = 0
        self.unique_modules = set()
        self.fan_out = 0                # Количество уникальных модулей
        
        # Структурный анализ
        self.import_blocks = []         # Блоки импортов
        self.import_density = 0.0       # Импорты на строку кода
        
        # Проблемные случаи
        self.star_imports = []          # Star импорты
        self.shadowed_builtins = []     # Переопределение built-in
        self.import_conflicts = []      # Конфликты имен
        
        # Контекстный анализ
        self.global_imports = []
        self.function_imports = []
        self.class_imports = []
        self.conditional_imports = []