import  fitz

class Bookmarks(object):
    def __init__(self):
        self.bookmarks = []
        self.doc = None
        self.txt = ''

    def read_pdf(self, path):
        self.doc = fitz.open(path)
        self.bookmarks = self.doc.get_toc()
        self.__init_txt()

    def __init_txt(self):
        length = len(self.bookmarks)

        blank = 0
        for page in range(length):
            blank = self.bookmarks[page][0] - 1
            if page >= 1:
                self.txt = f'{self.txt}\n'
                # 添加 '\t'
                for i in range(blank):
                    self.txt = f'{self.txt}\t'
                self.txt = f'{self.txt}{self.bookmarks[page][1]}\t{self.bookmarks[page][2]}'
            else:
                self.txt = f'{self.bookmarks[page][1]}\t{self.bookmarks[page][2]}'

    def close(self):
        self.doc.close()

if __name__ == "__main__":
    pages = Bookmarks()
    pages.read_pdf("E:\Desktop\PyQt5快速开发与实战.pdf")
    print(pages.bookmarks)
    pages.close()
