class ModuleInfo:
    def __init__(self, name):
        self.name      = name
        self.path      = ""
        self.imports   = []
        self.variables = []
        self.functions = []
        self.classes   = []

    def set_path(self, path):
        self.path = path

           
