

class InputBookmarks(object):
    def __init__(self):
        self.signals = None
        self.path = ''

    def input_bookmarks(self, signals, args):
        self.path = args[0]
        self.signals = signals

        try:

            with open(self.path, 'r', encoding='utf-8', ) as f:
                preLvl = 1
                for line in f:
                    if line.strip('\n \t') == '':
                        continue

                    bookmark = self.__handler_str(line)
                    self.__emit_signal(bookmark, preLvl)
                    preLvl = bookmark[0]

                self.signals.finish.emit()
        finally:
            f.close()

    def __emit_signal(self, bookmark:list, preLvl: int):
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

    def __handler_str(self, line: str) -> list:
        lvl = 1
        i = 0
        length = len(line)

        # 获取级别
        while i < (length - 4):
            if line[i] == '\t':
                i += 1
                lvl += 1
            elif line[i:i + 4] == "    ":
                i += 4
                lvl += 1
            else:
                break

        # 处理字符串
        line = line.strip('\n \t')
        # 获取页码
        i = len(line) - 1
        while line[i] != ' ' and line[i] != '\t':
            i -= 1

        page = line[i + 1:].strip('\n \t')

        title = line[0:i].strip('\n \t')

        return [lvl, title, page]