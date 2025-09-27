import os
from interfaces.IAction import IAction

class FileManager(IAction):
    def open(self, path):
        if os.path.exists(path):
            os.startfile(path)

    def execute(self, *args, **kwargs):
        path = kwargs.get("path")
        if path:
            self.open(path)
