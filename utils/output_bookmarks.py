

class OutputBookmarks(object):
    def __init__(self):
        self.txt = ''
        self.signals = None
        self.path = ''

    def output_bookmarks(self, signals, args ):
        self.txt = args[0]
        self.path = args[1]
        self.signals = signals

        try:
            with open(self.path,  'w', encoding='utf-8',) as f:
                f.write(self.txt)
        finally:
            f.close()


