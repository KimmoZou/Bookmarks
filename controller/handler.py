from PySide6.QtCore import QThreadPool
from model.bookmarks import Bookmarks
from model.worker import Worker
from utils.split_bookmarks import SplitBookmarks
from utils.output_bookmarks import OutputBookmarks
from utils.input_bookmarks import InputBookmarks
from utils.save_bookmarks import SaveBookmarks

class HandlerTask(object):
    def __init__(self):
        self.bookmarks = Bookmarks()
        self.splitBookmarks = SplitBookmarks()
        self.outputBookmarks = OutputBookmarks()
        self.inputBookmarks = InputBookmarks()
        self.saveBookmarks = SaveBookmarks()
        self.threadPool = QThreadPool()

    # 处理打开文件
    def handler_open(self, path, processFunc=[], finishFunc=[]):
        self.bookmarks.read_pdf(path)
        worker = Worker(self.splitBookmarks.split_bookmarks, self.bookmarks.bookmarks)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        self.threadPool.start(worker)

    def handler_output(self, path, processFunc=[], finishFunc=[]):
        worker = Worker(self.outputBookmarks.output_bookmarks,
                        self.bookmarks.txt, path)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        self.threadPool.start(worker)

    def handler_input(self, path, processFunc=[], finishFunc=[]):
        worker = Worker(self.inputBookmarks.input_bookmarks, path)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        self.threadPool.start(worker)

    def handler_save(self, path, shift, treeRoot,
                     processFunc= [],
                     finishFunc= [],
                     errorFunc =[]):
        worker = Worker(self.saveBookmarks.save_bookmarks,
                        path,
                        shift,
                        self.bookmarks.doc,
                        treeRoot)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        for func in errorFunc:
            worker.signals.error.connect(func)
        self.threadPool.start(worker)


