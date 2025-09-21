import threading
from module_analyzer import ModuleAnalyzer

class ThreadPool:
    def __init__(self):
        self.streams = []        # Создаем список для хранения потоков

    def start_work(self,path_file: str, module_analyzer: ModuleAnalyzer):
        # Создаем список для хранения потоков
        
        stream = threading.Thread(target=module_analyzer.analyze_module,
                                              args=(path_file,))    # ← запятая делает это кортежем (нужно передавать кортеж)
        self.streams.append(stream)   # Добавляем поток в список потоков
        stream.start()           # Запускаем поток

    def end_work(self):
        # Ожидаем завершения всех потоков
        for stream in self.streams:
            stream.join()