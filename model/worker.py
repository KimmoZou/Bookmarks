from PySide6.QtCore import QRunnable,  Slot

from model.signals import Signals


class Worker(QRunnable):
    def __init__(self, func, *args):
        super(Worker, self).__init__()
        self.func = func
        self.args = args
        self.signals = Signals()

    @Slot()
    def run(self):
        self.func(self.signals, self.args)