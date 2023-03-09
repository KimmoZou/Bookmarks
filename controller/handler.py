from PySide6.QtCore import QThreadPool
from model.bookmarks import Bookmarks
from model.worker import Worker
from model import  actions
from utils.split_bookmarks import SplitBookmarks
from utils.output_bookmarks import OutputBookmarks
from utils.input_bookmarks import InputBookmarks
from utils.save_bookmarks import SaveBookmarks


class HandlerTask(object):
    def __init__(self):
        self.bookmarks = Bookmarks()
        self.threadPool = QThreadPool()

    # 处理打开文件
    def handler_open(self, path, processFunc=[], finishFunc=[]):
        self.bookmarks.read_pdf(path)
        action = actions.OpenAction(self.bookmarks.bookmarks)
        worker = Worker(SplitBookmarks(), action)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        self.threadPool.start(worker)

    def handler_output(self, action: actions.OutputAction, processFunc=[], finishFunc=[]):
        action.set_txt(self.bookmarks.txt)
        worker = Worker(OutputBookmarks(),
                        action)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        self.threadPool.start(worker)

    def handler_input(self, action, processFunc=[], finishFunc=[]):
        worker = Worker(InputBookmarks(), action)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        self.threadPool.start(worker)

    def handler_save(self, action: actions.SaveAction,
                     processFunc= [],
                     finishFunc= [],
                     errorFunc =[]):
        action.set_pdf(self.bookmarks.doc)
        worker = Worker(SaveBookmarks(), action)
        for func in processFunc:
            worker.signals.process.connect(func)
        for func in finishFunc:
            worker.signals.finish.connect(func)
        for func in errorFunc:
            worker.signals.error.connect(func)
        self.threadPool.start(worker)


