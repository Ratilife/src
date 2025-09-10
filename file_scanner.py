from pathlib import Path
from types import Optional, Tuple, List

class FileScanner:
   def __init__(self,root_dir:str):
      self.modules: dict[str,str] = {}                     # {Имя файла,путь к файлу}
      self.packages: Optional[Tuple[str, List[str], str]]  # [Имя пакета, Имена модуллей, путь к папке]
      self.root_dir = Path(root_dir)


   def _find_python_modules(self, root_dir):
        self.modules = {}
        for path in self.root_dir.rglob("*.py"):
            if "__pycache__" not in path.parts:
               continue
            if not path.name.endswith(".pyc"):
               continue
            module_name = path.stem  # имя файла без расширения
            self.modules[module_name] =  str(path)


   def _scan_package(self, folder: Path) -> Optional[Tuple[str, List[str], str]]:
       # Проверка на наличие __init__.py
        if not (folder / "__init__.py").exists():
            return None
        
        # Имя пакета: относительный путь, точки вместо слэшей
        relative_path = folder.relative_to(self.root_dir)
        package_name = ".".join(relative_path.parts)

        # Список модулей: все .py файлы, кроме __init__.py
        module_names = [
            path.stem
            for path in folder.glob("*.py")
            if path.name != "__init__.py"
        ]

        self.packages =  package_name, module_names, str(folder)

   def get_packages(self):
       return self.packages

   def get_modules(self):
       return self.modules      