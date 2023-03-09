from utils.base import Base
from model import actions
from model.signals import Signals
from utils.tools import Tool


class InputBookmarks(Base):
    def __init__(self):
        self.signals = None
        self.input_action = None

    def start(self, signals: Signals, action: actions.InputAction):
        self.signals = signals
        self.input_action = action
        self.__input_bookmarks()
        self.__close()

    def __input_bookmarks(self):
        try:
            with open(self.input_action.path, 'r', encoding='utf-8', ) as f:
                preLvl = 1
                for line in f:
                    if line.strip('\n \t') == '':
                        continue

                    bookmark = Tool.str_to_list(line)
                    self.__emit_signal(bookmark, preLvl)
                    preLvl = bookmark[0]

                self.signals.finish.emit()
        finally:
            f.close()

    def __emit_signal(self, bookmark: list, preLvl: int):
        li = []
        if bookmark[0] == preLvl:
            li = [0]
        elif bookmark[0] > preLvl:
            li = [1]
        else:
            li = [bookmark[0] - preLvl]

        li.append(str(bookmark[1]))
        li.append(str(bookmark[2]))
        self.signals.process.emit(li)

    def __close(self):
        self.signals = None
        self.input_action = None
