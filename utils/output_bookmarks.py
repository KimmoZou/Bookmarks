from utils.base import Base

class OutputBookmarks(Base):
    def __init__(self):
        self.__signals = None
        self.__output_action = None

    def start(self, signal, action):
        self.__signals = signal
        self.__output_action = action
        self.__output_bookmarks()
        self.__close()

    def __output_bookmarks(self):

        try:
            with open(self.__output_action.path,  'w', encoding='utf-8',) as f:
                f.write(self.__output_action.txt)
        finally:
            f.close()

    def __close(self):
        self.__signals = None
        self.__output_action = None


