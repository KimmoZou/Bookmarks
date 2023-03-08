from PySide6.QtCore import QObject, Signal


class Signals(QObject):
    process = Signal(list)
    finish = Signal()
    error = Signal(str)