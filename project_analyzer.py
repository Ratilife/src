# Это главный модуль
from pathlib import Path
from module_analyzer import ModuleAnalyzer
from import_analyzer import ImportAnalyzer
from report_generator import ReportGenerator

class ProjectAnalyzer:
    def __init__(self):
        self.project_path: str = ''
        self.modules_info: dict = {}
        self.analysis_results: dict = {} 
        self.import_graph = None # TODO - 10.09.2025 пока не знаю какой будет тип данных
        self.file_scanner = None # TODO - 10.09.2025 пока не знаю какой будет тип данных
        self.module_analyzer = ModuleAnalyzer()
        self.import_analyzer = ImportAnalyzer()
        self.report_generator = ReportGenerator()

        