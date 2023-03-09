from utils.base import Base
from model import actions


class SplitBookmarks(Base):
    def __init__(self):
        self.__open_action = None
        self.__signals = None

    def start(self, signal, action):
        self.__signals = signal
        self.__open_action = action
        self.__split_bookmarks()
        self.__close()

    def __split_bookmarks(self,):

        length = len(self.__open_action.bookmarks)

        for page in range(length):
            li = []
            if page >= 1:
                if self.__open_action.bookmarks[page][0] > self.__open_action.bookmarks[page - 1][0]:
                    li = [1]
                elif self.__open_action.bookmarks[page][0] == self.__open_action.bookmarks[page - 1][0]:
                    li = [0]
                else:
                    li = [self.__open_action.bookmarks[page][0] - self.__open_action.bookmarks[page - 1][0]]
            # 第一页 顶级节点
            else:
                li = [0]

            li.append(self.__open_action.bookmarks[page][1])
            li.append(self.__open_action.bookmarks[page][2])
            self.__signals.process.emit(li)

        self.__signals.finish.emit()

    def __close(self):
        self.__signals = None
        self.__open_action = None
