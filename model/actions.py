class InputAction(object):
    def __init__(self, path=''):
        self.path = path

    def set_path(self, path):
        self.path = path


class OutputAction(object):
    def __init__(self, path='', txt=''):
        self.path = path
        self.txt = txt

    def set_path(self, path):
        self.path = path

    def set_txt(self, txt):
        self.txt = txt


class OpenAction(object):
    def __init__(self, bookmarks=None):
        if bookmarks is None:
            bookmarks = []
        self.bookmarks = bookmarks

    def set_bookmarks(self, bookmarks):
        self.bookmarks = bookmarks


class SaveAction(object):
    def __init__(self,  path='', shift=0, pdf=None, treeRoot=None):
        self.path = path
        self.shift = shift
        self.pdf = pdf
        self.treeRoot = treeRoot


    def set_path(self, path):
        self.path = path

    def set_shift(self, shift):
        self.shift = shift

    def set_pdf(self, pdf):
        self.pdf = pdf

    def set_treeRoot(self, treeRoot):
        self.treeRoot = treeRoot
