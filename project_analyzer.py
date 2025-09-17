# Это главный модуль

from module_analyzer import ModuleAnalyzer
from import_analyzer import ImportAnalyzer
from report_generator import ReportGenerator
from file_scanner import FileScanner

class ProjectAnalyzer:
    def __init__(self):
        self.project_path: str = ''
        self.modules_info: dict = {}
        self.analysis_results: dict = {} 
        self.import_graph = None # TODO - 10.09.2025 пока не знаю какой будет тип данных
        self.file_scanner = FileScanner(self.project_path)
        self.module_analyzer = ModuleAnalyzer()
        self.import_analyzer = ImportAnalyzer()
        self.report_generator = ReportGenerator()


    def _scan_project_files(self):
        """находит все Python файлы в проекте"""

        self.modules_info = self.file_scanner.get_modules()
             
    def _analyze_modules(self):
        """анализирует содержимое каждого найденного модуля"""
                