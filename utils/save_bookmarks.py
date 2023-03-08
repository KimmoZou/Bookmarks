from view.widgets import items
from exceptions import  myexceptions

class SaveBookmarks(object):
    def __init__(self):
        self.toc = None
        self.signals = None
        self.path = ''
        self.shift = 0
        self.pdf = None
        self.treeRoot = None
        

    def save_bookmarks(self, signals, args):
        self.toc = []
        self.path = args[0]
        self.shift = args[1]
        self.pdf = args[2]
        self.treeRoot = args[3]
        self.signals = signals
        try:
            self.__init_toc(self.treeRoot.topLevelItem(0), 1)
            self.__write()
        except myexceptions.PageNumberError:
            self.signals.error.emit(myexceptions.PageNumberError().message)
        except myexceptions.PageOutOFNumberError:
            self.signals.error.emit(myexceptions.PageOutOFNumberError().message)

    def __init_toc(self, root: items.Item, lvl: int):
        if root is None:
            return

        li = []
        li.append(lvl)
        li.append(root.text(0))
        page = root.text(1).strip('\t \n')

        if not str.isdigit(page):
            raise myexceptions.PageNumberError()

        if int(page) + self.shift <= 0:
            raise myexceptions.PageNumberError()

        if int(page) + self.shift > self.pdf.page_count:
            raise myexceptions.PageOutOFNumberError()

        li.append(int(page) + self.shift)
        self.toc.append(li)
        # 先递归儿子
        if root.child(0) is not None:
            self.__init_toc(root.child(0), lvl + 1)

        parent = root.parent()
        # 再加入兄弟
        if parent is None:
            index = self.treeRoot.indexOfTopLevelItem(root)
            self.__init_toc(self.treeRoot.topLevelItem(index+1), lvl)
        else:
            index = parent.indexOfChild(root)
            self.__init_toc(parent.child(index + 1), lvl)


    def __write(self):
        self.pdf.set_toc(self.toc)
        self.pdf.save(self.path)
        self.signals.finish.emit()

