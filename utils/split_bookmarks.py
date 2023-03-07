from view.widgets import items


class SplitBookmarks(object):
    def __init__(self):
        self.bookmarks = []
        self.signals = None

    def split_bookmarks(self, signals, args):
        self.bookmarks = args[0]
        self.signals = signals

        length = len(self.bookmarks)

        for page in range(length):
            li = []
            if page >= 1:
                if self.bookmarks[page][0] > self.bookmarks[page - 1][0]:
                    li = [1]
                elif self.bookmarks[page][0] == self.bookmarks[page - 1][0]:
                    li = [0]
                else:
                    li = [self.bookmarks[page][0] - self.bookmarks[page - 1][0]]
            # 第一页 顶级节点
            else:
                li = [0]

            li.append(self.bookmarks[page][1])
            li.append(self.bookmarks[page][2])
            self.signals.process.emit(li)

        self.signals.finish.emit()
