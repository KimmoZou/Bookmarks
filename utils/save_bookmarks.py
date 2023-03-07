import sys
import traceback

from view.widgets import items

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
        except Exception:
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))

    def __init_toc(self, root: items.Item, lvl: int):
        if root is None:
            return

        li = []
        li.append(lvl)
        li.append(root.text(0))
        li.append(int(root.text(1).strip('\t \n')) + self.shift)
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

