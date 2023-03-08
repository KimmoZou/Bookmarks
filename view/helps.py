from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QTextEdit, QVBoxLayout, QDialogButtonBox
from resources import resources_rc

class Help(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QVBoxLayout()
        self.text = QTextEdit()
        self.text.setStyleSheet(
            "QTextEdit{"
            "border:none;"
            "background:rgb(240, 240, 240)"
            "}"
        )
        self.ok = QDialogButtonBox(QDialogButtonBox.Ok)
        self.text.setReadOnly(True)
        self.setMinimumSize(400, 500)
        self.setWindowTitle("bookmarks")
        self.setWindowIcon(QIcon(r":\icon\icon-app"))
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.ok)
        self.setLayout(self.layout)
        self.__set_text()

        # 事件
        self.ok.clicked.connect(self.close)

    def __set_text(self):
        self.text.setText(""
                          "<body "
                          " style = "
                          " font-style:normal;"
                          ">"
                          "<h1>Bookmarks</h1>"
                          "<p>  pdf 给 pdf 文件添加目录。</p>"
                          "<h2>导出目录</h2>"
                          "<p>  将当前的pdf文件目录导出指定到txt文件。</p>"
                          "<h2>导入目录</h2>"
                          "<p>  将txt文件的目录导入到下方的目录树编辑器中。</p>"
                          "<p>  txt文件中以tab缩进来区分文件目录层级。</p>"
                          "<h2>保存文件</h2>"
                          "<p>  生成当前文件副本，并将目录树编辑器的目录保存到pdf副本中。</p>"
                          "</body>"
                          )



from PySide6.QtWidgets import QApplication

if __name__ == "__main__":

    app = QApplication([])
    app.setStyle('fusion')
    window = Help()
    window.show()
    app.exec()
