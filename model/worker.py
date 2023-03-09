from PySide6.QtCore import QRunnable,  Slot

from model.signals import Signals


class Worker(QRunnable):
    def __init__(self, task, action):
        super(Worker, self).__init__()
        self.task = task
        self.action = action
        self.signals = Signals()

    def __close(self):
        self.task = None
        self.action = None
        self.signals = None

    @Slot()
    def run(self):
        self.task.start(self.signals, self.action)
        self.__close()