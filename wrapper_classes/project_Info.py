class ProjectInfo:
    """Хранит информацию обо всём проекте"""
    def __init__(self, name="MyProject"):
        self.name = name
        self.modules = []  # список ModuleInfo

    def add_module(self, module_info):
        self.modules.append(module_info)
