from view.widgets import items
from exceptions import myexceptions
from utils.base import Base


class SaveBookmarks(Base):
    def __init__(self):
        self.signals = None
        self.save_action = None
        self.toc = []

    def start(self, signal, action):
        self.signals = signal
        self.save_action = action
        self.__save_bookmarks()
        self.__close()

    def __save_bookmarks(self):
        try:
            self.__init_toc(self.save_action.treeRoot.topLevelItem(0), 1)
            self.__write()
        except myexceptions.PageNumberError:
            self.signals.error.emit(myexceptions.PageNumberError().message)
        except myexceptions.PageOutOFNumberError:
            self.signals.error.emit(myexceptions.PageOutOFNumberError().message)

    def __init_toc(self, root: items.Item, lvl: int):
        if root is None:
            return

        li = [lvl, root.text(0)]
        page = root.text(1).strip('\t \n')

        if not str.isdigit(page):
            raise myexceptions.PageNumberError()

        if int(page) + self.save_action.shift <= 0:
            raise myexceptions.PageNumberError()

        if int(page) + self.save_action.shift > self.save_action.pdf.page_count:
            raise myexceptions.PageOutOFNumberError()

        li.append(int(page) + self.save_action.shift)
        self.toc.append(li)
        # 先递归儿子
        if root.child(0) is not None:
            self.__init_toc(root.child(0), lvl + 1)

        parent = root.parent()
        # 再加入兄弟
        if parent is None:
            index = self.save_action.treeRoot.indexOfTopLevelItem(root)
            self.__init_toc(self.save_action.treeRoot.topLevelItem(index + 1), lvl)
        else:
            index = parent.indexOfChild(root)
            self.__init_toc(parent.child(index + 1), lvl)

    def __write(self):
        self.save_action.pdf.set_toc(self.toc)
        self.save_action.pdf.save(self.save_action.path)
        self.signals.finish.emit()

    def __close(self):
        self.signals = None
        self.save_action = None
